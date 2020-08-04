# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import ChunChengELuXingItem
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

website='chuncheng_eluxing'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["https://appapiv2.kmcharge.com/station/sitestatus"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

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


    # def start_requests(self):
    #     return [scrapy.FormRequest(method="post", url="http://220.191.209.149:8888/asset-server/asset/api/v0.1/charging-stations")]

    def parse(self, response):
        sites = json.loads(response.text)
        for s in sites["data"]["lists"]:
            url = "https://appapiv2.kmcharge.com/station/batchinfo?ids=%s" % s["site_id"]
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        json_obj = json.loads(response.text)
        item = ChunChengELuXingItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        item["url"] = response.url
        item["station_id"] = json_obj["data"]["list"][0]["station_id"]
        item["title"] = json_obj["data"]["list"][0]["title"]
        item["carrier_id"] = json_obj["data"]["list"][0]["carrier_id"]
        item["carrier_icon"] = json_obj["data"]["list"][0]["carrier_icon"]
        item["total_num"] = json_obj["data"]["list"][0]["total_num"]
        item["fast_available"] = json_obj["data"]["list"][0]["fast_available"]
        item["slow_available"] = json_obj["data"]["list"][0]["slow_available"]
        item["open_time"] = json_obj["data"]["list"][0]["open_time"]
        item["longitude"] = json_obj["data"]["list"][0]["geo"]["longitude"]
        item["latitude"] = json_obj["data"]["list"][0]["geo"]["latitude"]
        item["type"] = json_obj["data"]["list"][0]["type"]
        item["remark"] = json_obj["data"]["list"][0]["remark"]
        item["op_state"] = json_obj["data"]["list"][0]["op_state"]
        item["is_network"] = json_obj["data"]["list"][0]["is_network"]
        item["score"] = json_obj["data"]["list"][0]["score"]
        item["is_ground"] = json_obj["data"]["list"][0]["is_ground"]
        item["quick_num"] = json_obj["data"]["list"][0]["quick_num"]
        item["slow_num"] = json_obj["data"]["list"][0]["slow_num"]
        item["park_free"] = json_obj["data"]["list"][0]["park_free"]
        item["park_expense"] = json_obj["data"]["list"][0]["park_expense"]
        item["pay_model"] = json_obj["data"]["list"][0]["pay_model"]
        item["pay_model_desc"] = json_obj["data"]["list"][0]["pay_model_desc"]
        item["elect_price"] = json_obj["data"]["list"][0]["elect_price"]
        item["service_price"] = json_obj["data"]["list"][0]["service_price"]
        item["time_elect"] = json_obj["data"]["list"][0]["time_elect"]
        item["status"] = response.url + "-" + time.strftime('%Y-%m-%d %H:%M', time.localtime()) + "-" + str(item["fast_available"]) + "-" + str(item["slow_available"])
        # print(item)
        yield item