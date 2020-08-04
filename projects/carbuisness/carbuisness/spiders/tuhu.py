# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import tuhuBaoYangItem
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
from urllib import quote

website='tuhu'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://item.tuhu.cn/Car/GetCarBrands?"
    ]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self, response):
        brands = json.loads(response.body)
        for brand_obj in brands["Brand"]:
            brand_str = brand_obj["Brand"].replace(" ", "+")
            url = "https://item.tuhu.cn/Car/SelOneBrand?Brand=%s&pwd=123456" % brand_str
            yield scrapy.Request(url, callback=self.parse_brand)


    def parse_brand(self, response):
        families = json.loads(response.body)
        for family in families["OneBrand"]:
            temp = {
                "Vehicle":family["Vehicle"],
                "ProductID": family["ProductID"],
                "Brand": family["Brand"],
            }
            url = "https://item.tuhu.cn/Car/SelectVehicle"
            yield scrapy.FormRequest(url, formdata={"VehicleID":family["ProductID"]}, meta=temp, callback=self.parse_pailiang)

    def parse_pailiang(self, response):
        pailiangs = json.loads(response.body)
        for pailiang in pailiangs["PaiLiang"]:
            temp = {
                "PaiLiang":pailiang["Value"]
            }
            temp = dict(temp, **response.meta)
            url = "https://item.tuhu.cn/Car/SelectVehicle"
            yield scrapy.FormRequest(url, formdata={"VehicleID":response.meta["ProductID"], "PaiLiang":pailiang["Value"]}, meta=temp, callback=self.parse_nian)

    def parse_nian(self, response):
        nians = json.loads(response.body)
        for nian in nians["Nian"]:
            temp = {
                "Nian": nian["Value"]
            }
            temp = dict(temp, **response.meta)
            vehicle_str = '"VehicleId":"%s","Nian":"%s","PaiLiang":"%s"' % (response.meta["ProductID"], nian["Value"], response.meta["PaiLiang"])
            url = "https://by.tuhu.cn/apinew/GetBaoYangManualTable.html?Vehicle={%s}" % vehicle_str
            yield scrapy.Request(url, meta=temp, callback=self.parse_detail)


    def parse_detail(self, response):
        details = json.loads(response.body)
        item = tuhuBaoYangItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item['vehicle'] = response.meta["Vehicle"]
        item['productID'] = response.meta["ProductID"]
        item['brand'] = response.meta["Brand"]
        item['paiLiang'] = response.meta["PaiLiang"]
        item['nian'] = response.meta["Nian"]
        item['accessoryData'] = details["Data"]["AccessoryData"] if details.has_key("Data") else "-"
        for data in details["Data"]["SuggestData"]:
            for i in range(32):
                if details["Data"]["SuggestData"].index(data) == i:
                    item["row%d" % i] = data
        yield item

