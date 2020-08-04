# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeFamilyConfigItem
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
from carbuisness.items import WeatherItem
import pymongo

website='autohome_family_config'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]
        res = collection.distinct("familyid")
        for fid in res:
        # for fid in ['2533']:
            url = "https://car.autohome.com.cn/price/series-%s.html" % fid
            yield scrapy.Request(url=url, meta={"fid":fid})

    def parse(self, response):
        item = AutohomeFamilyConfigItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        # item['status'] = re.findall("\d+", response.xpath("//*[@class='main-title']/a/@href").extract_first().split("#")[0])
        item['status'] = response.url
        item['brand'] = response.xpath("//*[@class='fn-left cartab-title-name']/a/text()").extract_first()
        item['brandid'] = re.findall("\d+", response.xpath("//*[@class='fn-left cartab-title-name']/a/@href").extract_first())[0]
        item['family'] = response.xpath("//*[@class='main-title']/a/text()").extract_first()
        item['familyid'] = response.meta["fid"]
        item['level'] = response.xpath("//*[@class='lever-ul']/li[1]/span/text()").extract_first()
        item['body'] = response.xpath("//*[@class='lever-ul']/li[2]/a")
        temp = []
        for body in item['body']:
            temp.append(body.xpath("text()").extract_first())
        item['body'] = temp
        item['engine'] = response.xpath("//*[@class='lever-ul']/li[3]/span/a")
        temp = []
        for engine in item['engine']:
            temp.append(engine.xpath("text()").extract_first())
        item['engine'] = temp
        item['gear'] = response.xpath("//*[@class='lever-ul']/li[4]/a")
        temp = []
        for gear in item['gear']:
            temp.append(gear.xpath("text()").extract_first())
        item['gear'] = temp
        yield item