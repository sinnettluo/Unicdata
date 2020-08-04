# -*- coding: utf-8 -*-
"""
C2017-41
bochewang 博车网

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

website='2017_prov_gdp'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['https://www.sohu.com/a/219596742_683734']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        ps = response.xpath("//*[@id='mp-editor']/p")[5:]

