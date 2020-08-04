# -*- coding: utf-8 -*-
"""

C2017-40

"""
import pymongo
import scrapy
from carbuisness.items import AutohomeDetailedPriceItem
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
import MySQLdb
import os
website='autohome_detailed_price'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.autohome.com.cn/beijing/"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     iedriver = "D:\IEDriverServer.exe"
    #     os.environ["webdriver.ie.driver"] = iedriver
    #     self.browser = webdriver.Ie(iedriver)
    #     # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        data = collection.distinct("autohomeid")
        for item in data:
            url = "https://j.autohome.com.cn/pcplatform/common/getChexingDetailInfo"
            yield scrapy.FormRequest(url=url, formdata={"chexingId":item}, callback=self.parse_price, dont_filter=True)

    def parse_price(self, response):
        data = json.loads(response.body)["result"]
        item = AutohomeDetailedPriceItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = str(data["specid"])
        item['brandid'] = data["brandid"]
        item['brandname'] = data["brandname"]
        item['dynamicprice'] = data["dynamicprice"]
        item['fctid'] = data["fctid"]
        item['fctname'] = data["fctname"]
        item['levelid'] = data["levelid"]
        item['levelname'] = data["levelname"]
        item['oilboxvolume'] = data["oilboxvolume"]
        item['seriesid'] = data["seriesid"]
        item['seriesname'] = data["seriesname"]
        item['specdisplacement'] = data["specdisplacement"]
        item['specdrivingmodename'] = data["specdrivingmodename"]
        item['specengineid'] = data["specengineid"]
        item['specenginename'] = data["specenginename"]
        item['specenginepower'] = data["specenginepower"]
        item['specflowmodeid'] = data["specflowmodeid"]
        item['specflowmodename'] = data["specflowmodename"]
        item['specheight'] = data["specheight"]
        item['specid'] = data["specid"]
        item['specisbooked'] = data["specisbooked"]
        item['specisimport'] = data["specisimport"]
        item['specispreferential'] = data["specispreferential"]
        item['specistaxexemption'] = data["specistaxexemption"]
        item['specistaxrelief'] = data["specistaxrelief"]
        item['speclength'] = data["speclength"]
        item['speclogo'] = data["speclogo"]
        item['specmaxprice'] = data["specmaxprice"]
        item['specminprice'] = data["specminprice"]
        item['specname'] = data["specname"]
        item['specoiloffical'] = data["specoiloffical"]
        item['specparamisshow'] = data["specparamisshow"]
        item['specpicount'] = data["specparamisshow"]
        item['specquality'] = data["specquality"]
        item['specstate'] = data["specstate"]
        item['specstructuredoor'] = data["specstructuredoor"]
        item['specstructureseat'] = data["specstructureseat"]
        item['specstructuretypename'] = data["specstructuretypename"]
        item['spectransmission'] = data["spectransmission"]
        item['specweight'] = data["specweight"]
        item['specwidth'] = data["specwidth"]
        yield item