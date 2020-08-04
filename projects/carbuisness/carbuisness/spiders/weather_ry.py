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
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

website='weather_tianqihoubao_ry'

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
        city_list = [u'营口',u'北京',u'上海',u'广州',u'深圳',u'杭州',u'南京',u'济南',u'天津',u'重庆',u'青岛',u'大连',u'宁波',u'厦门',u'成都',u'武汉',u'哈尔滨',u'沈阳',u'西安',u'长春',u'长沙',u'福州',u'郑州',u'石家庄',u'佛山',u'东莞',u'无锡',u'烟台',u'太原',u'合肥',u'南昌',u'南宁',u'昆明',u'温州',u'淄博',u'唐山']

        dls = response.xpath("//*[@id='content']/div[3]/dl")
        for dl in dls:
            ddas = dl.xpath("dd//a")
            # print(len(ddas))
            for a in ddas:
                city = a.xpath("text()").extract_first().strip()
                # print(city)
                if city in city_list:
                    # print("yes")
                    # city_list.remove(city)
                    city_url = response.urljoin(a.xpath("@href").extract_first())
                    print(city_url)
                    yield scrapy.Request(url=city_url, callback=self.parse_url)
        # print(city_list)
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
