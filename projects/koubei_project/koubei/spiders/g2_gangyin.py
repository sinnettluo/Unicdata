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

website='g2_gangyin2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000


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
        url = "https://chaoshi.banksteel.com/chaoshi/queryPageItem.jsp"
        urls = list()
        for m in ['SPCC', 'SPHC']:
            formdata = {
                "pageSize": "28",
                "pageNum": "1",
                "keyword": m
            }
            urls.append(scrapy.FormRequest(method="post", url=url, meta=formdata, formdata=formdata, dont_filter=True))
        return urls

    def parse(self, response):
        result =  json.loads(response.text)
        if result["totalCount"] != 0:
            for i in range(1, int(math.ceil(result["totalCount"]/12))+1):
                formdata = {
                    "pageSize": "28",
                    "pageNum": str(i),
                    "keyword": response.meta["keyword"]
                }
                url = "https://chaoshi.banksteel.com/chaoshi/queryPageItem.jsp"
                yield scrapy.FormRequest(method="post", url=url, meta=formdata, formdata=formdata, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        result = json.loads(response.text)
        for product in result["recordList"]:
            item = GangItem()
            item['url'] = response.url
            item['status'] = product["summaryCode"]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product["categoryName"]
            item['material'] = product["materialName"]
            item['weight'] = product["qty"]
            item['quantity'] = product["num"]
            item['type'] = product["specName"]
            item['factory'] = product["factoryName"]
            item['price'] = product["price"]
            item['storage'] = product["warehouseName"]
            item['city'] = product["areaName"]

            # print(item)
            yield item