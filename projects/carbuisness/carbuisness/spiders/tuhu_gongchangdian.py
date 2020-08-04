# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import TuhuGongchengdianItem
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
import xlrd



website='tuhu_gongchangdian_2019'
# city_name = '邢台市'r_store
page_num = 10

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.tuhu.cn/shops/shanghai1.aspx",
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    # def start_requests(self):
    #     file = xlrd.open_workbook(u"D:/city_copy.xlsx")
    #
    #     sheet = file.sheet_by_name("city_copy")
    #
    #     cols_city_name = sheet.col_values(1)
    #     print(cols_city_name)
    #     for city_name in cols_city_name:
    #         for i in range(page_num):
    #             url = "http://api.map.baidu.com/place/v2/search?query=途虎养车工厂店&region=%s&page_num=%d&output=json&ak=0nIp0ZxAyuSbIloGzSqZMK006GALOZMo" % (city_name, i)
    #             yield scrapy.Request(url=url, meta={"city_name":city_name})

    def parse(self, response):
        lis = response.xpath("//*[@class='tab-content active']/li")
        for li in lis:
            url = "https://www.tuhu.cn/Shop/Map.aspx?callback=__ShopMap__&province=%s" % li.xpath("@data-name").extract_first()
            yield scrapy.Request(url=url, callback=self.parse_details, dont_filter=True)
        for li in ["西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区", "内蒙古自治区", "广西壮族自治区", "上海市"]:
            yield scrapy.Request(url="https://www.tuhu.cn/Shop/Map.aspx?callback=__ShopMap__&province=%s" % li, callback=self.parse_details)

    def parse_details(self, response):
        shops = json.loads(response.body.replace("__ShopMap__(", "").replace("}]})", "}]}").strip())
        for shop in shops["shops"]:
            print(shop)
            item = TuhuGongchengdianItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = response.url + "-" + str(shop["PKID"])
            item["name"] = shop["Name"]
            item["city"] = shop["City"]
            item["province"] = shop["Province"]
            item["address"] = shop["Address"]
            item["position"] = shop["Position"]

            yield item