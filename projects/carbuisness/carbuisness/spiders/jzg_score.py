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

website='jzg_score'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        ""
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
        provs = response.xpath("//*[@id='province_']/option")[1:]
        for prov in provs:
            provName = prov.xpath("text()").extract_first()
            url = "http://www.boschcarservice.com.cn/web/common/select_city.jsp?province=%s" % provName
            yield scrapy.Request(url=url, meta={"provName":provName}, callback=self.parse_city)

    def parse_city(self, response):
        pass