# -*- coding: utf-8 -*-
import scrapy
from ..items import che300
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from hashlib import md5
import re
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import csv

website = 'che300_vehile_info'
spidername_new = 'che300_vehile_info_new'
spidername_update = 'che300_vehile_info_update'
#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]
    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider, self).__init__(*args, **kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 20000000
        self.dbname = 'usedcar_evaluation'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'
        self.part=int(part)
        self.parts=int(parts)

    def start_requests(self):
        with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        cars = []
        for model in modellist:
            i = model['salesdescid']
            url = 'https://www.che300.com/mi_' + str(i)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url=url, meta={"datainfo": {"salesdescid":i}}, callback=self.parse)

    def parse(self, response):
        dffile(self.fa, response.url, self.tag)
        item = che300()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['id'] = re.findall(r'\d+',response.url)[1]
        item['salesdesc'] = response.xpath('//div[@class="main-wrap clearfix"]/h1/text()').extract_first().replace(u" - \u5168\u90e8\u53c2\u6570","")
        item['datasave'] = response.xpath('//div[@class="main-wrap clearfix"]').extract_first()
        item['status'] = md5(response.url).hexdigest()
        item = dict(response.meta['datainfo'],**item)
        yield item

# new
class CarSpider_new(CarSpider):

    # basesetting
    name = spidername_new

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")
        self.part = int(part)
        self.parts = int(parts)

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        self.part = int(part)
        self.parts = int(parts)
        #do
        super(update, self).start_requests()