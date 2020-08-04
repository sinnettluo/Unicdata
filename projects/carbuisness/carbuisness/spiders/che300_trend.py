# -*- coding: utf-8 -*-
"""
C2017-41

"""
import scrapy
from carbuisness.items import BochewangCarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import pymongo

website='che300_trend'

class CarSpider(scrapy.Spider):
    name=website
    # start_urls=['http://bochewang.com.cn/AuctioningCar/Index/?t=636396123452239556']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["usedcar_evaluation"]
        collection = db["che300_price_daily"]
        result = collection.find()
        for doc in result:
            print(doc)
            data = doc['regDate'].split("-")
            month = data[1]
            year = data[0]
            url = ""

    def parse(self,response):
        pass

