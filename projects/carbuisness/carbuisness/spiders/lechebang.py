# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import LechebangItem
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

website='lechebang_shanghai'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://m.lechebang.com/gateway/maintenance/getCitys"]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=10000000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        # citys = json.loads(response.body)
        # for city in citys["result"]["all"]:
        meta = {
            # "cityId":city["code"],
            "cityId":10201,
            "serviceType":1,
            "appCode":600
        }
        yield scrapy.Request("http://m.lechebang.com/gateway/car/getAllFirstLevelBrandType", meta=meta, callback=self.parse_brand, dont_filter=True)

    def parse_brand(self, response):
        brands = json.loads(response.body)
        for brand in brands["result"]:
            for brandName in brand["results"]:
                meta = {
                    "cityId": response.meta["cityId"],
                    "serviceType": 1,
                    "appCode": 600,
                    "brandId":brandName["id"],
                    "brandName":brandName["brandName"]
                }
                yield scrapy.Request("http://m.lechebang.com/gateway/car/getBrandProducerCar", meta=meta, callback=self.parse_family, dont_filter=True)

    def parse_family(self, response):
        families = json.loads(response.body)
        for family in families["result"]:
            for familyName in family["brandProduceCar"]:
                meta = {
                    "cityId": response.meta["cityId"],
                    "serviceType": 1,
                    "appCode": 600,
                    "brandId_brand": response.meta["brandId"],
                    "brandName": response.meta["brandName"],
                    "brandId":familyName["id"],
                    "familyName":familyName["carName"]
                }
                yield scrapy.Request("http://m.lechebang.com/gateway/car/getCarTypeDetail", meta=meta, callback=self.parse_car, dont_filter=True)

    def parse_car(self, response):
        cars = json.loads(response.body)
        for car in cars["result"]:
            meta = {
                "cityId": response.meta["cityId"],
                "serviceType": 1,
                "appCode": 600,
                "brandId_brand": response.meta["brandId_brand"],
                "brandName": response.meta["brandName"],
                "brandId_family": response.meta["brandId"],
                "familyName": response.meta["familyName"],
                "brandTypeId":car["id"],
                "carName":car["carDetailName"],
                "carYear":car["yearName"],
                "mileage":1,
            }
            yield scrapy.Request("http://m.lechebang.com/gateway/plan/getMaintenanceManual", meta=meta, callback=self.parse_json, dont_filter=True)

    def parse_json(self, response):
        info_json = json.loads(response.body)
        for info in info_json["result"]:
            item = LechebangItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url + "-" + str(response.meta["brandTypeId"])
            item['status'] = str(info["plan"]["id"])
            item['cityId'] = response.meta["cityId"]
            item['brandId_brand'] = response.meta["brandId_brand"]
            item['brandName'] = response.meta["brandName"]
            item['brandId_family'] = response.meta["brandId_family"]
            item['familyName'] = response.meta["familyName"]
            item['brandTypeId'] = response.meta["brandTypeId"]
            item['carName'] = response.meta["carName"]
            item['carYear'] = response.meta["carYear"]
            item['mileage'] = info["plan"]["mileage"]
            item['items'] = info["items"]
            item['nearItems'] = info["nearItems"]
            item['otherItems'] = info["otherItems"]

            yield item

