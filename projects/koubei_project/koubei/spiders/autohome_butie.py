# -*- coding: utf-8 -*-
"""
C2017-40
"""
import scrapy
from koubei.items import AutohomeButieItem
import time
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
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

website = 'autohome_butie'


class CarSpider(scrapy.Spider):
    name = website
    start_urls = []

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 800000

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        request_list = []

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        result = collection.distinct("autohomeid")
        for r in result:
            url = "https://carif.api.autohome.com.cn/car/getspecelectricbutie.ashx?_callback=GetSpecElectricSubsidy&speclist=%s&cityid=310100&type=1" % str(
                r)
            request_list.append(scrapy.Request(url, meta={"autohomeid": r}, callback=self.parse))
        return request_list

    def parse(self, response):
        obj = json.loads(response.text.replace("GetSpecElectricSubsidy(", "")[:-1])

        item = AutohomeButieItem()
        item['url'] = response.url
        item['status'] = response.url + time.strftime('%Y-%m', time.localtime())
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['autohomeid'] = response.meta["autohomeid"]
        item['minprice'] = obj['result']['specitems'][0]['minprice']
        item['maxprice'] = obj['result']['specitems'][0]['maxprice']

        yield item
