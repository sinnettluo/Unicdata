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

website='g3_zhonggang2'

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
            url = "https://www.zgw.com/ProductResource/LoadXht?zl=&pm=&cz=%s&gg=&w=&w1=&h=&h1=&pa=&comp=&iston=-1&isdown=-1&cityid=-1&page=1&isgz=0&txtw=5&sa=" % m
            meta = {
                "pageNum": 1,
                "keyword": m
            }
            urls.append(scrapy.Request(method="get", url=url, meta=meta, headers=self.headers))
        return urls

    def parse(self, response):

        page = response.xpath("//*[@class='page']")
        if page:
            if page.xpath(".//a[text()='下一页']"):
                url = "https://www.zgw.com/ProductResource/LoadXht?zl=&pm=&cz=%s&gg=&w=&w1=&h=&h1=&pa=&comp=&iston=-1&isdown=-1&cityid=-1&page=%d&isgz=0&txtw=5&sa=" % (response.meta["keyword"], response.meta["pageNum"]+1)
                meta = {
                    "pageNum": response.meta["pageNum"]+1,
                    "keyword": response.meta["keyword"]
                }
                yield scrapy.Request(method="get", url=url, meta=meta, headers=self.headers, callback=self.parse)

        coms = response.xpath("//*[@class='xht_table']/tbody")
        for com in coms[1:]:
            did = com.xpath(".//*[@class='zk']/@did").extract_first()
            ct = com.xpath(".//*[@class='zk']/@ct").extract_first()
            comName = com.xpath(".//*[@class=' gs_name']/text()")
            if comName:
                comName = comName.extract_first().strip()
            posttime = com.xpath(".//td[5]/text()").extract_first()
            url = "https://www.zgw.com/ProductResource/GetXianHuoDetail"
            for i in range(1, int(math.ceil(int(ct)/15))+1):
                formdata = {
                    "count": ct,
                    "epid": did,
                    "page": str(i),
                    "price": "-1",
                    "cz": response.meta["keyword"]
                }
                meta = {
                    "company": comName,
                    "posttime": posttime
                }
                yield scrapy.FormRequest(method="post", url=url, formdata=formdata, meta=meta, dont_filter=True, headers=self.headers, callback=self.parse_product)


    def parse_product(self, response):
        result = json.loads(response.text)
        for product in result["PaperList"]:
            item = GangItem()
            item['url'] = response.url
            item['status'] = str(product["Id"])
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['name'] = product["Pm"]
            item['material'] = product["Cz"]
            item['weight'] = product["Ton"]
            item['type'] = product["Gg"]
            item['factory'] = product["ProductArea"]
            item['price'] = product["Price"]
            item['storage'] = product["StockArea"]
            item['city'] = product["DeliveryArea"]
            item['company'] = response.meta["company"]
            item['posttime'] = response.meta["posttime"]

            # print(item)
            yield item