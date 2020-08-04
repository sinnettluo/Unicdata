# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GangItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
import pymongo
import math

website='g8_ggang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        urls = list()
        for m in ['SPCC', 'SPHC']:
            url = "http://res.ggang.cn/SteelList/GetProductList/?productType=全部&productName=全部&material=%s&standard=全部&productId=0&mills=全部&home=&maxPrice=&maxThick=&maxlength=&maxwidth=&minPrice=&minThick=&minlength=&minwidth=&pageIndex=1&productCity=&key=&IsPriceSort=0&pageSize=30&pageType=1" % m
            meta = {
                "pageIndex": 1,
                "material": m,
            }
            urls.append(scrapy.Request(method="get", url=url, meta=meta, headers=self.headers))
        return urls

    def parse(self, response):
        result = json.loads(json.loads(response.text))
        # print(result)
        # print(result["status"])
        if result["status"]["pageIndex"] == "1":
            pagenum = int(math.ceil(int(result["status"]["pagenum"])/30))
            if pagenum > 100:
                pagenum = 100
            for i in range(2, pagenum + 1):
                url = "http://res.ggang.cn/SteelList/GetProductList/?productType=全部&productName=全部&material=%s&standard=全部&productId=0&mills=全部&home=&maxPrice=&maxThick=&maxlength=&maxwidth=&minPrice=&minThick=&minlength=&minwidth=&pageIndex=%d&productCity=&key=&IsPriceSort=0&pageSize=30&pageType=1" % (response.meta["material"], i)
                meta = {
                    "pageIndex": i,
                    "material": response.meta["material"],
                }
                yield scrapy.Request(method="get", url=url, meta=meta, headers=self.headers, callback=self.parse)

        for product in result["msg"]:
            item = GangItem()
            item['url'] = response.url
            item['status'] = product["ID"]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product["name"]
            item['material'] = product["material"]
            item['weight'] = product["piece"]
            item['type'] = product["norms"]
            item['factory'] = product["plant"]
            item['price'] = product["price"]
            item['storage'] = product["wareHouse"]
            item['city'] = product["place"]
            item['company'] = product["source"]
            # item['posttime'] = response.xpath("ul/li/div[1]/text()").extract_first()

            # print(item)
            yield item