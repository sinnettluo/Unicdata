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

website='cheguansuo'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://cz.bendibao.com/cyfw/wangdian/1805.shtm"
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
        uls = response.xpath("//*[@id='listContent']/ul")
        for ul in uls:
            item = CheguansuoItem()
            item["name"] = ul.xpath("li[1]/a/text()").extract_first()
            item["addr"] = ul.xpath("li[2]/a/text()").extract_first()
            item["tel"] = ul.xpath("li[3]/text()").extract_first()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(uls.index(ul))
            yield item
