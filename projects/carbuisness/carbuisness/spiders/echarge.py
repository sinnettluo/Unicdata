# -*- coding: utf-8 -*-
"""

C2017-40

"""
import codecs
import scrapy
from carbuisness.items import EChargeItem
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

website='echarge_c'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

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

    def start_requests(self):
        temp = ""
        with open("/home/echargenet.txt", "r") as f:
            for line in f.readlines():
                temp = temp + line
            f.close()
        data = json.loads(temp)
        print(len(data))
        for charge in data:
            url = "https://ecmyapp.echargenet.com/portal/charge-total/rest/plug/api/plugInfo?isGs=%d&id=%s" % (charge["isGs"], charge["id"])
            yield scrapy.Request(url=url, meta=charge)

        temp = ""
        with open("/home/echargenet_third.txt", "r") as f:
            for line in f.readlines():
                temp = temp + line
            f.close()
        data = json.loads(temp)
        print(len(data))
        for charge in data:
            url = "https://ecmyapp.echargenet.com/portal/charge-total/rest/plug/api/plugInfo?isGs=%d&id=%s" % (
            charge["isGs"], charge["id"])
            yield scrapy.Request(url=url, meta=charge)

    def parse(self, response):
        data = json.loads(response.body)
        item = EChargeItem()
        item["address"] = response.meta["address"],
        item["areaName"] = response.meta["areaName"]
        item["city"] = response.meta["city"]
        item["company"] = response.meta["company"]
        item["connectorType"] = response.meta["connectorType"],
        item["currentType"] = response.meta["currentType"],
        item["freeNum"] = response.meta["freeNum"],
        item["id"] = response.meta["id"]
        item["images"] = response.meta["images"],
        item["isGs"] = response.meta["isGs"],
        item["lat"] = response.meta["lat"],
        item["link"] = response.meta["link"],
        item["lng"] = response.meta["lng"],
        item["mapIcon"] = response.meta["mapIcon"]
        item["maxOutPower"] = response.meta["maxOutPower"],
        item["operatorTypes"] = response.meta["operatorTypes"]
        item["payType"] = response.meta["payType"]
        item["phone"] = response.meta["phone"]
        item["plugType"] = response.meta["plugType"],
        item["priceRational"] = response.meta["priceRational"],
        item["province"] = response.meta["province"]
        item["quantity"] = response.meta["quantity"],
        item["score"] = response.meta["score"],
        item["serviceCode"] = response.meta["serviceCode"],
        item["standard"] = response.meta["standard"],
        item["statuss"] = response.meta["status"],
        item["supportOrder"] = response.meta["supportOrder"]
        item["businessTime"] = data["data"]["businessTime"]
        item["electricizePrice"] = data["data"]["electricizePrice"]
        item["quantity"] = data["data"]["quantity"]
        item["parks"] = data["data"]["parks"]
        item["operatorInfos"] = data["data"]["operatorInfos"]
        item["name"] = data["data"]["name"]
        item["priceParking"] = data["data"]["priceParking"]
        item["favorite"] = data["data"]["favorite"]
        item["chargerTypeNum"] = data["data"]["chargerTypeNum"]
        item["chargerTypeStatusDes"] = data["data"]["chargerTypeStatusDes"]
        item["supportCharge"] = data["data"]["supportCharge"]
        item["servicedesc"] = data["data"]["servicedesc"]
        item["plugnotice"] = data["data"]["plugnotice"]
        item["marketingImage"] = data["data"]["marketingImage"]
        item["images"] = data["data"]["images"]
        item["payTypeDesc"] = data["data"]["payTypeDesc"]
        item["numOfComments"] = data["data"]["numOfComments"]
        item["totalFreeChargerNum"] = data["data"]["totalFreeChargerNum"]
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['status'] = response.url + "-" + item["grabtime"] + "-" + str(item['chargerTypeStatusDes']["01"]) + "-" + str(item['chargerTypeStatusDes']["02"])

        yield item