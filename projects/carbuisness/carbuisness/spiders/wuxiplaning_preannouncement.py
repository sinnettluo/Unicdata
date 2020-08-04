# -*- coding: utf-8 -*-
"""
C2017-30
"""
import scrapy
from carbuisness.items import wuxiplaning_preannouncement
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='wuxiplaning_preannouncement'

class CarSpider(scrapy.Spider):

    name=website

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
        urllist=['','_1','_2','_3','_4','_5','_6','_7','_8','_9','_10','_11','_12','_13','_14','_15','_16','_17','_18','_19','_20',]
        for temp in urllist:
            url = "http://gh.wuxi.gov.cn/zfxxgk/gggs/ghgs/csghzdgs/pqgs/index" + temp + ".shtml"
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        x = response.xpath('//div[@class="RightSide_con"]/ul/li')
        for temp in x:
            urlbase = temp.xpath('a/@href').extract_first()
            url="http://gh.wuxi.gov.cn"+str(urlbase)
            yield scrapy.Request(url,callback=self.parse_info)

    def parse_info(self,response):
        item=wuxiplaning_preannouncement()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['posttime']= response.xpath('//div[@class="mainCont"]/p/em/text()').extract_first() \
            if response.xpath('//div[@class="mainCont"]/p/em/text()').extract_first() else "-"
        item['browser']=response.xpath('//span[@id="clickCount"]/text()').extract_first() \
            if response.xpath('//span[@id="clickCount"]/text()').extract_first() else "-"
        item['shortdesc']=response.xpath('//div[@class="mainCont"]/h1/text()').extract_first().strip() \
            if response.xpath('//div[@class="mainCont"]/h1/text()').extract_first() else "-"
        data=response.xpath('//div[@id="Zoom"]/p')
        item['data'] = response.xpath('//div[@id="Zoom"]').extract_first()
        item['land_information']=data[1].xpath('text()').extract_first().strip() \
            if data[1].xpath('text()').extract_first() else "-"
        str1=''
        for temp in data[3:6]:
            str1=str1+"-"+temp.xpath('text()').extract_first()
        item['publicity']=str1
        str1=''
        for temp in data[6:13]:
            str1=str1+"-"+temp.xpath('text()').extract_first()
        item['contact_feedback']=str1
        yield item
