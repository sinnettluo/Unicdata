# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import UsedcarSalesItem
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
import datetime

website='usedcar_sales'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.suta.org.cn/tjjybb"
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
        for i in range(-365, 0):

            time = datetime.datetime(2018, 9, 11)
            change_time = time + datetime.timedelta(days=i)
            change_time_format = change_time.strftime('%Y-%m-%d')

            url = "http://www.suta.org.cn/tjjybb?cycle=1&pic_type=3&qsrq=%s&zzrq=%s" % (change_time_format, change_time_format)
            yield scrapy.Request(url=url, meta={"time":change_time_format}, callback=self.parse_sales)


    def parse_sales(self, response):
        trs = response.xpath("//*[@id='content']/form/table/tr[6]/td/table/tr/td/table/tr")[4:]
        for tr in trs:
            item = UsedcarSalesItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(trs.index(tr))
            item['market'] = tr.xpath("td[1]/font/text()").extract_first()
            item['amount'] = tr.xpath("td[2]/text()").extract_first()
            item['value'] = tr.xpath("td[3]/text()").extract_first()
            item['keche'] = tr.xpath("td[4]/text()").extract_first()
            item['huoche'] = tr.xpath("td[5]/text()").extract_first()
            item['motuoche'] = tr.xpath("td[6]/text()").extract_first()
            item['date'] = response.meta["time"]
            yield item

