# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Weixiudian_yangchewuyou
import time
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
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
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
import pymongo

website='weixiudian_yangchewuyou'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=310100&ad=310100&mc=false&type=1&keyword=&OrderBy=2&_=1556184153445',
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=110100&ad=110100&mc=false&type=1&keyword=&OrderBy=2&_=1556184650127',
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=510100&ad=510100&mc=false&type=1&keyword=&OrderBy=2&_=1556184816865',
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=320500&ad=320500&mc=false&type=1&keyword=&OrderBy=2&_=1556184855689',
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=130100&ad=130100&mc=false&type=1&keyword=&OrderBy=2&_=1556184974126',
        'http://p.yangche51.com/Handlers/Station/GetStationListForMap.ashx?cd=350500&ad=350500&mc=false&type=1&keyword=&OrderBy=2&_=1556185111684',
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','koubei',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    # def start_requests(self):
    #
    #     request_list = []
    #
    #     connection = pymongo.MongoClient("192.168.1.94", 27017)
    #     db = connection["newcar"]
    #     collection = db["autohome_newcar"]
    #
    #     result = collection.distinct("autohomeid")
    #     for r in result:
    #         url = "https://carif.api.autohome.com.cn/car/getspecelectricbutie.ashx?_callback=GetSpecElectricSubsidy&speclist=%s&cityid=310100&type=1" % str(r)
    #         request_list.append(scrapy.Request(url, meta={"autohomeid": r}, callback=self.parse))
    #     return request_list


    def parse(self, response):

        obj = json.loads(response.text)
        for dian in obj:
            item = Weixiudian_yangchewuyou()

            item['url'] = response.url
            item['status'] = str(dian["ID"])
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['id'] = dian["ID"]
            item['address'] = dian["Address"]
            item['sn'] = dian["SN"]
            item['dn'] = dian["SN"]

            # print(item)
            yield item