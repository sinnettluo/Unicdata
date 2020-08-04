# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomePriceInTaxItem
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

website='autohome_price_in_tax'

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

        result = collection.distinct("autohomeid")

        # mysqldb = MySQLdb.connect("192.168.2.120", "root", "ABCabc123", "peoplez", port=3306)
        # dbc = mysqldb.cursor()
        # mysqldb.set_character_set('utf8')
        # dbc.execute('SET NAMES utf8;')
        # dbc.execute('SET CHARACTER SET utf8;')
        # dbc.execute('SET character_set_connection=utf8;')
        #
        # sql = "select distinct(provid) from che168_city_cityid"
        # dbc.execute(sql)
        # res = dbc.fetchall()

        # for row in res:
            # print(row[0])
        for r in result:
            # print(r)
            url = "https://apiassess.che168.com/api/NewCarPriceInTax.ashx?_appid=2sc&specid=%s" % (r)
            # print(url)
            yield scrapy.Request(url, meta={"autohomeid":r}, callback=self.parse_info)

    def parse_info(self, response):
        if response.body != '""':
            item = AutohomePriceInTaxItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['autohomeid'] = response.meta['autohomeid']
            try:
                item['price_in_tax'] = re.findall("newcarprice\"\:(.*?)\}", response.body)[0]
            except:
                item['price_in_tax'] = "error"

            item['status'] = response.url + str(item['price_in_tax'])
            yield item

