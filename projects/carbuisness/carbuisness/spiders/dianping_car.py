# -*- coding: utf-8 -*-
"""
taskid=taskid=C2017-07

"""
import scrapy
from carbuisness.items import meituancarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='dianping_car_test'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['http://www.dianping.com/citylist/citylist?citypage=1']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self, response):
        print "do parse"
        x=response.xpath('//div[@class="main page-cityList"]/div/ul/li')
        for temp in x[0:2]:
            base = temp.xpath('div/a')
            for temp1 in base:
                citydata = dict()
                urlbase = temp1.xpath('@href').extract_first()
                city=temp1.xpath('strong/text()').extract_first()
                url=response.urljoin(urlbase)
                if not city:
                    city=temp1.xpath('text()').extract_first()
                citydata['city'] = city
                yield scrapy.Request(url, meta={'citydata': citydata}, callback=self.parse_middle1)

        for temp in x[2:5]:
            base=temp.xpath('dl/dd/a')
            for temp1 in base:
                citydata = dict()
                urlbase = temp1.xpath('@href').extract_first()
                city = temp1.xpath('strong/text()').extract_first()
                url = response.urljoin(urlbase)
                citydata['city']=city
                yield scrapy.Request(url,meta={'citydata':citydata},callback=self.parse_middle1)


    def parse_middle1(self,response):
        print "parse_middle1"
        metadata = response.meta['citydata']
        cityid=response.xpath('//script[contains(text(),"var G_rtop")]/text()').re('_setCityId\', (\d+)]')[0] \
            if response.xpath('//script[contains(text(),"var G_rtop")]/text()').re('_setCityId\', (\d+)]') else "-"
        addmeta={"cityid":cityid}
        metadata = dict(metadata, **addmeta)
        url="http://www.dianping.com/search/category/"+str(cityid)+"/65"
        print url
        yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_middle2)

    def parse_middle2(self,response):
        print "parse_middle2"
        metadata = response.meta['metadata']
        x=response.xpath('//div[@id="region-nav"]/a')
        for temp in x:
            districtdata = dict()
            urlbase = temp.xpath('@href').extract_first()
            district = temp.xpath('span/text()').extract_first()
            url=response.urljoin(urlbase)
            districtdata['district']=district
            metadata = dict(metadata, **districtdata)
            yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_middle3)

    def parse_middle3(self,response):
        print "parse_middle3"
        metadata = response.meta['metadata']
        x = response.xpath('//div[@id="region-nav-sub"]/a')
        for temp in x[1:len(x)]:
            urlbase = temp.xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_middle4)

    def parse_middle4(self,response):
        print "parse_middle4"
        metadata = response.meta['metadata']
        x = response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li')
        for temp in x:
            urlbase = temp.xpath('div[@class="txt"]/div/a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_car)
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url, meta={'metadata': metadata}, callback=self.parse_middle4)


    def parse_car(self,response):
        print "parse_car"
        metadata = response.meta['metadata']
        item=meituancarItem()
        item['website'] = website
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['city']=metadata['city']
        item['cityid']=metadata['cityid']
        item['district']=metadata['district']
        item['shopname']=response.xpath('//h1[@class="shop-name"]/text()').extract_first().strip() \
            if response.xpath('//h1[@class="shop-name"]/text()').extract_first() else "-"
        item['starnum']=response.xpath('//span[@class="mid-rank-stars mid-str40"]/@title').extract_first() \
            if response.xpath('//span[@class="mid-rank-stars mid-str40"]/@title').extract_first() else "-"
        item['phone']=response.xpath('//p[@class="expand-info tel"]/span[2]/text()').extract_first() \
            if response.xpath('//p[@class="expand-info tel"]/span[2]/text()').extract_first() else "-"
        item['location']=response.xpath('//div[@class="expand-info address"]/span[2]/@title').extract_first() \
            if response.xpath('//div[@class="expand-info address"]/span[2]/@title').extract_first() else "-"
        item['commentnum']=response.xpath('//span[@id="reviewCount"]/text()').re('\d')[0] \
            if response.xpath('//span[@id="reviewCount"]/text()').re('\d') else "-"
        item['shop_hours']=response.xpath(u'//span[contains(text(),"营业时间：")]/../span[2]/text()').extract_first().strip() \
            if response.xpath(u'//span[contains(text(),"营业时间：")]/../span[2]/text()').extract_first() else "-"
        item['price']=response.xpath(u'//span[contains(text(),"价格")]/text()').re(u'\u4ef7\u683c：(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"价格")]/text()').re(u'\u4ef7\u683c：(.*)') else "-"
        item['skillscore']=response.xpath(u'//span[contains(text(),"技术：")]/text()').re(u'\u6280\u672f\uff1a(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"技术：")]/text()').re(u'\u6280\u672f\uff1a(.*)') else "-"
        item['enscore']=response.xpath(u'//span[contains(text(),"环境：")]/text()').re(u'\u73af\u5883\uff1a(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"环境：")]/text()').re(u'\u73af\u5883\uff1a(.*)') else "-"
        item['servicescore']=response.xpath(u'//span[contains(text(),"服务：")]/text()').re(u'\u670d\u52a1\uff1a(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"服务：")]/text()').re(u'\u670d\u52a1\uff1a(.*)') else "-"
        print item['url']
        yield item
