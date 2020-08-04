# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeMinMaxPriceItem
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
import MySQLdb
import pymongo

website='autohome_min_max_price'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.autohome.com.cn/beijing/"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')



    def parse(self, response):

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        result = collection.find({})

        mysqldb = MySQLdb.connect("192.168.2.120", "root", "ABCabc123", "peoplez", port=3306)
        dbc = mysqldb.cursor()
        mysqldb.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select distinct(provid) from che168_city_cityid"
        dbc.execute(sql)
        res = dbc.fetchall()

        for row in res:
            # print(row[0])
            for r in result:
                url = "https://www.che168.com/handler/cardetail_v3/GetMinMaxPrice.ashx?sid=%s&pid=%s" % (r["autohomeid"],row[0])
                # print(url)
                yield scrapy.Request(url, meta={"provid":row[0], "autohomeid":r["autohomeid"]}, callback=self.parse_info)



    def parse_info(self, response):
        if response.body != '""':
            price_obj = json.loads(response.body)
            item = AutohomeMinMaxPriceItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + time.strftime('%Y-%m', time.localtime())
            item['autohomeid'] = response.meta['autohomeid']
            item['provid'] = response.meta['provid']
            item['minsellingprice'] = price_obj["message"]["minsellingprice"]
            item['maxsellingprice'] = price_obj["message"]["maxsellingprice"]
            item['minselledprice'] = price_obj["message"]["minselledprice"]
            item['maxselledprice'] = price_obj["message"]["maxselledprice"]
            yield item

