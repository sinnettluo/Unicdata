# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import DealerRXItem
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
import csv

website='dealer_rx2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

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


    def start_requests(self):
        # csvf = csv.reader(open("D:/dealer_rx.csv", "r"))
        urls = []
        with open("D:/dealer_rx.txt", "r") as f:
            text = f.readlines()
            f.close()

        for row in text:
            meta = {
                "familyid":row.strip()
            }
            url = "https://dealer.autohome.com.cn/handler/other/getdata?__action=dealerlq.getdealerlistseries&provinceId=0&cityId=0&countyId=0&seriesId="+str(row.strip())+"&orderType=0&pageIndex=1&kindId=1&isNeedMaintainNews=1&pageSize=20&isCPL=1"
            r = scrapy.Request(url=url, meta=meta)
            urls.append(r)
        return urls


    def parse(self, response):

        res = json.loads(response.text)
        res = res["result"]

        if res["pageindex"] < res["pagecount"]:
            meta = {
                "familyid":response.meta["familyid"]
            }
            yield scrapy.Request(url=response.url.replace("pageIndex=%d" % res["pageindex"], "pageIndex=%d" % (res["pageindex"] + 1)), meta=meta)


        for dealer in res["list"]:
            item = DealerRXItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = str(dealer["dealerId"]) + "-" + str(response.meta["familyid"])
            item['familyid'] = response.meta["familyid"]
            item['storename'] = dealer["dealerInfoBaseOut"]["companySimple"]
            item['address'] = dealer["dealerInfoBaseOut"]["address"]

            # print(item)
            yield item




