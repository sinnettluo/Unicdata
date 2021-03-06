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
            "?????????":"110000",
            "?????????": "120000",
            "?????????": "130000",
            "?????????": "140000",
            "??????????????????": "150000",
            "?????????": "210000",
            "?????????": "220000",
            "????????????": "230000",
            "?????????": "310000",
            "?????????": "320000",
            "?????????": "330000",
            "?????????": "340000",
            "?????????": "350000",
            "?????????": "360000",
            "?????????": "370000",
            "?????????": "410000",
            "?????????": "420000",
            "?????????": "430000",
            "?????????": "440000",
            "?????????????????????": "450000",
            "?????????": "460000",
            "?????????": "500000",
            "?????????": "510000",
            "?????????": "520000",
            "?????????": "530000",
            "???????????????": "540000",
            "?????????": "610000",
            "?????????": "620000",
            "?????????": "630000",
            "?????????????????????": "640000",
            "????????????????????????": "650000",
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