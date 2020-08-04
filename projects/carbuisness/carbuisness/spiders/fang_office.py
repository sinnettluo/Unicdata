# -*- coding: utf-8 -*-
"""

C2017-37


"""
import scrapy
from carbuisness.items import fangofficeitem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5

website='fang_office_test'

class CarSpider(scrapy.Spider):

    name=website

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        city_list=['','.sh','.gz','.tj','.cq','.cd','.suzhou','.wuhan','.xian','.dg','.km','.hz','.jn','.wuxi','.zz','.nc','.qd','.sjz','.nanjing','.dl','.hkproperty']
        for temp in city_list:
            url="http://office"+temp+".fang.com/"
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        x = response.xpath('//div[@class="qxName"]/a')
        for i in range(1,len(x)-1):
            urlbase=x[i].xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle1_parse)

    def middle1_parse(self,response):
        x = response.xpath('//p[@class="contain"]/a')
        for i in range(1, len(x)):
            urlbase = x[i].xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle2_parse)

    def middle2_parse(self,response):
        x = response.xpath('//div[@class="houseList"]/dl')
        for temp in x:
            urlbase = temp.xpath('dd/p/a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.parse_info)
        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.middle2_parse)

    def parse_info(self,response):
        item=fangofficeitem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['shortdesc']=response.xpath('//div[@class="title"]/h1/text()').extract_first().strip() \
            if response.xpath('//div[@class="title"]/h1/text()').extract_first() else "-"
        item['houseid']=response.xpath(u'//span[contains(text(),"房源编号")]/text()').re('\d+')[0] \
            if response.xpath(u'//span[contains(text(),"房源编号")]/text()').re('\d+') else "-"
        item['posttime']=response.xpath('//p[@class="gray9"]/text()[3]').re(u'发布时间：(.*)\(')[0] \
            if response.xpath('//p[@class="gray9"]/text()[3]').re(u'发布时间：(.*)\(') else "-"
        item['price']=response.xpath('//span[@class="red20b"]/text()').extract_first() \
            if response.xpath('//span[@class="red20b"]/text()').extract_first() else "-"
        item['unitprice']=response.xpath(u'//span[contains(text(),"元/平米·月")]/../span/span/text()').extract_first() \
            if response.xpath(u'//span[contains(text(),"元/平米·月")]/../span/span/text()').extract_first() else "-"
        item['area']=response.xpath('//dd[@class="gray6"]/span/text()').extract_first() \
            if response.xpath('//dd[@class="gray6"]/span/text()').extract_first() else "-"
        item['phone']=response.xpath('//label[@id="mobilecode"]/text()').extract_first() \
            if response.xpath('//label[@id="mobilecode"]/text()').extract_first() else "-"
        item['housename']=response.xpath(u'//span[contains(text(),"楼盘名称：")]/../a/text()').extract_first() \
            if response.xpath(u'//span[contains(text(),"楼盘名称：")]/../a/text()').extract_first() else "-"
        item['address']=response.xpath(u'//span[contains(text(),"楼盘地址：")]/../text()[1]').extract_first() \
            if response.xpath(u'//span[contains(text(),"楼盘地址：")]/../text()[1]').extract_first() else "-"
        item['propertycost']=response.xpath(u'//span[contains(text(),"\u7269 \u4e1a \u8d39\uff1a")]/text()').re(u'\u7269 \u4e1a \u8d39\uff1a(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"\u7269 \u4e1a \u8d39\uff1a")]/text()').re(u'\u7269 \u4e1a \u8d39\uff1a(.*)') else "-"
        item['level']=response.xpath(u'//span[contains(text(),"等")]/text()[2]').re(u'\uff1a(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"等")]/text()[2]').re(u'\uff1a(.*)') else "-"
        item['fitment']=response.xpath(u'//span[contains(text(),"装")]/../text()[2]').extract_first() \
            if response.xpath(u'//span[contains(text(),"装")]/../text()[2]').extract_first() else "-"
        item['type']=response.xpath(u'//span[contains(text(),"类")]/../text()[2]').extract_first() \
            if response.xpath(u'//span[contains(text(),"类")]/../text()[2]').extract_first() else "-"
        yield item
