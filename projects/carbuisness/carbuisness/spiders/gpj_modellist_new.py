# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import GpjModelListItem
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
from carbuisness.items import ZupukItem
from lxml import etree
import pymongo
import MySQLdb

website='gpj_modellist_new'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://api8.gongpingjia.com/mobile/api/brand-data/"]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000
        self.city_count = 0
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','residual_value',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    # def start_requests(self):
    #     yield scrapy.FormRequest(url="http://common.jingzhengu.com/carStyle/getMakesPanelHtml", formdata={"hasAppraise":"true", "hasNewCar":"true", "hasElec":"true"})

    def parse(self, response):
        brands = json.loads(response.text)
        for brand in brands["brand"]:
            url = "http://api8.gongpingjia.com/mobile/api/model-query/?brand=%s" % brand["slug"]
            meta = {
                "brandname": brand["name"],
                "brandid": brand["slug"]
            }
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)


    def parse_family(self, response):
        families = json.loads(response.text)
        for factories in families["models"]:
            factory = factories["mum"]
            for family in factories["models"]:
                url = "http://api8.gongpingjia.com/mobile/api/detail-model-query/?brand=%s&model=%s" % (response.meta["brandid"], family["slug"])
                meta = {
                    "factoryname": factory,
                    "familyname": family["name"],
                    "familyid": family["slug"],
                }
                meta = dict(meta, **response.meta)
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_model)


    def parse_model(self, response):
        models = json.loads(response.text)
        for model in models["detail_model"]:
            item = GpjModelListItem()
            item["brandcode"] = response.meta["brandid"]
            item["brandname"] = response.meta["brandname"]
            item["familyname"] = response.meta["familyname"]
            item["familycode"] = response.meta["familyid"]
            item["factoryname"] = response.meta["factoryname"]
            item["model_detail"] = model["detail_model"]
            item["emission_standard"] = model["emission_standard"]
            item["transmission"] = model["transmission"]
            item["max_reg_year"] = model["max_reg_year"]
            item["volume"] = model["volume"]
            item["min_reg_year"] = model["min_reg_year"]
            item["detail_model_slug"] = model["detail_model_slug"]
            item["year"] = model["year"]
            item["price_bn"] = model["price_bn"]

            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = response.url + "-" + str(models["detail_model"].index(model)) + "-" + time.strftime('%Y-%m', time.localtime())
            # print(item)
            yield item


