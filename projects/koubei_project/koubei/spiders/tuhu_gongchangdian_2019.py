# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import TuhuGongchengdianItem
import time
# from scrapy.conf import self.self.settings
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
# from scrapy.conf import self.settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
import pymongo

website='tuhu_gongchangdian_2019_fix3'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_self.settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=self.settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):

        with open("blm/tuhu_cities.json", "r", encoding="utf-8")  as f:
            json_str = f.read()
            f.close()

        cities = json.loads(json_str)
        urls_list = list()
        for letter in cities["Area"]:
            for city in cities["Area"][letter]:
                url = "https://api.tuhu.cn/Shops/SelectShopList?LngBegin=&pids=&serviceType=0&IsMatchRegion=0&city=%s&pageIndex=1&LatBegin=&isOpenLive=false&vehicleId=&district=&sort=HuShi&shopClassification=&Province=%s" % (city["City"], city["Province"])
                meta = {
                    "city": city["City"],
                    "province": city["Province"],
                }
                urls_list.append(scrapy.Request(url=url, meta=meta, callback=self.parse))
        return urls_list


    def parse(self, response):
        res = json.loads(response.text)

        if res["TotalPage"] > 1:
            for i in range(1, res["TotalPage"]+1):
                url = "https://api.tuhu.cn/Shops/SelectShopList?LngBegin=&pids=&serviceType=0&IsMatchRegion=0&city=%s&pageIndex=%d&LatBegin=&isOpenLive=false&vehicleId=&district=&sort=HuShi&shopClassification=&Province=%s" % (response.meta["city"], i, response.meta["province"])
                meta = {
                    "city": response.meta["city"],
                    "province": response.meta["province"],
                }
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_details, dont_filter=True)


    def parse_details(self, response):
        res = json.loads(response.text)

        for shop in res["Shops"]:
            item = TuhuGongchengdianItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = response.url + "-" + str(shop["ShopId"])
            item["name"] = shop["CarparName"]
            item["city"] = shop["City"]
            item["province"] = shop["Province"]
            item["address"] = shop["Address"]
            item["LngBegin"] = shop["LngBegin"]
            item["LatBegin"] = shop["LatBegin"]
            item["spec"] = shop["ShopClassification"]
            item["brand"] = shop["Brand"]
            item["shopType"] = shop["ShopType"]
            # print(item)
            yield item
