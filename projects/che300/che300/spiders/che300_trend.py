# -*- coding: utf-8 -*-
"""
C2017-41

"""
from ..items import che300TrendItem
import scrapy
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
import csv
website='che300_trend'

class CarSpider(scrapy.Spider):
    name=website
    # start_urls=['http://bochewang.com.cn/AuctioningCar/Index/?t=636396123452239556']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=2000000
        self.dbname = 'usedcar_evaluation'
        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','usedcar_evaluation',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        # connection = pymongo.MongoClient("192.168.1.94", 27017)
        # db = connection["usedcar_evaluation"]
        # collection = db["che300_price_daily"]
        # result = collection.find()

        with open('blm/'+self.dbname+'/che300_price_daily.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]

        # for item in modellist:
        #     print(item)
        for doc in modellist:
            # print(doc)
            data = doc['regDate'].split("-")
            month = data[1]
            year = data[0]
            price = doc['price6']
            model = doc['salesdescid']

            url = "https://dingjia.che300.com/demo/evaluate/getPriceTrend?model=%s&prov=3&ts=1531965106701&device_crypt_sign=ADC0107A87C5C8DD&app_type=android_price&app_channel=leshangdian&device_id=android_1c2af4ff-5917-3577-95f1-9132a5d00dd0&mch_type=che300_pro&type=dealer_price&version=1.9.1.0&city=3&price=%s&app_from=che300_pro&month=%s&mile=0.1&longitude=121.504304&year=%s&latitude=31.286698" % (model, price, month, year)
            yield scrapy.Request(url, meta={
                "month":month,
                "year":year,
                "price":price,
                "model":model
            })

    def parse(self,response):
        obj = json.loads(response.body)
        item = che300TrendItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['date201807'] = obj['data'][0]['eval_price']
        item['date201810'] = obj['data'][1]['eval_price']
        item['date201901'] = obj['data'][2]['eval_price']
        item['date201904'] = obj['data'][3]['eval_price']
        item['date201907'] = obj['data'][4]['eval_price']
        item['date201910'] = obj['data'][5]['eval_price']
        item['month'] = response.meta['month']
        item['year'] = response.meta['year']
        item['price'] = response.meta['price']
        item['model'] = response.meta['model']
        yield item

