# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import w58officeitem
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
from carbuisness.items import WeatherItem

website='weather_tianqihoubao'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.tianqihoubao.com/lishi/"
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
        dls = response.xpath("//*[@id='content']/div[3]/dl")
        for dl in dls:
            print(dl.xpath("./dd/a/text()").extract_first())
            if dl.xpath("./dd/a/text()").extract_first() in ['上海','咸阳']:
                city_url = response.urljoin(dl.xpath("./dd/a/@href").extract_first())
                # print(city_url)
                yield scrapy.Request(url=city_url, callback=self.parse_url)
        # yield scrapy.Request(url="http://www.tianqihoubao.com/lishi/shanghai.html", callback=self.parse_url)
        # yield scrapy.Request(url="http://www.tianqihoubao.com/lishi/xiaogan.html", callback=self.parse_url)


    def parse_url(self, response):
        uls = response.xpath("//*[@id='content']/div[@class='box pcity']/ul")
        for ul in uls:
            details_urls = ul.xpath(".//a")
            # print(details_urls)
            for details_url in details_urls:
                # print(response.urljoin(details_url.xpath("@href").extract_first()))
                yield scrapy.Request(url=response.urljoin(details_url.xpath("@href").extract_first()), callback=self.parse_details)

    def parse_details(self,response):

        trs = response.xpath("//*[@id='content']/table/tr")
        print(trs)
        for tr in trs:
            print(tr)
            if trs.index(tr) is not 0:
                print("yes")
                item = WeatherItem()
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['url'] = response.url
                item['data'] = tr.xpath("./td[1]/a/text()").extract_first().strip()
                item['status'] = tr.xpath("./td[1]/a/@href").extract_first()
                item['weather'] = tr.xpath("./td[2]/text()").extract_first().strip()
                item['temp'] = tr.xpath("./td[3]/text()").extract_first().strip()
                item['wind'] = tr.xpath("./td[4]/text()").extract_first().strip()
                item['data_url'] = tr.xpath("./td[1]/a/@href").extract_first()
                item['title'] = response.xpath("//*[@id='content']/h1/text()").extract_first()
                yield item
