# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import AutohomeRegYearItem
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
import MySQLdb
import pymongo

website='autohome_newcar_reg_year'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.baidu.com"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        print("querying...")
        res = collection.distinct("autohomeid")

        for id in res:
            url = "https://cacheapi.che168.com/CarProduct/GetParam.ashx?specid=%s" % id
            yield scrapy.Request(url=url, callback=self.parse_reg_year)


    def parse_reg_year(self, response):
        item = AutohomeRegYearItem()
        data_obj = json.loads(response.body.decode("gbk"))
        item['reg_year'] = '-'
        try:
            for i in data_obj['result']['paramtypeitems'][0]['paramitems']:
                if i["name"] == u'上市时间':
                    item['reg_year'] = i['value']
        except Exception as e:
            pass
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['autohomeid'] = data_obj['result']['specid']


        yield item