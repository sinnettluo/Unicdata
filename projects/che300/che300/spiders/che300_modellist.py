# -*- coding: utf-8 -*-
import scrapy
from ..items import che300modellist
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import json
import datetime
import random
from selenium import webdriver
from lxml import etree


website = 'che300_modellist_' + settings["UPDATE_CODE"]
# website = 'che300_modellist'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]

    start_urls=[
        'https://www.che300.com/pinggu'
    ]
    # custom_settings = {"CONCURRENT_REQUESTS"
    #                    :10}

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 2000000000
        self.counts = 0
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')






    #brandselect
    def parse(self,response):

        browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        browser.get(response.url)
        # print(browser.page_source)
        selector = etree.HTML(browser.page_source)

        for br in selector.xpath('//p[@class="pinpailist list_1"]'):
            brandid = br.xpath('@id')[0]
            brandname = br.xpath('text()')[0]
            metadata = {"brandid": brandid, "brandname": brandname}
            url = "https://ssl-meta.che300.com/meta/series/series_brand"+ brandid +".json"
            print url
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_family, dont_filter=True)

        browser.quit()


    def parse_family(self,response):
        meta = response.meta['metadata']
        # print meta
        data = json.loads(response.xpath('//p/text()').extract_first())
        for info in data:
            factoryname = info['series_group_name']
            familyid = info['series_id']
            familyname = info['series_name']
            familyinfo = {"factoryname": factoryname, "familyid": familyid, "familyname": familyname}
            familydata = dict(familyinfo, **meta)
            # print familydata
            # print familyname
            url = "https://ssl-meta.che300.com/meta/model/model_series"+ familyid +".json"
            yield scrapy.Request(url, meta={"familydata": familydata}, callback=self.parse_vehileinfo, dont_filter=True)

    def parse_vehileinfo(self, response):
        print response.text

        meta = response.meta['familydata']
        # print meta
        # procity = json.loads()
        data = json.loads(response.xpath('//p/text()').extract_first())
        for info in data:
            item = che300modellist()
            item['max_reg_year'] = info['max_reg_year']
            item['min_reg_year']  = info['min_reg_year']
            item['price']  = info['model_price']
            item['makeyear']  = int(info['model_year'])
            item['salesdescid']  = info['model_id']
            item['salesdesc']  = info['model_name']
            item['liter']  = info['liter']
            item['liter_type']  = info['liter_type']
            item['geartype']  = info['gear_type']
            item['emission']  = info['discharge_standard']
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = md5(item['salesdescid'] + '_'+ settings["UPDATE_CODE"]).hexdigest()
            item = dict(item,**meta)
            yield item
            # print item