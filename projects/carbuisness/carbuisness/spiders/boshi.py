# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import CheXiangJiaItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests

website='boshi_2019_fix'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.boschcarservice.com.cn/web/dealer_list.jsp"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        provs = response.xpath("//*[@id='province_']/option")[1:]
        for prov in provs:
            provName = prov.xpath("text()").extract_first()
            url = "http://www.boschcarservice.com.cn/web/common/select_city.jsp?province=%s" % provName
            yield scrapy.Request(url=url, meta={"provName":provName}, callback=self.parse_city)

    def parse_city(self, response):
        selector = etree.fromstring(response.body)
        citys = selector.xpath("//option")[1:]
        for city in citys:
            cityName = city.xpath("text()")[0]
            for i in [1, 2, 3]:
                print(response.meta["provName"] + cityName + str(i))
                url = "http://www.boschcarservice.com.cn/web/dealer_list.jsp?province=%s&city=%s&dealer_type=%d&kw=" % (response.meta["provName"], cityName, i)
                yield scrapy.Request(url=url, meta={"provName":response.meta["provName"], "cityName":cityName, "type":i}, callback=self.parse_list)

    def parse_list(self, response):
        stores = response.xpath("//*[@id='right']/div[2]/div")
        for store in stores[:-1]:
            typeNameList = [u"直营店", u"综合汽车服务", u"快捷汽车服务"]
            item = CheXiangJiaItem()
            item['status'] = response.url + "-" + str(stores.index(store))
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['address'] = store.xpath("div[3]/table/tr/td[2]/table/tr[1]/td[2]/text()").extract_first()
            item['businesstime'] = store.xpath("div[3]/table/tr/td[2]/table/tr[3]/td[2]/text()").extract_first()
            item['telephone'] = store.xpath("div[3]/table/tr/td[2]/table/tr[2]/td[2]/text()").extract_first()
            item['storeName'] = store.xpath("div[1]/div[1]/b/a/text()").extract_first()
            item['storeId'] = store.xpath("div[1]/div[1]/b/a/@href").re("\d+")[0]
            baidu_api_url = "http://api.map.baidu.com/place/v2/search?query=%s&region=%s&output=json&ak=0nIp0ZxAyuSbIloGzSqZMK006GALOZMo" % (
            item['address'], response.meta["provName"])
            print(baidu_api_url)
            res = requests.request("get", baidu_api_url)
            baidu_api_obj = json.loads(res.text)
            try:
                item['localX'] = baidu_api_obj['results'][0]['location']['lat']
            except:
                item['localX'] = "-"
            try:
                item['localY'] = baidu_api_obj['results'][0]['location']['lng']
            except:
                item['localY'] = '-'

            print(item['localX'])
            print(item['localY'])
            item['areaName'] = response.meta["cityName"]
            item['provinceName'] = response.meta["provName"]
            item['type'] = response.meta["type"]
            item['typeName'] = typeNameList[item['type']-1]
            # print(item)
            yield item
