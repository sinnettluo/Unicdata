# -*- coding: utf-8 -*-
"""
C2017-41

"""
import scrapy
from carbuisness.items import BochewangCarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from urllib import quote

website='all_province'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=10000000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self):
        self.browser.quit()

    def parse(self,response):
        ss = response.xpath("//*[@id='ss']/option")
        for s in ss[1:]:
            shengji = s.xpath("text()").extract_first()
            yield scrapy.FormRequest(url="http://xzqh.mca.gov.cn/selectJson", formdata={"shengji", shengji.decode("gb2312")}, callback=self.parse_diji)


    def parse_diji(self, response):
        obj = json.loads(response.body)
        print(obj)