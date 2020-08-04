# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import CheguansuoItem
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

website='cheguansuo_baidu'
city_name = '沧州市'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://map.baidu.com/?qt=s&wd=%s车管所" % city_name
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
        obj = json.loads(response.body)
        code = obj["current_city"]["code"]
        for i in range(0, 10):
            url = "https://map.baidu.com/?qt=s&wd=车管所&c=%s&nn=%i" % (code, (i*10))
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        obj = json.loads(response.body)
        if len(obj["content"]) > 10:
            locs = obj["content"][:-1]
        else:
            locs = obj["content"]
        for loc in locs:
            item = CheguansuoItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(obj["content"].index(loc))
            item['name'] = loc["name"]
            item['addr'] = loc["addr"]
            item['x'] = loc["x"]
            item['y'] = loc["y"]
            item['city_name'] = city_name
            yield item