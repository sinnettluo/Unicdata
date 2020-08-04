# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import TuhuTiresItem
# from scrapy.conf import self.settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='tuhu_tires'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['https://item.tuhu.cn/Tires/1/f0-a0-r1-w0.html#ProductFilter']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=self.settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
    #     self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
    #     super(KoubeiSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    # def start_requests(self):
    #     for i in range(1, 20):
    #         yield scrapy.Request(url="https://api.touchev.com:83/api/0190/index/index.do?jpushId=1507bfd3f79851701fd&deviceId=869622035270223&userId=&sss=b235a2d3468dd22be9a071cbf1016978&idx=0&first=no&appName=%E7%AC%AC%E4%B8%80%E7%94%B5%E5%8A%A8&lng=121.510961&network=wifi&naviId=12&networkOperator=CMCC&imei=869622035270223&deviceOsVer=7.0&deviceOs=android&appVer=1.9.2&tpToken=&page=" + str(i) + "&lat=31.292386&channel=yingyongbao&appToken=&limit=20&deviceSysVar=RNE-AL00%7CHUAWEI")

    def parse(self, response):
        first_param = response.xpath("//*[@id='CP_Tire_Width']/option/text()").extract()[2:]
        second_param = response.xpath("//*[@id='CP_Tire_AspectRatio']/option/text()").extract()[2:]
        final_param = response.xpath("//*[@id='CP_Tire_Rim']/option/text()").extract()[2:]
        for fp in first_param:
            for sp in second_param:
                for finalp in final_param:
                    url = "https://item.tuhu.cn/Tires/1/f0-a%s-r%s-w%s.html#ProductFilter" % (sp, finalp, fp)
                    meta = {
                        "first_param":fp,
                        "second_param": sp,
                        "final_param": finalp,

                    }
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)

    def parse_list(self, response):
        products = response.xpath("//*[@id='Products']/table[1]/tbody/tr")
        print(products)
        for product in products:
            item = TuhuTiresItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item['status'] = response.url + "-" + str(products.index(product))
            item['title'] = product.xpath("td[2]/a/div/text()").extract_first().strip()
            item['first_param'] = response.meta["first_param"]
            item['second_param'] = response.meta["second_param"]
            item['final_param'] = response.meta["final_param"]
            item['type'] = product.xpath("td[2]/div[1]/label[1]/span/text()").extract_first().strip()
            item['load_index'] = product.xpath("td[2]/div[1]/label[2]/span/text()").extract_first().strip()
            item['huawen'] = product.xpath("td[2]/div[1]/label[3]/span/text()").extract_first().strip()
            item['speed_level'] = product.xpath("td[2]/div[1]/label[4]/span/text()").extract_first().strip()
            item['price'] = product.xpath("td[3]/div[1]/strong/text()").extract_first().replace("¥", "")

            # print(item)
            yield item




