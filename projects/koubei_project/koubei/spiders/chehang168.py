# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Chehang168Item
import time
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
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

website = 'chehang168'


class CarSpider(scrapy.Spider):
    name = website
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 800000

        self.DEVICE_ID = "08b3e7995356e97d8f61dc171048c05a"
        self._uab_collina = "156698635367094109337198"
        self.soucheAnalytics_usertag = "WDuGdR0f7I"
        self.U = "1497797_d51aecb5183ede2691a53a97a963906c"
        self.UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

        self.cookies = {
            'DEVICE_ID': '{}'.format(self.DEVICE_ID),
            '_uab_collina': '{}'.format(self._uab_collina),
            'soucheAnalytics_usertag': '{}'.format(self.soucheAnalytics_usertag),
            'U': '{}'.format(self.U),
        }

        self.headers = {
            'User-agent': "{}".format(self.UserAgent),
            'cookies': "DEVICE_ID={}; _uab_collina={}; soucheAnalytics_usertag={}; U={}".format(self.DEVICE_ID, self._uab_collina, self.soucheAnalytics_usertag, self.U)
        }
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        logging.log(level=logging.INFO, msg=json.dumps(self.cookies))
        url = "http://www.chehang168.com/index.php?c=index&m=carData"
        return [scrapy.Request(url=url, cookies=self.cookies,
                               headers=self.headers)]

    def parse(self, response):

        res = ""

        try:

            with open("/root/familyname_log_full.txt", "r") as f:
            # with open("/Users/cagey/PycharmProjects/zt_scrapy/projects/koubei_project/koubei/familyname_log_full.txt", "r") as f:
                # with open("D:\chehang168_family_log", "r") as f:
                res = f.read()
                f.close()
        except Exception as e:
            pass

        family_list = res.split("\n")
        print(family_list)

        logging.log(level=logging.INFO, msg=response.text)
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
                        url = "http://www.chehang168.com/index.php?c=index&m=series&psid=%s" % (
                            familycode.replace("'", ""))
                        print(url)
                        print("*"*100)
                        yield scrapy.Request(url=url, meta=meta, cookies=self.cookies, headers=self.headers,
                                             callback=self.parse_list)

    def parse_list(self, response):
        # print(response.text)
        # next = response.xpath("//a[contains(text(), '下一页')]")
        # if next:
        #     yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), meta=response.meta, callback=self.parse_list)

        cars = response.xpath("//*[@class='ch_carlistv3']/li")
        if cars:
            # with open("D:\chehang168_family_log", "a") as f:
            # with open("/root/familyname_log_full.txt", "a") as f:
            with open("/Users/cagey/PycharmProjects/zt_scrapy/projects/koubei_project/koubei/familyname_log_full.txt", "a") as f:
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

            print(item)
            # yield item
