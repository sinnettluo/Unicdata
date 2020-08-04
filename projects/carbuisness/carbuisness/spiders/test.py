# -*- coding: utf-8 -*-
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
website='Demo'

header = {
    'Connection': 'keep - alive',  # 保持链接状态
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

cookie={}

cookie['PHPSESSID']="k692fpcb6mcu75iivemt07u742"
cookie['uid']="Chn0nFmc88aeGGvvA3l/Ag=="
cookie['15308_7']='true'
cookie['lpaiche:cookie:user_info']="%7B%22uid%22%3A%22106635%22%2C%22user_name%22%3A%22clcw_mz0n_264%22%2C%22dealer_id%22%3A%2215308%22%2C%22mobile%22%3A%2213301679752%22%2C%22uniq_login_token%22%3A%22MDAwMDAwMDAwMK-eoqy0r5arhHZnra91p66zjdGTgnXSqYXQa5uMrceWvHivnrR6r62DnZqrromwob99p5WDeLBnh6yLrJJ6vtGxiKqrs6CrZg%22%7D"

class CarSpider(scrapy.Spider):
    name = website
    start_urls=["http://www.lpaiche.com/HisPrice/index/ajax/1/brand_id/229?p=1"]

    def __init__(self,**kwargs):
        #print "do init"
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=header,
                       cookies=cookie)

    def parse(self, response):
        print response.body

