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
import requests

website='chijia_fixed_2019_add_location'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.tyreplus.com.cn/Find_tyreplus_store/"
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
        provs = response.xpath("//*[@id='province']/option")[1:]
        for prov in provs:
            provCode = prov.xpath("@value").extract_first()
            provName = prov.xpath("text()").extract_first()
            url = "http://www.tyreplus.com.cn/Find_tyreplus_store/city.html?province=%s" % provCode
            yield scrapy.Request(url=url, meta={"provCode": provCode, "provName": provName}, callback=self.parse_city)

    def parse_city(self, response):
        citys = json.loads(response.body)
        for city in citys:
            provCode = response.meta["provCode"]
            cityCode = city['id']
            cityName = city['name']
            url = "http://www.tyreplus.com.cn/Find_tyreplus_store/index.html?province=%s&city=%s" % (provCode, cityCode)
            yield scrapy.Request(url=url, meta={"provCode": provCode, "provName": response.meta["provName"], "cityCode": cityCode, "cityName": cityName}, callback=self.parse_list)

    def parse_list(self, response):
        store_list = response.xpath("//*[@id='ulsearch']/li")
        for store in store_list:
            item = CheXiangJiaItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(store_list.index(store))
            item['storeName'] = store.xpath("div/span/text()[1]").extract_first()
            item['address'] = store.xpath("div/p/text()[1]").extract_first()
            item['telephone']  = store.xpath("div/p/text()[2]").extract_first()
            item['areaCode'] = response.meta["cityCode"]
            item['areaName'] = response.meta["cityName"]
            item['provinceId'] = response.meta["provCode"]
            item['provinceName'] = response.meta["provName"]
            # print(item)
            yield item
            # url = store.xpath("div/a[2]/@href").extract_first()
            # print(url)
            # yield scrapy.Request(url=response.urljoin(url), meta=response.meta, callback=self.parse_detail)

    # def parse_detail(self, response):
    #     item = CheXiangJiaItem()
    #     item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    #     item['url'] = response.url
    #     item['status'] = response.url
    #     strongs = response.xpath("//*[@class='search2in']/p[1]/strong")
    #     for strong in strongs:
    #         label = strong.xpath("text()").extract_first()
    #         if label == u"地址：":
    #             item['address'] = response.xpath("//*[@class='search2in']/p[1]/text()[%d]" % (strongs.index(strong)*2+1)).extract_first()
    #         if label == u"行车指南：":
    #             item['intro'] = response.xpath("//*[@class='search2in']/p[1]/text()[%d]" % (strongs.index(strong)*2+1)).extract_first()
    #         if label == u"工作时间：":
    #             item['businesstime'] = response.xpath("//*[@class='search2in']/p[1]/text()[%d]" % (strongs.index(strong)*2+1)).extract_first()
    #         if label == u"电话：":
    #             item['telephone'] = response.xpath("//*[@class='search2in']/p[1]/text()[%d]" % (strongs.index(strong)*2+1)).extract_first()
    #     item['storeName'] = response.xpath("//*[@class='search2in']/span[1]/text()").extract_first()
    #     item['storeId'] = response.xpath("//*[@class='search2in']/span[1]/a[1]/@href").re("\(\'(.*?)\'\)")[0]
    #     baidu_api_url = "http://api.map.baidu.com/place/v2/search?query=%s&region=%s&output=json&ak=0nIp0ZxAyuSbIloGzSqZMK006GALOZMo" % (item['address'], response.meta["provName"])
    #     print(baidu_api_url)
    #     res = requests.request("get",baidu_api_url)
    #     baidu_api_obj = json.loads(res.text)
    #     try:
    #         item['localX'] = baidu_api_obj['results'][0]['location']['lat']
    #     except:
    #         item['localX'] = "-"
    #     try:
    #         item['localY'] = baidu_api_obj['results'][0]['location']['lng']
    #     except:
    #         item['localY'] = '-'
    #
    #     print(item['localX'])
    #     print(item['localY'])
    #     item['image1'] = response.xpath("//*[@id='banner_list']/a[1]/img[1]/@src").extract_first()
    #     item['areaCode'] = response.meta["cityCode"]
    #     item['areaName'] = response.meta["cityName"]
    #     item['provinceId'] = response.meta["provCode"]
    #     item['provinceName'] = response.meta["provName"]
    #     item['cityId'] = response.meta["cityCode"]
    #     service1 = response.xpath("//*[@class='service1']/ul[1]/li")
    #     service1_list = []
    #     for li in service1:
    #         service1_list.append(li.xpath("a[1]/text()").extract_first())
    #     item['serviceScopeMap'] = "|".join(service1_list)
    #     service2 = response.xpath("//*[@class='service2']/ul[1]/li")
    #     service2_list = []
    #     for li in service2:
    #         service1_list.append(li.xpath("text()").extract_first())
    #     item['stationTypeMap'] = "|".join(service2_list)
    #     item['score'] = response.xpath("//*[@class='search2in']/p[1]/img[1]/@alt").re(u"店面综合评价(.*?)分")[0]
    #     # print(item)
    #     yield item


