# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import LechebangPenqi
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='lechebang_penqi'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ["http://m.lechebang.com/gateway/maintenance/getCitys"]

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # super(KoubeiSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    # def start_requests(self):
    #     return [scrapy.Request(method="post", url='http://m.lechebang.com/gateway/car/getBrandProducerCar', meta={
    #
    #         "brandId":620,
    #         "appCode":600,
    #         # "token":"f906252f278dbbe35517c7c56e3cbd02",
    #         # "lcb_client_id": "b4d53546a02f87af",
	 #        # "lcb_request_id": "d57508cd-ba49-4af1-9af1-783fb05cbe51",
    #     })]
    def parse(self, response):
        city_list = ["上海", "北京", "成都", "苏州", "郑州", "石家庄", "西安", "昆明", "泉州", "滁州"]
        citys = json.loads(response.body)
        for city in citys["result"]["all"]:
            if city["name"] in city_list:
                meta = {
                    "cityId":city["code"],
                    "cityname":city["name"],
                    "appCode": 600,
                    "brandId": 620,
                }
                yield scrapy.Request("http://m.lechebang.com/gateway/car/getBrandProducerCar", meta=meta, callback=self.parse_family, dont_filter=True)

    def parse_family(self, response):

        families = json.loads(response.body)
        for family in families["result"]:
            if family["producerName"] in ["上海大众"]:
                for familyName in family["brandProduceCar"]:
                    meta = {
                        "appCode": 600,
                        "brandId": familyName["id"],
                        "familyName":familyName["carName"],
                        "cityId": response.meta["cityId"],
                        "cityname": response.meta["cityname"],
                    }
                    yield scrapy.Request("http://m.lechebang.com/gateway/car/getCarTypeDetail", meta=meta, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):

        cars = json.loads(response.body)
        for car in cars["result"]:
            meta = {
                "brandTypeId": car["id"],
                "appCode": "600",
                "token": "f906252f278dbbe35517c7c56e3cbd02",
                "familyName": response.meta["familyName"],
                "modelname":car["wholeName"],
                "cityId": response.meta["cityId"],
                "cityname": response.meta["cityname"],
            }
            yield scrapy.Request("http://m.lechebang.com/gateway/spray/getSprayItemInfoCross", meta=meta, callback=self.parse_json, dont_filter=True)


    def parse_json(self, response):
        print(response.text)
        for product in json.loads(response.text)["result"]["sprayItemInfoList"]:
            partname = product["partName"]
            for p in product["itemPriceInfo"]:
                item = LechebangPenqi()
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['partname'] = partname
                item['itemid'] = p["itemId"]
                item['itemname'] = p["itemName"]
                item['metalMarketPrice'] = p["metalMarketPrice"]
                item['metalSalePrice'] = p["metalSalePrice"]
                item['sprayMarketPrice'] = p["sprayMarketPrice"]
                item['spraySalePrice'] = p["spraySalePrice"]
                item['cityname'] = response.meta["cityname"]
                item['familyname'] = response.meta["familyName"]
                item['modelname'] = response.meta["modelname"]
                item['status'] = item['cityname'] + item['familyname'] + item['modelname'] + item['partname'] + str(item['itemid'])
                yield item
