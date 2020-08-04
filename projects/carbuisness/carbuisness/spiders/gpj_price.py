# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import GpjPriceItem
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
from carbuisness.items import ZupukItem
from lxml import etree
import pymongo
import MySQLdb

website='gpj_price_new'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://bj.gongpingjia.com/api/city-group-by-alphabet/"]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000
        self.city_count = 0
        self.headers = {
            "app-version": "C 3.9.17",
            "User-Agent": "EquityPrice/3.9.17",
        }
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','residual_value',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    # def start_requests(self):
    #     yield scrapy.FormRequest(url="http://common.jingzhengu.com/carStyle/getMakesPanelHtml", formdata={"hasAppraise":"true", "hasNewCar":"true", "hasElec":"true"})

    def parse(self, response):

        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'people_zb', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select cityname from jingzhengu_city"
        dbc.execute(sql)
        res = dbc.fetchall()
        dbc.close()
        mysqlconnection.close()

        citylist = []
        for row in res:
            citylist.append(row[0])

        cities = json.loads(response.text)
        final_city_list = {}
        for letter in ["a","b","c","d","e","f","g","h","j","k","l","m","n","p","q","r","s","t","w","x","y","z"]:
            for city in cities["cities"][letter]:
                if city["name"] in citylist:
                    final_city_list[city["slug"]] = city["name"]

        self.city_count += len(final_city_list)
        print(self.city_count)


        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["residual_value"]
        collection = db["gpj_modellist2"]

        res = collection.find()
        for city in {"sh":u"上海"}:
        # for city in final_city_list:
            for r in res:
                if r["max_reg_year"] == "2019":
                    r["max_reg_year"] = "2018"
                for year in range(int(r["min_reg_year"]), int(r["max_reg_year"])+1):
                    month = str(time.strftime('%m', time.localtime()))
                    mile = 2 * (int(time.strftime('%Y', time.localtime())) - year)
                    model_detail = r["detail_model_slug"]
                    brand = r["brandcode"]
                    model = r["familycode"]
                    meta = {
                        "month":month,
                        "mile": mile,
                        "model_detail": model_detail,
                        "brand": brand,
                        "model": model,
                        "city": city,
                        "year": year,
                    }
                    url = u"http://api8.gongpingjia.com/mobile/eval/sell-price/?mile=%d&month=%s&model_detail=%s&brand=%s&city=%s&year=%d&model=%s" % (mile, month, model_detail, brand, final_city_list[city], year, model)
                    yield scrapy.Request(url=url, meta=meta, headers=self.headers,  callback=self.parse_detail)

    def parse_detail(self, response):
        data = json.loads(response.text)
        item = GpjPriceItem()

        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["month"] = response.meta["month"]
        item["mile"] = response.meta["mile"]
        item["model_detail"] = response.meta["model_detail"]
        item["brand"] = response.meta["brand"]
        item["model"] = response.meta["model"]
        item["city"] = response.meta["city"]
        item["year"] = response.meta["year"]
        item["sell_good"] = data["data"]["eval_prices"]["sell"]["good"]
        item["sell_fair"] = data["data"]["eval_prices"]["sell"]["fair"]
        item["sell_excellent"] = data["data"]["eval_prices"]["sell"]["excellent"]
        item["private_good"] = data["data"]["eval_prices"]["private"]["good"]
        item["private_fair"] = data["data"]["eval_prices"]["private"]["fair"]
        item["private_excellent"] = data["data"]["eval_prices"]["private"]["excellent"]
        if "replace" in data["data"]["eval_prices"]:
            item["replace_good"] = data["data"]["eval_prices"]["replace"]["good"]
            item["replace_fair"] = data["data"]["eval_prices"]["replace"]["fair"]
            item["replace_excellent"] = data["data"]["eval_prices"]["replace"]["excellent"]
        if "buy" in data["data"]["eval_prices"]:
            item["buy_good"] = data["data"]["eval_prices"]["buy"]["good"]
            item["buy_fair"] = data["data"]["eval_prices"]["buy"]["fair"]
            item["buy_excellent"] = data["data"]["eval_prices"]["buy"]["excellent"]

        item["model_detail_zh"] = data["data"]["model_detail_info"]["model_detail_zh"]
        item["price_bn"] = data["data"]["model_detail_info"]["price_bn"]
        item["emission_standard"] = data["data"]["model_detail_info"]["emission_standard"]
        item["status"] = str(item["year"]) + "-" + str(item["month"]) + "-" + str(item["mile"]) + "-" + item["model_detail"] + "-" + \
                         item["model"] + "-" + item["brand"] + "-" + item["city"] + "-" + time.strftime('%Y-%m', time.localtime())


        item["good1"] = data["data"]["eval_price_ranges"]["good"][0]
        item["good2"] = data["data"]["eval_price_ranges"]["good"][1]
        item["good3"] = data["data"]["eval_price_ranges"]["good"][2]
        item["good4"] = data["data"]["eval_price_ranges"]["good"][3]

        item["fair1"] = data["data"]["eval_price_ranges"]["fair"][0]
        item["fair2"] = data["data"]["eval_price_ranges"]["fair"][1]
        item["fair3"] = data["data"]["eval_price_ranges"]["fair"][2]
        item["fair4"] = data["data"]["eval_price_ranges"]["fair"][3]

        item["excellent1"] = data["data"]["eval_price_ranges"]["excellent"][0]
        item["excellent2"] = data["data"]["eval_price_ranges"]["excellent"][1]
        item["excellent3"] = data["data"]["eval_price_ranges"]["excellent"][2]
        item["excellent4"] = data["data"]["eval_price_ranges"]["excellent"][3]


        # print(item)
        yield item