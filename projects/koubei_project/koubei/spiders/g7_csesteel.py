# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GangItem
import time
# from scrapy.conf import settings
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
import math

website='g7_csesteel'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        urls = list()
        for m in ['SPCC', 'SPHC']:
            url = "http://www.csesteel.com/online/resource/hall/goodList?ajaxCmd=goodContent&securityToken="
            data = {
                "current": "1",
                "ph": m,
            }
            urls.append(scrapy.FormRequest(method="post", url=url, meta=data, formdata=data, headers=self.headers, dont_filter=True))
        return urls

    def parse(self, response):

        next = response.xpath("//*[@class='page-nex page-control']")
        if next:
            url = "http://www.csesteel.com/online/resource/hall/goodList?ajaxCmd=goodContent&securityToken="
            data = {
                "current": str(int(response.meta["current"]) + 1),
                "ph": response.meta["ph"],
            }
            yield scrapy.FormRequest(method="post", url=url, meta=data, formdata=data, headers=self.headers,
                                           dont_filter=True)

        products = response.xpath("//*[@class='main-content']/div[@class='list']")
        for product in products:
            item = GangItem()
            item['url'] = response.url
            item['status'] = product.xpath("ul/li/div[1]/a/@href").re("\d+")[0]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product.xpath("ul/li/div[1]/a/text()").extract_first()
            item['material'] = product.xpath("ul/li/div[2]/text()").extract_first()
            item['weight'] = product.xpath("ul/li/div[8]/text()").extract_first()
            item['type'] = product.xpath("ul/li/div[3]/text()").extract_first()
            item['factory'] = product.xpath("ul/li/div[4]/text()").extract_first()
            item['price'] = product.xpath("ul/li/div[9]/span/text()").extract_first().strip().replace("￥", "")
            item['storage'] = product.xpath("ul/li/div[5]/div/div[2]/text()").extract_first()
            item['city'] = product.xpath("ul/li/div[5]/span/text()").extract_first()
            # item['company'] = response.xpath("ul/li/div[1]/text()").extract_first()
            # item['posttime'] = response.xpath("ul/li/div[1]/text()").extract_first()

            # print(item)
            yield item