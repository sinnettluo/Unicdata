# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import LianlianItem
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
from urllib import quote
import csv

website='lianlian_c'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        # "https://www.evchargeonline.com/site/index",
        # "https://www.evchargeonline.com/site/station/list?operatorIds=&equipmentTypes=&payChannels=&isNewNantionalStandard=-1&isOpenToPublic=-1&isParkingFree=-1&longitude=121.50447&latitude=31.28671"
    ]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        with open("/home/python/scrapyd/blm/SH_xy.csv") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[0] != "x":
                    tm = int(round(time.time() * 1000))
                    url = "https://www.evchargeonline.com/site/station/list?timestamp=%d&pageNo=3&stationName=&operatorIds=&equipmentTypes=&payChannels=&isNewNantionalStandard=-1&isOpenToPublic=-1&isParkingFree=-1&longitude=%s&latitude=%s&radius=10000" % (
                    tm, line[0], line[1])
                    yield scrapy.Request(url=url, meta={"lng":line[0], "lat":line[1]})

    def parse(self, response):
        data = json.loads(json.loads(response.body))
        for station in data["data"]["stations"]:
            item = LianlianItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['url'] = response.url
            item['status2'] = station["stationId"] + "-" + response.url if station.has_key("payment") else "-"
            item['payment'] = station["payment"] if station.has_key("payment") else "-"
            item['operatorLogo'] = station["operatorLogo"] if station.has_key("operatorLogo") else "-"
            item['operatorId'] = station["operatorId"] if station.has_key("operatorId") else "-"
            item['operatorName'] = station["operatorName"] if station.has_key("operatorName") else "-"
            item['stationId'] = station["stationId"] if station.has_key("stationId") else "-"
            item['stationName'] = station["stationName"] if station.has_key("stationName") else "-"
            item['electricityFee'] = station["electricityFee"] if station.has_key("electricityFee") else "-"
            item['distance'] = station["distance"] if station.has_key("distance") else "-"
            item['directTotal'] = station["directTotal"] if station.has_key("directTotal") else "-"
            item['directAvaliable'] = station["directAvaliable"] if station.has_key("directAvaliable") else "-"
            item['alternatingTotal'] = station["alternatingTotal"] if station.has_key("alternatingTotal") else "-"
            item['alternatingAvaliable'] = station["alternatingAvaliable"] if station.has_key("alternatingAvaliable") else "-"
            item['parkFee'] = station["parkFee"] if station.has_key("parkFee") else "-"
            item['serviceFee'] = station["serviceFee"] if station.has_key("serviceFee") else "-"
            item['stationLng'] = station["stationLng"] if station.has_key("stationLng") else "-"
            item['stationLat'] = station["stationLat"] if station.has_key("stationLat") else "-"
            item['stationLngBD'] = station["stationLngBD"] if station.has_key("stationLngBD") else "-"
            item['stationLatBD'] = station["stationLatBD"] if station.has_key("stationLatBD") else "-"
            item['stationType'] = station["stationType"] if station.has_key("stationType") else "-"
            item['address'] = station["address"] if station.has_key("address") else "-"
            item['pictures'] = station["pictures"] if station.has_key("pictures") else "-"
            item['sitePicUrl'] = station["sitePicUrl"] if station.has_key("sitePicUrl") else "-"
            item['status'] = item["grabtime"] + "-" + str(item["stationId"]) + "-" + response.url + "-" + str(item['directAvaliable']) + "-" + str(item['alternatingAvaliable'])
            yield item
