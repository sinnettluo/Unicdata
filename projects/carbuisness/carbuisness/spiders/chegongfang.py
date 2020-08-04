# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import CheXiangJiaItem
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

website='chegongfang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.caremore-sgm.com/store.html"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.Chrome(executable_path=settings['CHROME_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        dealers = response.xpath("//*[@class='dealer-item']")

        for dealer in dealers:
            item = CheXiangJiaItem()
            item['status'] = response.url + "-" + str(dealers.index(dealer))
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['storeName'] = dealer.xpath("h5/text()").extract_first()
            item['address'] = dealer.xpath("@data-address").extract_first()
            item['telephone'] = dealer.xpath("@data-tel").extract_first()

            yield item
