# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import CurrencySupplyItem
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

website='currency_supply'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=1",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=2",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=3",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=4",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=5",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=6",
        "http://data.eastmoney.com/cjsj/moneysupply.aspx?p=7",
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
        trs = response.xpath("//*[@id='tb']/tr")[2:-1]
        for tr in trs:
            item = CurrencySupplyItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = response.url + "-" + str(trs.index(tr))
            item['m2'] = tr.xpath("td[2]/text()").extract_first().strip()
            item['m2_last_year'] = tr.xpath("td[3]/span/text()").extract_first().strip()
            item['m2_last_month'] = tr.xpath("td[4]/span/text()").extract_first().strip()
            item['m1'] = tr.xpath("td[5]/text()").extract_first().strip()
            item['m1_last_year'] = tr.xpath("td[6]/span/text()").extract_first().strip()
            item['m1_last_month'] = tr.xpath("td[7]/span/text()").extract_first().strip()
            item['m0'] = tr.xpath("td[8]/text()").extract_first().strip()
            item['m0_last_year'] = tr.xpath("td[9]/span/text()").extract_first().strip()
            item['m0_last_month'] = tr.xpath("td[10]/span/text()").extract_first().strip()
            item['date'] = tr.xpath("td[1]/text()").extract_first().strip()
            yield item

