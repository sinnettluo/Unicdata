# -*- coding: utf-8 -*-
"""
C2017-38
"""
import scrapy
from carbuisness.items import fangshopitem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5

website='fang_shop'

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
            url="http://shop"+temp+".fang.com/zu/house/"
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        x = response.xpath('//div[@class="qxName"]/a')
        for i in range(1,len(x)-1):
            urlbase=x[i].xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle1_parse, dont_filter=True)

    def middle1_parse(self,response):
        x = response.xpath('//div[@class="houseList"]/dl')
        for temp in x:
            urlbase = temp.xpath('dd/p[@class="title"]/a/@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.parse_info, dont_filter=True)
        next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            url=response.urljoin(next_page)
            yield scrapy.Request(url,callback=self.middle1_parse, dont_filter=True)

    def parse_info(self,response):
        item=fangshopitem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['shortdesc']=response.xpath('//div[@class="title"]/h1/text()').extract_first().strip() \
            if response.xpath('//div[@class="title"]/h1/text()').extract_first() else "-"                   # 标题描述
        item['houseid']=response.xpath(u'//span[contains(text(),"房源编号")]/text()').re('\d+')[0] \
            if response.xpath(u'//span[contains(text(),"房源编号")]/text()').re('\d+') else "-"             # 房源编号
        item['posttime']=response.xpath('//p[@class="gray9"]/text()[3]').re(u'发布时间：(.*)\(')[0] \
            if response.xpath('//p[@class="gray9"]/text()[3]').re(u'发布时间：(.*)\(') else "-"              # 发布时间
        item['price']=response.xpath('//span[@class="red20b"]/text()').extract_first() \
            if response.xpath('//span[@class="red20b"]/text()').extract_first() else "-"                        # 价格
        item['paystyle']=response.xpath('//dt[@class="gray6 zongjia1"]/text()[3]').re(u'支付方式：(.*)\)')[0] \
            if response.xpath('//dt[@class="gray6 zongjia1"]/text()[3]').re(u'支付方式：(.*)\)') else "-"    # 支付方式
        item['area']=response.xpath(u'//dt[contains(text(),"建筑面积：")]/strong/text()').extract_first() \
            if response.xpath(u'//dt[contains(text(),"建筑面积：")]/strong/text()').extract_first() else "-"     # 建筑面积
        item['phone']=response.xpath('//div[@class="phone_top"]/span/label/text()').extract_first() \
            if response.xpath('//div[@class="phone_top"]/span/label/text()').extract_first() else "-"               # 电话
        item['shopname']=response.xpath(u'//span[contains(text(),"楼盘名称：")]/../text()[2]').extract_first().strip() \
            if response.xpath(u'//span[contains(text(),"楼盘名称：")]/../text()[2]').extract_first() else "-"        # 楼盘名称
        item['address']=response.xpath(u'//span[contains(text(),"楼盘地址：")]/../text()[1]').extract_first() \
            if response.xpath(u'//span[contains(text(),"楼盘地址：")]/../text()[1]').extract_first() else "-"        # 楼盘地址
        item['propertycost']=response.xpath(u'//span[contains(text(),"物业费：")]/../text()[1]').extract_first() \
            if response.xpath(u'//span[contains(text(),"物业费：")]/../text()[1]').extract_first() else "-"             # 物业费
        item['sfb']=response.xpath(u'//span[contains(text(),"适合经营：")]/../span[2]/text()').extract_first() \
            if response.xpath(u'//span[contains(text(),"适合经营：")]/../span[2]/text()').extract_first() else "-"       # 适合经营
        item['type']=response.xpath('//div[@class="inforTxt"]/dl[2]/dd[3]/text()[2]').extract_first() \
            if response.xpath('//div[@class="inforTxt"]/dl[2]/dd[3]/text()[2]').extract_first() else "-"                    # 房屋类型
        item['uniprice']=response.xpath(u'//span[contains(text(),"元/平米·天")]/../span/text()').extract_first().strip() \
            if response.xpath(u'//span[contains(text(),"元/平米·天")]/../span/text()').extract_first() else "-"         # 租金
        yield item




