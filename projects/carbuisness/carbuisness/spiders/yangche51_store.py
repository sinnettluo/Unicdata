# -*- coding: utf-8 -*-
"""

C2017-09

"""
import scrapy
from carbuisness.items import Yangche51StoreItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='yangche51_store'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://p.yangche51.com/p-110100']

    def __init__(self,**kwargs):
        #print "do init"
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        areas = response.xpath('//div[@class="province"]/p/a')
        for area in areas:
            city = area.xpath('text()').extract_first()
            metadata = {"city" : city}
            url = area.xpath('@href').extract_first()
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)

    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        if response.xpath('//div[@id="points"]/text()'):
            points_base = response.xpath('//div[@id="points"]/text()').extract_first()
            points = points_base.split("|")
            for point_info in points:
                point = point_info.split(",")
                location = point[2]
                addmeta = {"location" : location}
                metadata = dict(metadata, **addmeta)
                url_info = point[3]
                url = "http://p.yangche51.com/info-" + url_info +".html"
                yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        metadata = response.meta['metadata']
        item = Yangche51StoreItem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        item['city'] = metadata['city']

        if response.xpath('//div[@class="shopName"]/p/text()'):
            item['shopname'] = response.xpath('//div[@class="shopName"]/p/text()').extract_first()
        else:
            item['shopname'] = "-"

        if response.xpath('//div[@class="shopName"]/h1/text()'):
            location = response.xpath('//div[@class="shopName"]/h1/text()').extract_first().strip()
            item['location'] = location
            item['shopno'] = re.findall("NO.(\d+)", location)[0]
        else:
            item['location'] = "-"
            item['shopno'] = "-"

        if response.xpath(u'//dt[contains(text(),"服务时间：")]/../dd/text()'):
            item['shop_hours'] = response.xpath(u'//dt[contains(text(),"服务时间：")]/../dd/text()').extract_first()
        else:
            item['shop_hours'] = "-"

        if response.xpath('//div[@class="shopInfo"]/input[@id="HiddenStrPhone"]/@value'):
            item['phone'] = response.xpath('//div[@class="shopInfo"]/input[@id="HiddenStrPhone"]/@value').extract_first()
        else:
            item['phone'] = "-"

        if response.xpath(u'//dt[contains(text(),"车型服务：")]/../dd//span[@class="percent"]/text()'):
            item['carservice'] = response.xpath(u'//dt[contains(text(),"车型服务：")]/../dd//span[@class="percent"]/text()').extract_first()
        else:
            item['carservice'] = "-"

        if response.xpath(u'//dt[contains(text(),"技术等级：")]/../dd//div[@class="techdiv"]/strong/text()'):
            item['skilllevel'] = response.xpath(u'//dt[contains(text(),"技术等级：")]/../dd//div[@class="techdiv"]/strong/text()').extract_first()
        else:
            item['skilllevel'] = "-"

        if response.xpath(u'//dt[contains(text(),"用户评价：")]/../dd/div[@class="nStar"]/span/a/text()'):
            num = response.xpath(u'//dt[contains(text(),"用户评价：")]/../dd/div[@class="nStar"]/span/a/text()').extract_first()
            item['commentnum'] = re.findall("\d+", num)[0]
        else:
            item['commentnum'] = "-"

        if response.xpath(u'//dt[contains(text(),"好 评 率 ：")]/../dd/div[@class="shopLine"]/span/text()'):
            item['goodper'] = response.xpath(u'//dt[contains(text(),"好 评 率 ：")]/../dd/div[@class="shopLine"]/span/text()').extract_first()
        else:
            item['goodper'] = "-"

        if response.xpath('//div[@class="shopScore"]/div/span[@class="zanGoal"][1]/a/text()'):
            userscore = response.xpath('//div[@class="shopScore"]/div/span[@class="zanGoal"][1]/a/text()').extract_first().strip()
            item['userscore'] = re.findall(u"(.*?)分", userscore)[0]
        else:
            item['userscore'] = "-"

        if response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"服务态度：")]/../dd[1]/div[@class="nStar"]/span/text()'):
            servicescore = response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"服务态度：")]/../dd[1]/div[@class="nStar"]/span/text()').extract_first()
            item['servicescore'] = re.findall(u"(.*?)分", servicescore)[0]
        else:
            item['servicescore'] = "-"


        if response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"店内环境：")]/../dd[2]/div[@class="nStar"]/span/text()'):
            envirscore = response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"店内环境：")]/../dd[2]/div[@class="nStar"]/span/text()').extract_first()
            item['envirscore'] = re.findall(u"(.*?)分", envirscore)[0]
        else:
            item['envirscore'] = "-"

        if response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"技术水平：")]/../dd[3]/div[@class="nStar"]/span/text()'):
            skillscore = response.xpath(u'//dl[@id="staScore"]/dt[contains(text(),"技术水平：")]/../dd[3]/div[@class="nStar"]/span/text()').extract_first()
            item['skillscore'] = re.findall(u"(.*?)分", skillscore)[0]
        else:
            item['skillscore'] = "-"

        yield item

