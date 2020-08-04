# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import EchongwangItem
import time
# from scrapy.conf import settings
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
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests

website='echongwang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.type = {
            "http://www.ndrc.gov.cn/zcfb/zcfbl/": "发展改革委令",
            "http://www.ndrc.gov.cn/zcfb/gfxwj/": "规范性文件",
            "http://www.ndrc.gov.cn/zcfb/zcfbgg/": "公告",
            "http://www.ndrc.gov.cn/zcfb/zcfbghwb/": "规划文本",
            "http://www.ndrc.gov.cn/zcfb/zcfbtz/": "通知",
            "http://www.ndrc.gov.cn/zcfb/jd/": "解读",
            "http://www.ndrc.gov.cn/zcfb/zcfbqt/": "其他",
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        posts = []
        # tm = int(round(time.time() * 1000))
        # yield scrapy.Request("https://www.evchargeonline.com/site/station/list?timestamp="+str(tm)+"&pageNo=3&stationName=&operatorIds=&equipmentTypes=&payChannels=&isNewNantionalStandard=-1&isOpenToPublic=-1&isParkingFree=-1&longitude=121.021804&latitude=30.874093&radius=10000")
        # return [scrapy.FormRequest(method="post", url="http://220.191.209.149:8888/asset-server/asset/api/v0.1/charging-stations")]
        for i in range(1, 20000):
            data = {
                "site_id":str(i)
            }
            posts.append(scrapy.FormRequest(method="post", url='https://mina.zc3u.com/mina/site/detail', formdata=data))
        return posts



    def parse(self, response):
        obj = json.loads(response.text)
        item = EchongwangItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item['url'] = response.url
        item['status'] = obj['data']['station_id']
        item['data'] = response.text
        yield item
        # data = json.loads(json.loads(response.text))
        # for station in data["data"]["stations"]:
        #     item = LianlianItem()
        #     item['grabtime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        #     item['url'] = response.url
        #     item['status2'] = station["stationId"] + "-" + response.url if "stationId" in station else "-"
        #     item['payment'] = station["payment"] if "payment" in station else "-"
        #     item['operatorLogo'] = station["operatorLogo"] if "operatorLogo" in station else "-"
        #     item['operatorId'] = station["operatorId"] if "operatorId" in station else "-"
        #     item['operatorName'] = station["operatorName"] if "operatorName" in station else "-"
        #     item['stationId'] = station["stationId"] if "stationId" in station else "-"
        #     item['stationName'] = station["stationName"] if "stationName" in station else "-"
        #     item['electricityFee'] = station["electricityFee"] if "electricityFee" in station else "-"
        #     item['distance'] = station["distance"] if "distance" in station else "-"
        #     item['directTotal'] = station["directTotal"] if "directTotal" in station else "-"
        #     item['directAvaliable'] = station["directAvaliable"] if "directAvaliable" in station else "-"
        #     item['alternatingTotal'] = station["alternatingTotal"] if "alternatingTotal" in station else "-"
        #     item['alternatingAvaliable'] = station["alternatingAvaliable"] if "alternatingAvaliable" in station else "-"
        #     item['parkFee'] = station["parkFee"] if "parkFee" in station else "-"
        #     item['serviceFee'] = station["serviceFee"] if "serviceFee" in station else "-"
        #     item['stationLng'] = station["stationLng"] if "stationLng" in station else "-"
        #     item['stationLat'] = station["stationLat"] if "stationLat" in station else "-"
        #     item['stationLngBD'] = station["stationLngBD"] if "stationLngBD" in station else "-"
        #     item['stationLatBD'] = station["stationLatBD"] if "stationLatBD" in station else "-"
        #     item['stationType'] = station["stationType"] if "stationType" in station else "-"
        #     item['address'] = station["address"] if "address" in station else "-"
        #     item['pictures'] = station["pictures"] if "pictures" in station else "-"
        #     item['sitePicUrl'] = station["sitePicUrl"] if "sitePicUrl" in station else "-"
        #     item['status'] = item["grabtime"] + "-" + str(item["stationId"]) + "-" + response.url + "-" + str(item['directAvaliable']) + "-" + str(item['alternatingAvaliable'])
        #     yield item


