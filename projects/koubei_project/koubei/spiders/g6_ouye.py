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

website='g6_ouye'

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
            url = "https://www.ouyeel.com/jk-mobile/search/main-search/"
            data = {
                "page": "1",
                "keywords": m,
            }
            urls.append(scrapy.FormRequest(method="post", url=url, meta=data, formdata=data, headers=self.headers, dont_filter=True))
        return urls

    def parse(self, response):
        result = json.loads(response.text)

        if result["has_more"] == 1:
            url = "https://www.ouyeel.com/jk-mobile/search/main-search/"
            data = {
                "page": str(int(response.meta["page"]) + 1),
                "keywords": response.meta["keywords"],
            }
            yield scrapy.FormRequest(method="post", url=url, meta=data, formdata=data, headers=self.headers, dont_filter=True)

        for product in result["data"]:
            item = GangItem()
            item['url'] = response.url
            item['status'] = str(product["id"])
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product["product_name"]
            item['material'] = product["shop_sign"]
            item['weight'] = product["weight"]
            item['type'] = product["spec"]
            item['factory'] = product["manufacturer"]
            item['price'] = product["price"]
            item['storage'] = product["warehouse_name"]
            item['city'] = product["store_city_name"]
            item['company'] = product["provider_name"]
            item['posttime'] = product["active_date"]

            # print(item)
            yield item