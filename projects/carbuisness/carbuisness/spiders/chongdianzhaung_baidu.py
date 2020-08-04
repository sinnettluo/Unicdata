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
import xlrd



website='chongdianzhuang_baidu'
# city_name = '邢台市'
page_num = 400

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [

    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        file = xlrd.open_workbook(u"D:/city_copy.xlsx")

        sheet = file.sheet_by_name("city_copy")

        cols_city_name = sheet.col_values(1)
        print(cols_city_name)
        # for city_name in cols_city_name:
        for city_name in ["上海市"]:
            for i in range(page_num):
                url = "http://api.map.baidu.com/place/v2/search?query=充电站&region=%s&page_num=%d&output=json&ak=0nIp0ZxAyuSbIloGzSqZMK006GALOZMo" % (city_name, i)
                yield scrapy.Request(url=url, meta={"city_name":city_name})

    def parse(self, response):
        obj = json.loads(response.body)
        for loc in obj["results"]:
            item = CheguansuoItem()
            item["name"] = loc["name"]
            item["addr"] = loc["address"]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(obj["results"].index(loc))
            item['lat']  = loc["location"]["lat"]
            item['lng'] = loc["location"]["lng"]
            item['city_name'] = response.meta["city_name"]
            item['province'] = loc["province"]
            item['city'] = loc["city"]
            item['area'] = loc["area"]
            yield item