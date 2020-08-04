# -*- coding: utf-8 -*-
import json
import time
from datetime import date
from hashlib import md5

import scrapy
from scrapy.conf import settings
from scrapy.mail import MailSender

from ..items import che168citys

website = 'che168_city'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che168.com"]

    start_urls=[
        'https://m.che168.com/handler/select/getallprovince.ashx'
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 20000000
        self.counts = 0
        self.today = date.today()

        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #pro_city select
    def parse(self,response):
        # print meta
        data = json.loads(response.xpath('//p/text()').extract_first())[2]['all']
        for info in data:
            for temp in info['item']:
                provname = temp['n']
                provid = temp['id']
                provinfo = {"provname": provname, "provid": provid}
                url = "https://m.che168.com/handler/select/getallcitybyprovinceid.ashx?pid="+provid
                yield scrapy.Request(url, meta={"provdata": provinfo}, callback=self.cityinfo, dont_filter=True)

    def cityinfo(self, response):
        meta = response.meta['provdata']
        # print meta
        data = json.loads(response.xpath('//p/text()').extract_first())['item']
        for info in data:
            item = che168citys()
            item['provname'] = meta['provname']
            item['provid'] = meta['provid']
            item['cityname'] = info['value']
            item['cityid'] = info['id']
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = md5(info['id']).hexdigest()
            yield item