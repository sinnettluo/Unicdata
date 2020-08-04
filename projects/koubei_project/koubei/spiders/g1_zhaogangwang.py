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

website='g1_zhaogangwang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        # }
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
        for type in ['SPCC', 'SPHC']:
            for i in range(1, 101):
                data_dict = {
                    "basicQuery": type,
                    "isBasicSearch": 1,
                    "searchFlag": 0,
                    "shopTypeList": None,
                    "pageIndex": i,
                    "pageSize": 10,
                    "orderTimeIndex": None,
                    "orderPriceIndex": None,
                    "orderSpecIndex": None,
                    "sourceState": None,
                    "normName": None,
                    "normMaterial": None,
                    "normSpecification": None,
                    "normFactory": None,
                    "companyName": None,
                    "thicknessStart": None,
                    "thicknessEnd": None,
                    "widthStart": None,
                    "widthEnd": None,
                    "lengthStart": None,
                    "lengthEnd": None,
                    "toleranceStart": None,
                    "toleranceEnd": None,
                    "exteriorName": None,
                    "lableItemList": [],
                    "canLableQuery": "T",
                    "dataVersion": 1
                }
                req = scrapy.Request(url="http://mall.zhaogang.com/api/goods/getSearchGoods", meta=data_dict, dont_filter=True)
                urls.append(req)
        return urls

    def parse(self, response):
        result = json.loads(response.text)
        for product in result["data"]["list"]:
            productids = product["productIds"]
            posttime = product["lastUpdateTime"]
            data_dict = {
                "dataVersion": 9,
                "pageIndex":1,
                "sonDataIndex":result["data"]["list"].index(product),
                "spotIds":productids,
                "posttime":posttime
            }
            if not product["companyName"]:
                item = GangItem()
                item['url'] = response.url
                item['status'] = product["id"]
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['name'] = product["categoryName"]
                item['material'] = product["materialName"]
                item['weight'] = product["pieceWeight"]
                item['type'] = product["specificationName"]
                item['factory'] = product["factoryName"]
                item['price'] = product["mallPrice"]
                item['storage'] = product["warehouseName"]
                item['city'] = product["city"]
                item['company'] = "找钢网"
                item['posttime'] = posttime

                # print(item)
                yield item
            else:
                yield scrapy.Request(url="http://mall.zhaogang.com/api/goods/findThirdGoodsItems", meta=data_dict, callback=self.parse_products, dont_filter=True)

    def parse_products(self, response):
        # print(response.request.meta)
        # print(response.text)
        result = json.loads(response.text)
        for product in result["data"]["list"]:
            item = GangItem()
            item['url'] = response.url
            item['status'] = product["id"]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product["categoryName"]
            item['material'] = product["material"]
            item['weight'] = product["pieceWeight"]
            item['type'] = product["specification"]
            item['factory'] = product["factory"]
            item['price'] = product["mallPrice"]
            item['storage'] = product["warehouse"]
            item['city'] = product["city"]
            item['company'] = product["orgTitleName"]
            item['posttime'] = response.request.meta["posttime"]

            # print(item)
            yield item
