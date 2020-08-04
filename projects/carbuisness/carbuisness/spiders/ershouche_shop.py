# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import ErshoucheShopItem
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

website='ershouche_trade_cangzhou'

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

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        for i in range(50):
            url = u"http://map.baidu.com/?qt=con&c=149&wd=沧州二手车交易市场&nn=%d" % (i*10)
            yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        data_dict = json.loads(response.body)
        for shop in data_dict["content"][:-1]:
            item = ErshoucheShopItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            # item['status'] = response.url + "-" + str(data_dict["content"].index(shop))
            item['status'] = shop["primary_uid"]
            item['shopname'] = shop["name"]
            item['x'] = shop["x"]
            item['y'] = shop["y"]
            item['di_tag'] = shop["di_tag"]
            item['addr'] = shop["addr"]
            yield item