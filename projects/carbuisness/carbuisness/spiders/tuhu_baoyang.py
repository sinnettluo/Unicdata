# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import TuhuBaoyangItem
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

website='tuhu_baoyang_test'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://item.tuhu.cn/Car/GetCarBrands2?callback=__GetCarBrands__"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for i in range(65,91):
            try:
                brandList = res[unichr(i)]
            except Exception as e:
                print(e)
                continue
            for brand in brandList:
                brandStr = brand["Brand"].replace(" ", "+")
                url = "https://item.tuhu.cn/Car/SelOneBrand?callback=__GetCarBrands__&Brand=%s" % brandStr
                meta = {"brand":brandStr}
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)


    def parse_family(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for family in res["OneBrand"]:
            url = "https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID=%s" % family["ProductID"]
            meta = dict({"familyID":family["ProductID"], "familyName":family["CarName"]}, **response.meta)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_pailiang)

    def parse_pailiang(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for pailiang in res["PaiLiang"]:
            url = "https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID=%s&PaiLiang=%s" % (pailiang["Key"], pailiang["Value"])
            meta = dict({"pailiang":pailiang["Value"]}, **response.meta)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_year)

    def parse_year(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for year in res["Nian"]:
            url = ""
            meta = dict({"nian": year["Value"]}, **response.meta)
            # yield scrapy.Request(url=url, meta=meta, headers={"referer": "https://by.tuhu.cn/baoyang/", "cookie": "_um_deti=036e903a44f54d77aeb255c3a3554b360"}, callback=self.parse_change_product)
            yield scrapy.Request(url=url, callback=self.parse_what)

    def parse_what(self, response):
        pass



    # def parse_change_product(self, response):
    #     res = json.loads(response.body)
    #     for Category in res:
    #         for items in Category["Items"]:
    #             for products in items["Items"]:
    #                 try:
    #                     for product in products["Products"]:
    #                         item = TuhuBaoyangItem()
    #                         item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
    #                         item["url"] = response.url
    #                         item['status'] = response.url + "-" + Category["CategoryType"] + "-" + items["PackageType"] + "-" + products["BaoYangType"] + "-" + str(product["Product"]["Oid"])
    #                         item['brand'] = response.meta["brand"]
    #                         item['family'] = response.meta["familyName"]
    #                         item['familyID'] = response.meta["familyID"]
    #                         item['pailiang'] = response.meta["pailiang"]
    #                         item['nian'] = response.meta["nian"]
    #                         item['type'] = Category["CategoryType"]
    #                         item['subType'] = items["PackageType"]
    #                         item['productType'] = products["BaoYangType"]
    #                         item['product'] = product["Product"]["DisplayName"]
    #                         item['productID'] = product["Product"]["ProductId"]
    #                         item['price'] = product["Product"]["Price"]
    #                         item['count'] = product["Count"]
    #                         item['typeName'] = Category["CategoryName"]
    #                         item['subTypeName'] = items["ZhName"]
    #                         item['productTypeName'] = products["ZhName"]
    #                         # yield item
    #                 except Exception as e:
    #                     print(response.body)
    #                     print(products)
    #                     return

    def parse_change_product(self, response):
        res = json.loads(response.body)
        for Category in res:
            for items in Category["Items"]:
                for products in items["Items"]:
                    try:
                        for product in products["Products"]:
                            item = TuhuBaoyangItem()
                            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                            item["url"] = response.url
                            item['status'] = response.url + "-" + Category["CategoryType"] + "-" + items["PackageType"] + "-" + products["BaoYangType"] + "-" + str(product["Product"]["Oid"]) + "-" + response.meta["brand"] + "-" + response.meta["familyName"] + "-" + response.meta["pailiang"] + "-" + response.meta["nian"]
                            item['brand'] = response.meta["brand"]
                            item['family'] = response.meta["familyName"]
                            item['familyID'] = response.meta["familyID"]
                            item['pailiang'] = response.meta["pailiang"]
                            item['nian'] = response.meta["nian"]
                            item['type'] = Category["CategoryType"]
                            item['subType'] = items["PackageType"]
                            item['productType'] = products["BaoYangType"]
                            item['product'] = product["Product"]["DisplayName"]
                            item['productID'] = product["Product"]["ProductId"]
                            item['price'] = product["Product"]["Price"]
                            item['count'] = product["Count"]
                            item['typeName'] = Category["CategoryName"]
                            item['subTypeName'] = items["ZhName"]
                            item['productTypeName'] = products["ZhName"]
                            # print(item)
                            yield item
                    except Exception as e:
                        print(e)
                        print(response.body)
                        print(products)
                        return
