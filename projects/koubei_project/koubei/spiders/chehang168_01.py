# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Chehang168Item
import time
# from scrapy.conf import settings
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
import random
import redis

website='chehang168_new'

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
            "soucheAnalytics_usertag" : "WjKeC56Vpf",
            "DEVICE_ID" : "1156331fbfb00c34d8cc46f39cb5716c",
        "_uab_collina"  : "155531505872406790895702",
        "U"  : "1495168_8ad4212494c76c922d965f13636a8a83",
        }
        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')
        self.r =redis.Redis(host=self.settings["REDIS_SERVER"],port=self.settings["REDIS_PORT"],db=0)
    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        # try:
        #     with open("/root/familyname_log.txt", "r") as f:
        #         res = f.readlines()
        #         f.close()
        # except Exception as e:
        #     pass
        cookie = self.r.get("che168").decode("utf-8")
        headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",

        }
        cookie={i.split("=")[0].strip(""):i.split("=")[1].strip("")for i in cookie.split(";")}
        return [scrapy.Request(url="http://www.chehang168.com/index.php?c=index&m=carData", headers=headers,cookies=cookie)]

    def parse(self, response):
        print(response.request.headers)
        #
        # res = ""
        #
        # try:
        #     with open("familyname_log.txt", "r") as f:
        #         res = f.read()
        #         f.close()
        # except Exception as e:
        #     pass

        # family_list = res.split("\n")
        print(response.text)
        # logging.log(msg=str(family_list), level=logging.INFO)
        res = json.loads(response.text.replace("var carData = ", ""))
        # book = csv.reader(open("chehang168_0418.csv", "r", encoding="utf-8"))
        # with open("./chehang168_0418.txt","r",encoding="utf-8")as f:
        #     book=f.readlines()
        # book = list(book)
        # # random.shuffle(book)
        book =['??????', '??????', '??????', '??????', '??????eRX5', '??????RX5', '????????????', '????????????', '????????????', '???', '???', '???', 'POLO', '??????', '??????', '??????L', '??????L?????????', '??????RAV4', '?????????', '?????????', '???????????????', '?????????', '??????', '??????310', '??????530', '??????630', '??????730', '??????1???', '??????3???', '??????5???', '??????X1', '??????X3', '?????????', '??????CR-V', '?????????', '??????', '??????UR-V', '??????', '?????????', '??????', '??????', '??????', '??????', '??????', '???MAX?????????', '?????????S7', '?????????S6', '?????????M6', '?????????G6', '?????????F0', '??????', '??????A???', '??????C???', '??????E???', '??????GLA', '??????GLC', 'VELITE 5', '?????????', '?????????', '??????GL6', '??????GL8', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '?????????', '??????', '??????', '??????', '??????', '??????CC', '??????', '??????', '?????????', '??????', '??????', '?????????', '??????', '??????', '??????', 'V5??????', '??????DX3', '??????DX7', '??????DX3?????????', '??????A5??????', '??????????????????', '????????????T-Cross', '??????', 'T-ROC??????', '?????????????????', '??????', 'LANNIA??????', '??????', '??????', '??????', '??????', '??????', '??????????????', '??????', '??????', '??????A3', '??????A4L', '??????A6L', '??????A6L?????????', '??????Q2L', '??????Q3', '??????Q5', '??????Q5L', 'VELITE 6', '????????????ATS-L', '????????????CT6', '????????????XT4', '????????????XT5', '????????????XTS', '??????', '?????????', '?????????', '?????????', '?????????', '??????RV', '?????????', '?????????XL', '??????', '?????????', '?????????', '??????350', '??????360', '??????550', '??????950', '??????e950', '??????Ei5', '??????ei6', '??????i5', '??????i6', '??????MARVEL X', '??????RX3', '??????RX8', '?????????e1', '?????????e5', '?????????e6', '?????????F3', '?????????G5', '???MAX', '???', '????????EV10', '??????EX5', '??????ES8', 'MODEL 3', 'MODEL S', 'MODEL X', 'EC??????', 'EU??????', 'EV??????', 'EX??????', '???????????????EX3', '???????????????EX5', '??????S01', 'INSPIRE', '??????XR-V', 'YARiS L ??????', '??????', '??????', '?????????', '??????C-HR', '?????????', '?????????', '?????????', '?????????', '??????', '??????', '?????????', '??????', '??????', '??????', '????????????ix35', '??????ix25', '?????????CX-4', '?????????CX-5', '?????????MU-X', '??????H9', '??????', '?????????', '??????FS', '???????????????', '??????']
        for row in book:
            if book.index(row) < 64:

                for brand in res:
                    for brandid in res[brand]["brand"]:
                        brandcode = brandid
                        brandname = res[brand]["brand"][brandid]["name"]
                        for familyid in res[brand]["brand"][brandid]["pserise"]:
                            familycode = familyid
                            familyidname = res[brand]["brand"][brandid]["pserise"][familyid]["name"]
                            # if row[0] == familyidname:
                                # if familyidname not in family_list:
                            # if familyidname in ["??????", "??????", "??????", "??????", "??????eRX5", "??????RX5", "????????????", "????????????", "????????????", "???", "???", "???", "POLO", "??????", "??????", "??????L", "??????L?????????"]:
                            meta = {
                                "brandcode":brandcode,
                                "brandname":brandname,
                                "familycode":familycode,
                                "familyname":familyidname,
                                "count":1,
                            }
                            url = "http://www.chehang168.com/index.php?c=index&m=series&psid=%s" % (familycode.replace("'",""))
                            logging.log(msg=str(url), level=logging.INFO)
                            yield scrapy.Request(url=url, meta=meta, cookies=self.cookies, callback=self.parse_list)

    def parse_list(self, response):
        print(1)
        # print(response.text)
        # next = response.xpath("//a[contains(text(), '?????????')]")
        # if next and response.meta["count"] < 2:
        #     response.meta["count"] = response.meta["count"] + 1
        #     yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), meta=response.meta, callback=self.parse_list)

        cars = response.xpath("//*[@class='ch_carlistv3']/li")
        if cars:
            with open("familyname_log.txt", "a") as f:
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
            item['price'] = car.xpath("div/span/b/text()").extract_first().replace("???", "")
            item['store'] = car.xpath("p[@class='c3']/a/text()").extract_first()

            item['desc1'] = car.xpath("p[@class='c1']/text()[1]").extract_first()
            item['desc2'] = car.xpath("p[@class='c2']/text()").extract_first()
            item['time'] = car.xpath("p[@class='c3']/cite[1]/text()").extract_first()
            item['desc3_2'] = car.xpath("p[@class='c3']/cite[2]/text()").extract_first()
            item['desc3_3'] = car.xpath("p[@class='c3']/cite[3]/text()").extract_first()
            item['status'] = item["title"] + "-" + item["desc1"] + "-" + item["store"]

            print(item)
            # yield item
