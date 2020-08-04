# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import TeLaiDianItem
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

website='telaidian'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.teld.cn/StationNetwork/Chargenet"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000
        self.page = 1
        self.page_start = 0

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.Chrome(executable_path=settings['CHROME_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        # print(response.body)
        while self.page <= 36:
            try:
                res = etree.HTML(response.text)
            except Exception as e:
                res = etree.HTML(response)
            lis = res.xpath("//*[@class='scroll']/ul[@class='list']/li[@class='item']")
            print(len(lis))
            for li in lis[:10]:
                item = TeLaiDianItem()
                # print(li.xpath("div[1]/div[1]/text()"))
                item['name'] = li.xpath("div[1]/div/text()")[0].strip()
                item['address'] = li.xpath("div[2]/text()")[0].strip()
                if li.xpath("div[3]/span[@class='fast']"):
                    item['fast'] = "True"
                if li.xpath("div[3]/span[@class='slow']"):
                    item['slow'] = "True"
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['url'] = self.browser.current_url
                item['status'] = self.browser.current_url + "-" + str(lis.index(li)) + "-" + str(self.page)
                yield item


            print(self.page)
            print(self.page_start)

            next = res.xpath("//*[@class='pagination pagination-sm']/li[%d]/a/text()" % (3+self.page_start))[0]
            print(next)

            if int(next) <= 3:
                print("s1")
                self.page = int(next)
                self.browser.find_element_by_xpath(
                    "//*[@class='pagination pagination-sm']/li[%d]/a" % (3 + self.page_start)).click()
                time.sleep(10)
                self.page_start += 1
            elif next != str(self.page) and int(next) > 3:
                print("s2")
                self.page = int(next)
                self.browser.find_element_by_xpath(
                    "//*[@class='pagination pagination-sm']/li[5]/a").click()
                time.sleep(10)
                response = self.browser.page_source
            else:
                print("s3")
                self.page = int(next) + 1
                self.browser.find_element_by_xpath(
                    "//*[@class='pagination pagination-sm']/li[6]/a").click()
                time.sleep(10)
                response = self.browser.page_source