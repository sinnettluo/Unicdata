# -*- coding: utf-8 -*-
import scrapy
from ..items import che300_price
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import json
import datetime

website = 'che300_city'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]

    start_urls=[
        'https://dingjia.che300.com/api/lib/util/city/prov_with_city'
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 500
        self.counts = 0
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #pro_city select
    #brandselect
    def parse(self, response):

        data = response.xpath('//p/text()').extract_first()
        t = re.findall(r'\{\"prov_name.*?\}\]\}',data)
        for i in range(len(t)):
            p = json.loads(t[i])
            provid = p['prov_id']
            provname = p['prov_name']
            da = p['data']
            # print da
            for j in da:
                cityname = j['city_name']
                cityid = j['city_id']
                citycode = j['city_code']
                procity = {'provid':provid, 'provname':provname ,'cityid':cityid, 'cityname':cityname}
                item = che300_price()
                item['provname'] = procity['provname']
                item['provid'] = procity['provid']
                item['cityname'] = procity['cityname']
                item['cityid'] = procity['cityid']
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['status'] = md5(response.url+"-"+procity['provid']+"-"+procity['cityid']).hexdigest()
                yield item