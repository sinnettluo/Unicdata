# -*- coding: utf-8 -*-
"""

C2017-21

"""
import scrapy
from carbuisness.items import GasDianpingItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

website='dianping_gas'

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
        desired_capabilities["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
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
        # self.browser = webdriver.PhantomJS(executable_path="/root/phantomjs/bin/phantomjs")
        self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
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
        areas = response.xpath('//ul[@id="divArea"]')
        for area in areas:
            if area.xpath('.//a//text()').extract_first()!= u"更多":
                cityname = area.xpath('.//a//text()').extract_first()
                cityurlbase = area.xpath('.//a/@href').extract_first()
                city_pingyin = re.findall("/(\S+)", cityurlbase)[0]
                url = "http://www.dianping.com/" + city_pingyin
                # proxy = getProxy()
                # headers = {'Accept': 'application/json, text/javascript'}
                metadata = {"cityname":cityname}
                yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)

    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        # cityid = re.findall("\['_setCityId', (\d)\]", response.body)[0]   早期的id提取
        cityid_base = response.xpath('//script[@type="text/javascript"]/text()').extract_first()
        cityid = re.findall("cityId.*?(\d+)", cityid_base)[0]
        addmeta = {"cityid" : cityid}
        metadata = dict(metadata, **addmeta)
        url = "http://www.dianping.com/search/category/" + cityid + "/65/g236"
        yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)

    def parse_middle2(self, response):
        metadata = response.meta['metadata']
        areas = response.xpath('//div[@id="region-nav"]')
        for area in areas:
            district = area.xpath('.//a/span/text()').extract_first()
            addmeta = {"district" : district}
            metadata = dict(metadata, **addmeta)
            urlbase = area.xpath('.//a/@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle3, dont_filter=True)

    def parse_middle3(self, response):
        metadata = response.meta['metadata']
        urls = response.xpath('//div[@id="region-nav-sub"]//a')
        flag = 0
        for urlbase in urls:
            #这里第一个链接是“不限”，最后一个链接是“更多”。需要删除
            if flag and urlbase.xpath('text()').extract_first()!="更多":
                url_temp = urlbase.xpath('@href').extract_first()
                url = response.urljoin(url_temp)
                yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle4, dont_filter=True)
            else:
                flag =1

    def parse_middle4(self, response):
        metadata = response.meta['metadata']
        gas_stations = response.xpath('//div[@id="shop-all-list"]/ul/li')
        for gas_station in gas_stations:
            urlbase = gas_station.xpath('div[@class="txt"]/div[@class="tit"]/a[1]/@href').extract_first()
            url = response.urljoin(urlbase)
            print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle5, dont_filter=True)
        next_page = response.xpath('//a[@class="next"]')
        if next_page:
            next = next_page.xpath('@href').extract_first()
            nexturl = response.urljoin(next)
            yield scrapy.Request(nexturl, meta={"metadata":metadata}, callback=self.parse_middle4, dont_filter=True)

    def parse_middle5(self, response):
        item = GasDianpingItem()
        metadata = response.meta['metadata']
        parse_infos = response.xpath('//div[@id="basic-info"]')
        for info in parse_infos:
            if info.xpath('h1/text()'):
                item['shopname'] = info.xpath('h1/text()').extract_first().strip()
            else:
                item['shopname'] = "-"

            if info.xpath('div[@class="brief-info"]/span/@title'):
                item['starnum'] = info.xpath('div[@class="brief-info"]/span/@title').extract_first()
            else:
                item['starnum'] = "-"

            if info.xpath('div[@class="expand-info address"]/span[2]/text()'):
                item['location'] = info.xpath('div[@class="expand-info address"]/span[2]/text()').extract_first().strip()
            else:
                item['location'] = "-"

            if info.xpath('p[@class="expand-info tel"]/span[2]/text()'):
                item['phone'] = info.xpath('p[@class="expand-info tel"]/span[2]/text()').extract_first()
            else:
                item['phone'] = "-"

            if info.xpath('div[@class="other J-other"]/p/span[2]/text()'):
                item['shop_hours'] = info.xpath('div[@class="other J-other"]/p/span[2]/text()').extract_first()
            else:
                item['shop_hours'] = "-"

            if info.xpath('div[@class="brief-info"]/span[2]/text()'):
                commentnum = info.xpath('div[@class="brief-info"]/span[2]/text()').extract_first()
                item['commentnum'] = re.findall("\d+", commentnum)[0]
            else:
                item['commentnum'] = "-"

            if info.xpath('div[@class="brief-info"]/span[3]/text()'):
                pricebase = info.xpath('div[@class="brief-info"]/span[3]/text()').extract_first()
                item['price'] = re.findall(u"费用：(\S+)", pricebase)[0]
            else:
                item['price'] = "-"

            if response.xpath(u'//span[contains(text(),"技术：")]/text()'):
                item['skillscore'] = response.xpath(u'//span[contains(text(),"技术：")]/text()').re(u'\u6280\u672f\uff1a(.*)')[0]
            else:
                item['skillscore'] = "-"
            if response.xpath(u'//span[contains(text(),"环境：")]/text()'):
                item['enscore'] = response.xpath(u'//span[contains(text(),"环境：")]/text()').re(u'\u73af\u5883\uff1a(.*)')[0]
            else:
                item['enscore'] = "-"
            if response.xpath(u'//span[contains(text(),"服务：")]/text()'):
                item['servicescore'] = response.xpath(u'//span[contains(text(),"服务：")]/text()').re(u'\u670d\u52a1\uff1a(.*)')[0]
            else:
                item['servicescore'] = "-"

            item['district'] = metadata['district']
            item['cityid'] = metadata['cityid']
            item['cityname'] = metadata['cityname']
            item['url'] = response.url
            item['website'] = website
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = response.url

            yield item
