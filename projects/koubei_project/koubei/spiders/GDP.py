# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GDPItem
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
import pymongo

website='gdp'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://data.stats.gov.cn/easyquery.htm?cn=E0102"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=self.settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    #
    # def start_requests(self):
    #
    #     request_list = []
    #
    #     connection = pymongo.MongoClient("192.168.1.94", 27017)
    #     db = connection["newcar"]
    #     collection = db["autohome_newcar"]
    #
    #     result = collection.distinct("autohomeid")
    #     for r in result:
    #         url = "https://carif.api.autohome.com.cn/car/getspecelectricbutie.ashx?_callback=GetSpecElectricSubsidy&speclist=%s&cityid=310100&type=1" % str(r)
    #         request_list.append(scrapy.Request(url, meta={"autohomeid": r}, callback=self.parse))
    #     return request_list


    def parse(self, response):


        provs = {
            "北京市":"110000",
            "天津市": "120000",
            "河北省": "130000",
            "山西省": "140000",
            "内蒙古自治区": "150000",
            "辽宁省": "210000",
            "吉林省": "220000",
            "黑龙江省": "230000",
            "上海市": "310000",
            "江苏省": "320000",
            "浙江省": "330000",
            "安徽省": "340000",
            "福建省": "350000",
            "江西省": "360000",
            "山东省": "370000",
            "河南省": "410000",
            "湖北省": "420000",
            "湖南省": "430000",
            "广东省": "440000",
            "广西壮族自治区": "450000",
            "海南省": "460000",
            "重庆市": "500000",
            "四川省": "510000",
            "贵州省": "520000",
            "云南省": "530000",
            "西藏自治区": "540000",
            "陕西省": "610000",
            "甘肃省": "620000",
            "青海省": "630000",
            "宁夏回族自治区": "640000",
            "新疆维吾尔自治区": "650000",
        }
        # print(response.text)
        # provs = response.xpath("//*[@id='mySelect_reg']/div[2]/div[2]/div[2]/ul/li")
        # print(provs)
        for prov in provs:
            provname = prov
            provid = provs[prov]
            meta = {
                "provname":provname,
                "provid":provid
            }
            headers = {
                "User-agent":"User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsjd&rowcode=zb&colcode=sj&wds=[{"wdcode":"reg","valuecode":"%s"}]&dfwds=[{"wdcode":"sj","valuecode":"LAST18"}]' % str(provid)
            yield scrapy.FormRequest(method="post", url=url, meta=meta, headers=headers, callback=self.parse_details, dont_filter=True)

    def parse_details(self, response):
        res = json.loads(response.text)
        for d in res['returndata']['datanodes'][:18]:
            item = GDPItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['date'] = d['code'].split(".")[-1]
            item['prov'] = response.meta['provname']
            item['gdp'] = d['data']['data']
            item['status'] = d['code']

            print(item)
            # yield item