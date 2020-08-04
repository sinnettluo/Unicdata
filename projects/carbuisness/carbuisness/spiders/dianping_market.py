# -*- coding: utf-8 -*-
"""
taskid=C2017-15

"""
import scrapy
from carbuisness.items import dianpingmarketitem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
website='dianping_market'

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

        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        # cookies = {
        #     '_hc.v': '6816d991-e52c-b34c-cc39-42da62e1157e.1505100566',
        #     's_ViewType': '10',
        #     '_lxsdk_cuid': '15f297ee321c8-0e880d3f104725-3e63430c-144000-15f297ee32123',
        #     '_lxsdk': '15f297ee321c8-0e880d3f104725-3e63430c-144000-15f297ee32123',
        #     '__utma': '1.1141451281.1505100566.1505100566.1508389667.2',
        #     '__utmz': '1.1505100566.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        #     'aburl': '1',
        #     'cy': '2',
        #     'cy2': 'beijing',
        #     '_lxsdk_s': '15f3334019b-8c-8e6-79b%7C%7C53'
        # }
        self.browser = webdriver.PhantomJS(executable_path="/root/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        self.browser.start_session(desired_capabilities)
        self.browser.implicitly_wait(10)
        self.browser.get("http://www.dianping.com/")
        # self.browser.add_cookie(cookies)

        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

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
        url="http://www.dianping.com/search/category/"+str(cityid)+"/20/g119"
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
        item = dianpingmarketitem()
        item['website'] = website
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['city'] = metadata['city']
        item['cityid'] = metadata['cityid']
        item['district'] = metadata['district']

        if response.xpath('//h2[@class="market-name"]/text()'):
            item['shopname'] = response.xpath('//h2[@class="market-name"]/text()').extract_first().strip()
        elif response.xpath('//h1[@class="shop-name"]/text()'):
            item['shopname'] = response.xpath('//h1[@class="shop-name"]/text()').extract_first().strip()
        else:
            item['shopname'] = ""

        item['starnum']=response.xpath('//span[@class="mid-rank-stars mid-str40"]/@title').extract_first() \
            if response.xpath('//span[@class="mid-rank-stars mid-str40"]/@title').extract_first() else "-"
        item['phone']=response.xpath('//div[@class="market-detail-other Hide"]/p/text()[2]').extract_first().strip() \
            if response.xpath('//div[@class="market-detail-other Hide"]/p/text()[2]').extract_first() else "-"
        item['location']=response.xpath('//div[@class="market-detail"]/p/text()[3]').extract_first().strip() \
            if response.xpath('//div[@class="market-detail"]/p/text()[3]').extract_first() else "-"
        item['commentnum']=response.xpath('//span[@id="reviewCount"]/text()').re('\d')[0] \
            if response.xpath('//span[@id="reviewCount"]/text()').re('\d') else "-"
        item['shop_hours']=response.xpath(u'//span[contains(text(),"营业时间：")]/../text()[2]').extract_first() \
            if response.xpath(u'//span[contains(text(),"营业时间：")]/../text()[2]').extract_first() else "-"
        item['price']=response.xpath(u'//span[contains(text(),"人均消费：")]/../text()[2]').extract_first() \
            if response.xpath(u'//span[contains(text(),"人均消费：")]/../text()[2]').extract_first() else "-"
        item['productscore']=response.xpath(u'//span[contains(text(),"产品")]/text()').re(u'\u4ea7\u54c1(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"产品")]/text()').re(u'\u4ea7\u54c1(.*)') else "-"
        item['enscore']=response.xpath(u'//span[contains(text(),"环境")]/text()').re(u'\u73af\u5883(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"环境")]/text()').re(u'\u73af\u5883(.*)') else "-"
        item['servicescore']= response.xpath(u'//span[contains(text(),"服务")]/text()').re(u'\u670d\u52a1(.*)')[0] \
            if response.xpath(u'//span[contains(text(),"服务")]/text()').re(u'\u670d\u52a1(.*)') else "-"
        yield item
