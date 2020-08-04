# -*- coding: utf-8 -*-
"""
C2017-41
bochewang 博车网

"""
import scrapy
from carbuisness.items import ChezhiwangRankItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import calendar

website='chezhiwang_report'

class CarSpider(scrapy.Spider):
    name=website
    # start_urls=['http://www.12365auto.com/carowners/index.shtml']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        for i in range(1, 11):
            url = "http://www.12365auto.com/carowners/index.shtml?attv=%d" % i
            yield scrapy.Request(url=url, meta={"attv":i})

    def parse(self,response):
        dls = response.xpath("//*[@class='dc_b_wxc_b']/dl")
        for dl in dls:
            score = dl.xpath("/dd/ul/li[2]/span/text()").extract_first()
            url = dl.xpath("/dd/ul/li[1]/a/@href").extract_first().replace("\.shtml", "-all\.shtml")
            yield scrapy.Request(url=url, callback=self.parse_final, meta={"score":score})

    def parse_final(self, response):
        pass

