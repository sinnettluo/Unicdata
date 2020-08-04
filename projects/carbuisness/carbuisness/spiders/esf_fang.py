# -*- coding: utf-8 -*-
"""
C2017-27-1
二手房和新房分成两个程序，这是二手房
"""

import scrapy
from carbuisness.items import EsfFangItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='esf_fang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://www.fang.com/SoufunFamily.htm']

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        time.sleep(1)
        cityurls = response.xpath('//table[@id="senfe"]//a')
        for cityurl in cityurls:
            citybase = cityurl.xpath('@href').extract_first()
            citypingyin = re.findall("http://(.*?)\.", citybase)[0]
            city = cityurl.xpath('text()').extract_first()
            metadata = {"city": city}
            url = "http://esf." + citypingyin + ".fang.com/housing/"
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)

    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        # areas = response.xpath('//div[@id="houselist_B03_02"]//a')
        areas = response.xpath('//div[@id="houselist_B03_02"]//div[@class="qxName"]/a')
        flag = 0    # 第一个对应网页上的“不限”
        for area in areas:
            if flag:
                districts = area.xpath('text()').extract()
                x = 0
                district = None
                for dis in districts:
                    if x==0:
                        x = 1
                        district = dis
                    else:
                        district += " " + dis
                addmeta = {"district" : district}
                metadata = dict(metadata, **addmeta)
                urlbase = area.xpath('@href').extract_first()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)
            else:
                flag = 1

    def parse_middle2(self, response):
        metadata = response.meta['metadata']
        coutys = response.xpath('//p[@id="shangQuancontain"]/a')
        flag = 0    #这第一个元素对应于页面上的“不限”
        for county_temp in coutys:
            if flag:
                county = county_temp.xpath('text()').extract_first()
                addmeta = {"county": county}
                metadata = dict(metadata, **addmeta)
                countyurlbase = county_temp.xpath('@href').extract_first()
                countyurl = response.urljoin(countyurlbase)
                yield scrapy.Request(countyurl, meta={"metadata":metadata}, callback=self.parse_middle3, dont_filter=True)
            else:
                flag = 1

    def parse_middle3(self, response):
        metadata = response.meta['metadata']
        esflist = response.xpath('//div[@class="listBox floatl"]/div[@class="houseList"]/div/dl')
        for esf in esflist:
            if esf.xpath('dd/p[1]/a/@href'):
                urlbase = esf.xpath('dd/p[1]/a/@href').extract_first()
                url = response.urljoin(urlbase)
                #print url
                yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle4, dont_filter=True)
        next_page = response.xpath(u'//a[contains(text(),"下一页")]')
        if next_page:
            next = next_page.xpath('@href').extract_first()
            nexturl = response.urljoin(next)
            yield scrapy.Request(nexturl, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)

    def parse_middle4(self, response):
        metadata = response.meta['metadata']

        webtype = 0
        addmeta = {"webtype": webtype}  # 这个字段用来标记两种不同的页面，以便后面根据不同页面分别解析
        metadata = dict(metadata, **addmeta)

        #   这里会得到两种不同页面，例如下面两个：
        #   http://mocoxsjcj.fang.com/esf/              这种情况对应webtype=2
        #   http://yangtaishanzhuang.fang.com/shop/     这种情况对应webtype==1
        #   http://xiuyunlild.fang.com/esf/             这种情况对应webtype==0
        #   分开解析
        url = None
        if response.xpath('//li[@id="xqw_C02_02"]/a/@href'):
            url = response.xpath('//li[@id="xqw_C02_02"]/a/@href').extract_first()
        elif response.xpath(u'//div[@class="snav_sq"]//li/a[contains(text(),"楼盘详情")]/@href'):
            url = response.xpath(u'//div[@class="snav_sq"]//li/a[contains(text(),"楼盘详情")]/@href').extract_first()
            webtype = 1
        elif response.xpath(u'//div[@class="xqnavN"]//li/a[contains(text(),"小区详情")]/@href'):
            url = response.xpath(u'//div[@class="xqnavN"]//li/a[contains(text(),"小区详情")]/@href').extract_first()
            webtype = 2
        metadata['webtype'] = webtype
        if url:
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        item = EsfFangItem()
        metadata = response.meta['metadata']
        #item['province'] = metadata['province']
        item['city'] = metadata['city']             # 城市
        item['district'] = metadata['district']     # 区
        item['county'] = metadata['county']         #
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        if metadata['webtype'] == 0:
            item['location'] = response.xpath(u'//strong[contains(text(),"小区地址")]/../@title').extract_first()       # 小区地址
            item['buildingname'] = response.xpath('//h1/a/text()').extract_first()                                          # 小区名
            if response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()'):
                housenumbase = response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()').extract_first()     # 总 户 数
                item['housenum'] = re.findall("\d+", housenumbase)[0]
            else:
                item['housenum'] = "-"
            item['completetime'] = response.xpath(u'//strong[contains(text(),"竣工时间：")]/../text()').extract_first()      # 竣工时间
            item['opening_quotation'] = response.xpath(u'//strong[contains(text(),"开盘时间")]/../text()').extract_first()  # 开盘时间
            item['area'] = response.xpath(u'//strong[contains(text(),"建筑面积：")]/../text()').extract_first()                  #  建筑面积
            item['parkingnum'] = response.xpath(u'//strong[contains(text(),"停 车 位：")]/../text()').extract_first()           # 停 车 位
            item['price'] = response.xpath(u'//dt[contains(text(),"本月均价")]/../dd/span/text()').extract_first()                  # 本月均价
            item['buildtype'] = response.xpath(u'//strong[contains(text(),"物业类别：")]/../text()').extract_first()             # 物业类别
            item['factoryname'] = response.xpath(u'//strong[contains(text(),"开 发 商：")]/../text()').extract_first()              # 开 发 商

        elif metadata['webtype'] == 1:
            item['location'] = response.xpath(u'//dd[contains(text(),"楼盘地址：")]/span/text()').extract_first()
            item['buildingname'] = response.xpath('//div[@class="title"]/span[@class="biaoti"]/text()').extract_first()
            item['housenum'] = "-"

            if response.xpath(u'//dd[contains(text(),"竣工时间")]/span/text()'):
                completetime = response.xpath(u'//dd[contains(text(),"竣工时间")]/span/text()').extract_first()
            else:
                completetime = response.xpath(u'//dd[contains(text(),"竣工时间")]/text()').extract_first()
            if re.findall(u"竣工时间：(\S+)", completetime):
                item['completetime'] = re.findall(u"竣工时间：(\S+)", completetime)[0]
            else:
                item['completetime'] = "-"

            item['opening_quotation'] = "-" #这种页面里面没有开盘时间这个字段的相关信息

            area = response.xpath(u'//dd[contains(text(),"建筑面积：")]/text()').extract_first()
            item['area'] = re.findall(u"建筑面积：(\S+)", area)[0]
            parkingnum = response.xpath(u'//dd[contains(text(),"停 车 位：")]/text()').extract_first()
            item['parkingnum'] = re.findall(u"停 车 位：(\S+)", parkingnum)[0]
            item['price'] = "-"
            buildtype = response.xpath(u'//dd[contains(text(),"物业类别：")]/text()').extract_first()
            item['buildtype'] = re.findall(u"物业类别：(\S+)", buildtype)[0]

            if response.xpath(u'//dd[contains(text(),"开 发 商：")]/span/text()'):
                item['factoryname'] = response.xpath(u'//dd[contains(text(),"开 发 商：")]/span/text()').extract_first()
            else:
                item['factoryname'] = response.xpath(u'//dd[contains(text(),"开 发 商")]/text()').extract_first()

        elif metadata['webtype'] == 2:
            item['location'] = response.xpath(u'//strong[contains(text(),"小区地址")]/../@title').extract_first()
            item['buildingname'] = response.xpath('//h1/a/text()').extract_first()
            if response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()'):
                housenumbase = response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()').extract_first()
                item['housenum'] = re.findall("\d+", housenumbase)[0]
            else:
                item['housenum'] = "-"
                if response.xpath(u'//strong[contains(text(),"竣工时间：")]/../text()'):
                    item['completetime'] = response.xpath(u'//strong[contains(text(),"竣工时间：")]/../text()').extract_first()
                if response.xpath(u'//strong[contains(text(),"开盘时间")]/../text()'):
                    item['opening_quotation'] = response.xpath(u'//strong[contains(text(),"开盘时间")]/../text()').extract_first()
                if response.xpath(u'//strong[contains(text(),"建筑面积：")]/../text()'):
                    item['area'] = response.xpath(u'//strong[contains(text(),"建筑面积：")]/../text()').extract_first()
                if response.xpath(u'//strong[contains(text(),"停 车 位：")]/../text()'):
                    item['parkingnum'] = response.xpath(u'//strong[contains(text(),"停 车 位：")]/../text()').extract_first()
                if response.xpath(u'//dt[contains(text(),"本月均价")]/../dd/span/text()'):
                    item['price'] = response.xpath(u'//dt[contains(text(),"本月均价")]/../dd/span/text()').extract_first()
                if response.xpath(u'//strong[contains(text(),"物业类别：")]/../text()'):
                    item['buildtype'] = response.xpath(u'//strong[contains(text(),"物业类别：")]/../text()').extract_first()
                if response.xpath(u'//strong[contains(text(),"开 发 商：")]/../text()'):
                    item['factoryname'] = response.xpath(u'//strong[contains(text(),"开 发 商：")]/../text()').extract_first()

        yield item

