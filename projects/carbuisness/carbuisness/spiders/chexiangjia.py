# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import CheXiangJiaItem
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

website='chexiangjia_2019'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://jia.chexiang.com/t/stores.htm"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        citylist = response.xpath("//*[@class='city-name']")
        for city in citylist:
            code = city.xpath("@areacode").extract_first()
            # print(code)
            yield scrapy.FormRequest(url="http://jia.chexiang.com/store/list_PC.htm", formdata={"areaCode":code}, dont_filter=True, callback=self.parse_json)
            # yield scrapy.Request(url="http://jia.chexiang.com/store/list_PC.htm", meta={"areaCode":code}, dont_filter=True, callback=self.parse_json)

    def parse_json(self, response):
        stations = json.loads(response.body)
        for station in stations["obj"]:
            item = CheXiangJiaItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = station['storeId']
            item['storeName'] = station['storeName']
            item['intro'] = station['intro']
            item['address'] = station['address']
            item['telephone'] = station['telephone']
            item['mobile'] = station['mobile']
            item['businesstime'] = station['businesstime']
            item['storeId'] = station['storeId']
            item['storeNo'] = station['storeNo']
            item['localX'] = station['localX']
            item['localY'] = station['localY']
            item['image1'] = station['image1']
            item['baiduCityCode'] = station['baiduCityCode']
            item['areaCode'] = station['areaCode']
            item['areaName'] = station['areaName']
            item['provinceId'] = station['provinceId']
            item['provinceName'] = station['provinceName']
            item['cityId'] = station['cityId']
            item['storeName'] = station['storeName']
            item['distId'] = station['distId']
            item['distName'] = station['distName']
            item['storeType'] = station['storeType']
            item['storeScore'] = station['storeScore']
            item['isChat'] = station['isChat']
            item['isAppointment'] = station['isAppointment']
            item['businessTimeType'] = station['businessTimeType']
            item['workBusinessTime'] = station['workBusinessTime']
            item['weekendBusinessTime'] = station['weekendBusinessTime']
            item['holidayName'] = station['holidayName']
            item['holidayBusinessTime'] = station['holidayBusinessTime']
            item['holidayStartDate'] = station['holidayStartDate']
            item['holidayEndDate'] = station['holidayEndDate']
            item['appointmentWashCar'] = station['appointmentWashCar']
            item['appointmentBeauty'] = station['appointmentBeauty']
            item['appointmentMaintain'] = station['appointmentMaintain']
            item['cityNamePrefix'] = station['cityNamePrefix']
            item['partnerId'] = station['partnerId']
            item['partnerCode'] = station['partnerCode']
            item['outCode'] = station['outCode']
            item['storeStatus'] = station['storeStatus']
            item['storeOwner'] = station['storeOwner']
            item['openStoreTime'] = station['openStoreTime']
            item['ownerType'] = station['ownerType']
            item['manHourPrice'] = station['manHourPrice']
            item['stationTypeMap'] = station['stationTypeMap']
            item['serviceScopeMap'] = station['serviceScopeMap']
            item['operationCode'] = station['operationCode']
            item['bankName'] = station['bankName']
            item['bankAccount'] = station['bankAccount']
            item['ownerTypeName'] = station['ownerTypeName']
            item['storeStatusName'] = station['storeStatusName']
            item['defaultCity'] = station['defaultCity']
            item['additionServiceScopeMap'] = station['additionServiceScopeMap']

            # print(item)
            yield item