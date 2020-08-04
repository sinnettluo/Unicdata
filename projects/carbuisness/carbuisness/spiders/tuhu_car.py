# -*- coding: utf-8 -*-
"""
taskid=C2017-08

"""
import scrapy
from carbuisness.items import tuhucaritem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='tuhu_car'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['https://www.tuhu.cn/sitemap/shops']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        print "do parse"
        x = response.xpath('//ul[@class="map_linklist cf"]/li')
        for temp in x:
            url=temp.xpath('a/@href').extract_first()
            yield scrapy.Request(url,callback=self.parse_middle1)

    def parse_middle1(self,response):
        print "do parse_middle1"
        x = response.xpath('//div[@class="non-list"]/div')
        for temp in x:
            url=temp.xpath('div/a/@href').extract_first()
            yield scrapy.Request(url,callback=self.parse_car)

    def parse_car(self,response):
        print "do parse_car"
        item = tuhucaritem()
        item['website'] = website
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        temp=response.xpath('//script[contains(text(),"Tuhu.Map.init")]/text()')
        item['shopname']=temp.re('Name: \'(.*)\'')[0]
        item['shop_hours']=response.xpath(u'//p[contains(text(),"营业时间：")]/../p/span/text()').extract_first() \
            if response.xpath(u'//p[contains(text(),"营业时间：")]/../p/span/text()').extract_first() else "-"
        item['shoptype']=response.xpath('//span[@class="shop-type"]/text()').extract_first() \
            if response.xpath('//span[@class="shop-type"]/text()').extract_first() else "-"
        item['phone']=response.xpath(u'//p[contains(text(),"服务电话：")]/../p[4]/span/text()').extract_first() \
            if response.xpath(u'//p[contains(text(),"服务电话：")]/../p[4]/span/text()').extract_first() else "-"
        item['location']=response.xpath('//div[@class="address clearfix"]/div[@id="submitbtns"]/span/text()').extract_first() \
            if response.xpath('//div[@class="address clearfix"]/div[@id="submitbtns"]/span/text()').extract_first() else "-"
        item['province']=temp.re('Province = \'(.*)\'')[0]
        item['city']=temp.re('City = \'(.*)\'')[0]
        item['shopid']=temp.re('PKID: \'(.*)\'')[0]
        item['commentscore']=response.xpath(u'//h2[contains(text(),"综合评价：")]/../h2/span/text()').extract_first() \
            if response.xpath(u'//h2[contains(text(),"综合评价：")]/../h2/span/text()').extract_first() else "-"
        x = response.xpath('//div[@class="shop-info"]/p[3]/span')
        str=""
        for temp in x:
            base=temp.xpath('text()').extract_first()
            str=base+" "+str
        item['paytype']=str
        star = response.xpath('//div[@class="star-level"]/div')
        item['skillstar']=star[0].xpath('span/i/@style').extract_first()
        item['servicestar']=star[1].xpath('span/i/@style').extract_first()
        item['envirstar']=star[2].xpath('span/i/@style').extract_first()
        yield item



