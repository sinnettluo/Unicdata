# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import AllLocationItem
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

website='alllocation2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://lbs.amap.com"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000
        self.provinces = {
            u"澳门特别行政区": 820000,
            u"北京市":110000,
            u"重庆市":500000,
            u"福建省":350000,
            u"广东省":440000,
            u"广西壮族自治区":450000,
            u"海南省":460000,
            u"贵州省":520000,
            u"山西省":140000,
            u"台湾省":710000,
            u"甘肃省":620000,
            u"上海市":310000,
            u"安徽省":340000,
            u"河南省":410000,
            u"河北省":130000,
            u"湖北省":420000,
            u"湖南省":430000,
            u"黑龙江省":230000,
            u"江苏省":320000,
            u"江西省":360000,
            u"吉林省":220000,
            u"辽宁省":210000,
            u"宁夏回族自治区":640000,
            u"内蒙古自治区":150000,
            u"山东省":370000,
            u"青海省":630000,
            u"陕西省":610000,
            u"天津市":120000,
            u"香港特别行政区":810000,
            u"四川省":510000,
            u"西藏自治区":540000,
            u"新疆维吾尔自治区":650000,
            u"云南省":530000,
            u"浙江省":330000,
        }
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB',' carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):

        for province in self.provinces:
            url = "https://restapi.amap.com/v3/config/district?subdistrict=1&extensions=all&key=160cab8ad6c50752175d76e61ef92c50&s=rsv3&output=json&level=province&keywords=%d" % self.provinces[province]
            # if province in [u"澳门特别行政区", u"香港特别行政区"]:
            #     yield scrapy.Request(url=url, meta={"province_name":province, "province_id":self.provinces[province], "city_name": "-", "city_id": "-"}, callback=self.parse_district)
            yield scrapy.Request(url=url, meta={"province_name":province, "province_id":self.provinces[province]}, callback=self.parse_city)

    def parse_city(self, response):
        json_data = json.loads(response.body)
        item = AllLocationItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item["province_name"] = json_data["districts"][0]["name"]
        item["province_id"] = json_data["districts"][0]["adcode"]
        item["center"] = json_data["districts"][0]["center"]
        item["polyline"] = json_data["districts"][0]["polyline"]
        item["level"] = json_data["districts"][0]["level"]
        yield item

        sublists = json_data["districts"][0]["districts"]
        for city in sublists:
            url = "https://restapi.amap.com/v3/config/district?subdistrict=1&extensions=all&key=160cab8ad6c50752175d76e61ef92c50&s=rsv3&output=json&level=%s&keywords=%s" % (
                city["level"], city["adcode"])
            if city["level"] == "city":
                meta_dict = {"city_name":city["name"], "city_id":city["adcode"]}
                yield scrapy.Request(url=url, meta=dict(meta_dict, **response.meta), callback=self.parse_district)
            if city["level"] == "district":
                meta_dict = {"city_name": "-", "city_id": "-", "district_name":city["name"], "district_id":city["adcode"]}
                yield scrapy.Request(url=url, meta=dict(meta_dict, **response.meta), callback=self.parse_street)

    def parse_district(self, response):
        json_data = json.loads(response.body)
        item = AllLocationItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item["province_name"] = response.meta["province_name"]
        item["province_id"] = response.meta["province_id"]
        item["center"] = json_data["districts"][0]["center"]
        item["polyline"] = json_data["districts"][0]["polyline"]
        item["level"] = json_data["districts"][0]["level"]
        item["city_name"] = json_data["districts"][0]["name"]
        item["city_id"] = json_data["districts"][0]["adcode"]
        item["citycode"] = json_data["districts"][0]["citycode"]
        yield item

        sublists = json_data["districts"][0]["districts"]
        for district in sublists:
            url = "https://restapi.amap.com/v3/config/district?subdistrict=1&extensions=all&key=160cab8ad6c50752175d76e61ef92c50&s=rsv3&output=json&level=%s&keywords=%s" % (
                district["level"], district["adcode"])
            if district["level"] == "district":
                meta_dict = {"district_name": district["name"], "district_id": district["adcode"]}
                yield scrapy.Request(url=url, meta=dict(meta_dict, **response.meta), callback=self.parse_street)

    def parse_street(self, response):
        json_data = json.loads(response.body)
        item = AllLocationItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item["province_name"] = response.meta["province_name"]
        item["province_id"] = response.meta["province_id"]
        item["center"] = json_data["districts"][0]["center"]
        item["polyline"] = json_data["districts"][0]["polyline"]
        item["level"] = json_data["districts"][0]["level"]
        item["city_name"] = response.meta["city_name"]
        item["city_id"] = response.meta["city_id"]
        item["district_name"] = json_data["districts"][0]["name"]
        item["district_id"] = json_data["districts"][0]["adcode"]
        item["citycode"] = json_data["districts"][0]["citycode"]
        yield item

        sublists = json_data["districts"][0]["districts"]
        for street in sublists:
            item = AllLocationItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = response.url + "-" + str(sublists.index(street))
            item["province_name"] = response.meta["province_name"]
            item["province_id"] = response.meta["province_id"]
            item["center"] = street["center"]
            item["level"] = street["level"]
            item["city_name"] = response.meta["city_name"]
            item["city_id"] = response.meta["city_id"]
            item["district_name"] = response.meta["district_name"]
            item["district_id"] = response.meta["district_id"]
            item["street_name"] = street["name"]
            item["citycode"] = street["citycode"]
            yield item