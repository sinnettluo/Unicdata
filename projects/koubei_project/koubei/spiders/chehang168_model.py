# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Chehang168Item
import time
from scrapy.mail import MailSender
import logging
import json
import re
import csv
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

website='chehang168_model'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.cookies = {
            'DEVICE_ID':"211cc798d8a161bcefe8dc8a1b419c8cx",
            '_uab_collina':"155928081037335702062646",
            'soucheAnalytics_usertag':"IResWvVuea",
            'U':"1372402_3fe9f4d25278ce1bfa74b10b88d6852a"
        }
        self.headers = {
            'User-agent':"User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            # 'cookies':"DEVICE_ID=b06867da7fb0e5b1ad9fc0706be5bfb0; _uab_collina=155895052515172990847746; soucheAnalytics_usertag=1FqQfTRrN5; U=1364406_3d27cd75fb80b2f7b8c59d3da38b3cd8"
        }
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')



    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):

        return [scrapy.Request(url="http://www.chehang168.com/index.php?c=index&m=carData", cookies=self.cookies, headers=self.headers)]

    def parse(self, response):

        res = ""

        try:
            with open("/root/familyname_log_full.txt", "r") as f:
            # with open("D:\chehang168_family_log", "r") as f:
                res = f.read()
                f.close()
        except Exception as e:
            pass

        family_list = res.split("\n")
        print(family_list )

        res = json.loads(response.text.replace("var carData = ", ""))

        # book = csv.reader(open("D:\chehang168_0418.csv", "r", encoding="utf-8"))
        # for row in book:

        # print(response.text.replace("var carData = ", ""))

        for brand in res:
            for brandid in res[brand]["brand"]:
                brandcode = brandid
                brandname = res[brand]["brand"][brandid]["name"]
                for familyid in res[brand]["brand"][brandid]["pserise"]:
                    familycode = familyid
                    familyidname = res[brand]["brand"][brandid]["pserise"][familyid]["name"]
                    # if row[0] == familyidname:
                    if familyidname not in family_list:
                        meta = {
                            "brandcode": brandcode,
                            "brandname": brandname,
                            "familycode": familycode,
                            "familyname": familyidname,
                        }
                        # cookies = {
                        #     'DEVICE_ID': "1156331fbfb00c34d8cc46f39cb5716c",
                        #     '_uab_collina': "155738838172118614916745",
                        #     'soucheAnalytics_usertag': "1Te61e5TMN",
                        #     'U': "1121010_b949e4ef634edbd6feec73c6bbdc7b12"
                        # }
                        url = "http://www.chehang168.com/index.php?c=index&m=series&psid=%s" % (familycode.replace("'",""))
                        yield scrapy.Request(url=url, meta=meta, cookies=self.cookies, headers=self.headers, callback=self.parse_list)

    def parse_list(self, response):
        # print(response.text)
        # next = response.xpath("//a[contains(text(), '下一页')]")
        # if next:
        #     yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), meta=response.meta, callback=self.parse_list)

        cars = response.xpath("//*[@class='ch_carlistv3']/li")
        if cars:
            # with open("D:\chehang168_family_log", "a") as f:
            with open("/root/familyname_log_full.txt", "a") as f:
                f.write(response.meta["familyname"] + "\n")
            f.close()
        for car in cars:
            item = Chehang168Item()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['brandname'] = response.meta["brandname"]
            item['brandcode'] = response.meta["brandcode"]
            item['familyname'] = response.meta["familyname"]
            item['familycode'] = response.meta["familycode"]
            item['title'] = car.xpath("div/h3/a/text()").extract_first()
            item['guideprice'] = car.xpath("div/h3/b/text()").extract_first()
            item['price'] = car.xpath("div/span/b/text()").extract_first().replace("万", "")
            item['store'] = car.xpath("p[@class='c3']/a/text()").extract_first()

            item['desc1'] = car.xpath("p[@class='c1']/text()[1]").extract_first()
            item['desc2'] = car.xpath("p[@class='c2']/text()").extract_first()
            item['time'] = car.xpath("p[@class='c3']/cite[1]/text()").extract_first()
            item['desc3_2'] = car.xpath("p[@class='c3']/cite[2]/text()").extract_first()
            item['desc3_3'] = car.xpath("p[@class='c3']/cite[3]/text()").extract_first()
            item['status'] = item["title"] + "-" + item["desc1"] + "-" + item["store"]

            # print(item)
            yield item
