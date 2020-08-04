# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import TuhuProductsItem
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
import requests

website='tuhu_products'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://item.tuhu.cn/List/BY/"
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
        lis = response.xpath("//li[@class='cpli']")
        print(lis)
        for li in lis:
            url = li.xpath("a/@href").extract_first()
            yield scrapy.Request(url=url, callback=self.parse_details)

        next = response.xpath("//a[@class='last-child']")
        if next:
            url = next.xpath("@href").extract_first()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_details(self, response):
        item = TuhuProductsItem()
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['title'] = response.xpath("//*[@id='product_detail']/div[2]/h1/text()").extract_first().strip()
        item['small_title'] = response.xpath("//*[@id='product_detail']/div[2]/span/text()").extract_first().strip()
        item['price'] = response.xpath("//*[@id='product_detail']/div[2]/div[2]/div[2]/strong/text()").extract_first()
        lis = response.xpath("//*[@id='product_detail']/div[2]/div[1]/ul/li")
        configs = {}
        for li in lis:
            key = li.xpath("span/text()").extract_first().replace("：", "")
            value = li.xpath("text()").extract_first()
            configs[key] = value
        item['config'] = configs
        yield item
