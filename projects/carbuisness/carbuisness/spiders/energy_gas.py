# -*- coding: utf-8 -*-
"""

C2017-24

"""
import scrapy
from carbuisness.items import GasEnergyItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='energy_gas'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://energy.cngold.org/jyzwd.htm']

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        #print "do parse"
        companys = response.xpath('//div[@class="net-content"]/ul/li')
        for company in companys:
            url = company.xpath('a/@href').extract_first()
            company = company.xpath('div/a[1]/text()').extract_first()
            metadata = {"company" : company}
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)

    def parse_middle1(self, response):
        #print "do parse_middle1"
        metadata = response.meta['metadata']
        areas = response.xpath('//div[@class="w730m w730m02 country-panel mt10"]//dl[@class="clearfix"]/dd')
        for area in areas:
            provincebase = area.xpath('a/text()').extract_first()
            province = re.findall(u"(.*?)加油站", provincebase)[0]
            url = area.xpath('a/@href').extract_first()
            addmeta = {"province":province}
            metadata = dict(metadata, **addmeta)
            #print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)

    def parse_middle2(self, response):
        #print "do parse_middle2"
        metadata = response.meta['metadata']
        areas = response.xpath(u'//div[@class="net-content-part2"]//a[contains(text(),"查看更多")]')
        for area in areas:
            url = area.xpath('../a/@href').extract_first()
            #print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle3, dont_filter=True)

    def parse_middle3(self, response):
        #print "do parse_middle3"
        metadata = response.meta['metadata']
        gaslist = response.xpath(u'//ul[@class="clearfix"]//a[contains(text(),"查看更多")]/../div')
        for gas in gaslist:
            url = gas.xpath('a/@href').extract_first()
            #print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_info, dont_filter=True)
        next_page = response.xpath('//a[contains(text(),"下一页")]')
        if next_page:
            next = next_page.xpath('@href').extract_first()
            yield scrapy.Request(next, meta={"metadata":metadata}, callback=self.parse_middle3, dont_filter=True)

    def parse_info(self, response):
        #print "parse_info"
        item = GasEnergyItem()
        metadata = response.meta['metadata']

        item['stationname'] = response.xpath('//div[@class="w730m w730m02 detail-panel company-panel"]//h3/a/text()').extract_first()

        item['parentfirm'] = response.xpath('//div[@class="company-info"]/ul/li[1]/text()').extract_first()

        item['city'] = response.xpath('//div[@class="company-info"]/ul/li[2]/text()').extract_first()
        item['phone'] = response.xpath('//div[@class="company-info"]/ul/li[3]/text()').extract_first()
        item['shop_hours'] = response.xpath('//div[@class="company-info"]/ul/li[4]/text()').extract_first()
        item['location'] = response.xpath('//div[@class="company-info"]/ul/li[5]/text()').extract_first()

        item['province'] = metadata['province']
        item['company'] = metadata['company']

        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url  # 序号+url

        yield item

