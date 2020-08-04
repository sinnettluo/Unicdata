# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import HangzhouEChong
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

website='hangzhou_echong'

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
        return [scrapy.FormRequest(method="post", url="http://220.191.209.149:8888/asset-server/asset/api/v0.1/charging-stations")]

    def parse(self, response):
        css = json.loads(response.text)
        # print(len(css["queryCountyList"][0]["queryList"]))
        for cs in css["queryCountyList"][0]["queryList"]:
            url = "http://220.191.209.149:8888/asset-server/asset/api/v0.1/charging-stations/%d?mobile=" % cs["stationId"]
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        details = json.loads(response.text)

        item = HangzhouEChong()

        item["grabtime"] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item["url"] = response.url

        item["operId"] = details["operId"] if "operId" in details else "-"
        item["stationNo"] = details["stationNo"] if "stationNo" in details else "-"
        # item["carModelList"] = details["carModelList"] if "carModelList" in details else "-"
        item["remark"] = details["remark"] if "remark" in details else "-"
        item["cityName"] = details["cityName"] if "cityName" in details else "-"
        item["stationId"] = details["stationId"] if "stationId" in details else "-"
        item["operTel"] = details["operTel"] if "operTel" in details else "-"
        item["city"] = details["city"] if "city" in details else "-"
        item["countyName"] = details["countyName"] if "countyName" in details else "-"
        item["busiTime"] = details["busiTime"] if "busiTime" in details else "-"
        item["parkPrice"] = details["parkPrice"] if "parkPrice" in details else "-"
        item["stationName"] = details["stationName"] if "stationName" in details else "-"
        item["freeNums"] = details["freeNums"] if "freeNums" in details else "-"
        item["servicePrice"] = details["servicePrice"] if "servicePrice" in details else "-"
        item["chargePrice"] = details["chargePrice"] if "chargePrice" in details else "-"
        item["lat"] = details["lat"] if "lat" in details else "-"
        item["lon"] = details["lon"] if "lon" in details else "-"
        item["payment"] = details["payment"] if "payment" in details else "-"
        item["storeFlag"] = details["storeFlag"] if "storeFlag" in details else "-"
        item["evaNum"] = details["evaNum"] if "evaNum" in details else "-"
        item["dcNums"] = details["dcNums"] if "dcNums" in details else "-"
        item["evaScore"] = details["evaScore"] if "evaScore" in details else "-"
        item["imgList"] = details["imgList"] if "imgList" in details else "-"
        item["stationAddr"] = details["stationAddr"] if "stationAddr" in details else "-"
        item["county"] = details["county"] if "county" in details else "-"
        item["operName"] = details["operName"] if "operName" in details else "-"
        item["acNums"] = details["acNums"] if "acNums" in details else "-"
        item["acFreeNums"] = details["acFreeNums"] if "acFreeNums" in details else "-"
        item["status"] = str(details["stationId"]) + "-" + str(item["grabtime"]) + "-" + str(details["freeNums"]) + "-" + str(details["acFreeNums"])
        for pile in details["pileList"]:
            item["parkNo"] = pile["parkNo"] if "parkNo" in pile else "-"
            item["gunName"] = pile["gunName"] if "gunName" in pile else "-"
            item["pileNo"] = pile["pileNo"] if "pileNo" in pile else "-"
            item["qrCodes"] = pile["qrCodes"] if "qrCodes" in pile else "-"
            item["powerRating"] = pile["powerRating"] if "powerRating" in pile else "-"
            item["gunSn"] = pile["gunSn"]  if "gunSn" in pile else "-"
            item["gunType"] = pile["gunType"] if "gunType" in pile else "-"
            item["pileName"] = pile["pileName"] if "pileName" in pile else "-"
            item["elecMode"] = pile["elecMode"] if "elecMode" in pile else "-"
            item["currentRated"] = pile["currentRated"] if "currentRated" in pile else "-"
            item["pileId"] = pile["pileId"] if "pileId" in pile else "-"
            item["gunStatus"] = pile["gunStatus"] if "gunStatus" in pile else "-"
            # print(item)
            yield item

