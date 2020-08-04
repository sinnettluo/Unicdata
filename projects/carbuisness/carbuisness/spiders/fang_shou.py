# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import FangZuItem
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

website='fang_shou'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def start_requests(self):
        yield scrapy.Request(url="http://shop.fang.com/shou/house/i31/", dont_filter=True)

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        shops = response.xpath("//*[@class='shop_list']/dl")
        for shop in shops:
            item = FangZuItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = json.loads(shop.xpath("@data-bg").extract_first())["houseid"]
            item["price"] = shop.xpath("dd[3]/span[1]/b/text()").extract_first().strip() \
                if shop.xpath("dd[3]/span[1]/b/text()") else shop.xpath("dd[3]/span[1]/text()").extract_first().strip()
            item["area"] = shop.xpath("dd[2]/span[1]/b/text()").extract_first().strip()
            item["address"] = shop.xpath("dd[1]/p[1]/span/@title").extract_first().strip()
            item["type"] = shop.xpath("dd[1]/p[2]/text()[1]").extract_first().strip()
            item["city"] = "beijing"
            item["name"] = shop.xpath("dd[1]/p[1]/a/@title").extract_first().strip() \
                if shop.xpath("dd[1]/p[1]/a/@title") else shop.xpath("dd[1]/p[1]/text()").extract_first().strip()
            item["layer"] = shop.xpath("dd[1]/p[2]/text()[2]").extract_first().strip()
            item["store_id"] = json.loads(shop.xpath("@data-bg").extract_first())["houseid"]
            yield item
            # print(item)

        next = response.xpath("//*[@id='PageControl1_hlk_next']")
        if next:
            yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), callback=self.parse)