# -*- coding: utf-8 -*-
"""

C2017-22

"""
import scrapy
from carbuisness.items import GasSinopecItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='sinopec_gas'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://www.sinopecsales.com/website/html/service/jiayouzhan.html']

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=50000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        #print "do parse"
        time.sleep(1)
        areas = response.xpath('//div[@class="serve_left"]/ul/li')
        for area in areas:
            urlbase = area.xpath('a/@href').extract_first()
            province = area.xpath('a/div/text()').extract_first().strip()
            urltemp = re.findall("website(\S+)", urlbase)[0]
            url = "http://www.sinopecsales.com/website" + urltemp
            metadata = {"province" : province}
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle, dont_filter=True)

    def parse_middle(self, response):
        #print "do parse_middle"
        metadata = response.meta['metadata']
        urlfront =  re.findall("(.*?)pageNo=", response.url)[0] + "pageNo="
        #urlnum = re.findall("pageNo=(\d+)", response.url)[0]
        urlback =  "&stationCharge=" + re.findall("stationCharge=(\S+)", response.url)[0]
        pagenumbase = response.xpath(u'//td[contains(text(), "第 1 页")]/text()').extract_first().strip()
        pagenum = re.findall(u"共 (\d+)", pagenumbase)[0]
        for i in range(1, int(pagenum)+1):
            url = urlfront + str(i) + urlback
            #print url
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        #print "parse_info"
        metadata = response.meta['metadata']
        tbody = response.xpath(u'//th[contains(text(), "序号")]/../../tr')

        flag = 0    #第一个是空值需要过滤掉
        #print response.url
        for dot in tbody:
            if dot and flag!=0:
                item = GasSinopecItem()

                if dot.xpath('td[2]/text()'):
                    item['dotname'] = dot.xpath('td[2]/text()').extract_first()
                else:
                    item['dotname'] = "-"

                if dot.xpath('td[3]/text()'):
                    item['location'] = dot.xpath('td[3]/text()').extract_first().strip()
                else:
                    item['location'] = "-"

                if dot.xpath('td[4]/text()'):
                    item['sell_card'] = dot.xpath('td[4]/text()').extract_first().strip()
                else:
                    item['sell_card'] = "-"

                if dot.xpath('td[5]/text()'):
                    item['phonenum'] = dot.xpath('td[5]/text()').extract_first().strip()
                else:
                    item['phonenum'] = "-"

                if dot.xpath('td[6]/text()'):
                    item['electronic_prepaid_card_invoice'] = dot.xpath('td[6]/text()').extract_first().strip()
                else:
                    item['electronic_prepaid_card_invoice'] = "-"

                if dot.xpath('td[7]/text()'):
                    item['valueadd_tax_invoice'] = dot.xpath('td[7]/text()').extract_first().strip()
                else:
                    item['valueadd_tax_invoice'] = "-"

                # item['pagenum'] = re.findall("pageNo=(\d+)", response.url)[0]
                item['province'] = metadata['province']
                item['url'] = response.url
                item['website'] = website
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['status'] = str(dot.xpath('td[1]/text()').extract_first()) + response.url  #序号+url
                yield item
            else:
                flag = 1
