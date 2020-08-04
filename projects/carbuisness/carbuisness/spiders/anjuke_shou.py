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

website='anjuke_shou_fix'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://bj.sp.anjuke.com/shou/p1/"
    ]

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
        shops = response.xpath("//*[@class='list-item']|//*[@class='list-item item-over']")
        for shop in shops:
            item = FangZuItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = shop.xpath("@link").extract_first().strip()
            item["price"] = shop.xpath("div/div/em/text()").extract_first().strip()
            if u"\u4e07" in shop.xpath("div/div/text()[2]").extract_first().strip():
                item["price"] = item["price"] * 10000
            item["area"] = shop.xpath("dl/dd[1]/span[1]/text()").extract_first().replace(u"平米", "").strip()
            item["address"] = shop.xpath("dl/dd[2]/span/text()").extract_first().strip() \
                if shop.xpath("dl/dd[2]/span/text()") else "-"
            item["type"] = shop.xpath("dl/dd[1]/span[3]/text()").extract_first().strip() \
                if shop.xpath("dl/dd[1]/span[3]/text()") else "-"
            item["city"] = shop.xpath("//*[@id='list-content']/div[1]/span/em/text()").extract_first().strip()
            item["name"] = shop.xpath("dl/dd[2]/a/text()").extract_first().strip()
            item["layer"] = shop.xpath("dl/dd[1]/span[2]/text()").extract_first().strip()
            item["store_id"] = shop.xpath("@link").re("\d+")[0]
            item["title"] = shop.xpath("dl/dt/text()").extract_first().strip()
            # yield item
            # print(item)

        next = response.xpath("//a[@class='aNxt']")
        if next:
            yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), callback=self.parse)