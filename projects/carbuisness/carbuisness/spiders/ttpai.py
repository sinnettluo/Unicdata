# -*- coding: utf-8 -*-
import scrapy
from carbuisness.items import YouxinpaiPicItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import pymongo
import urllib2
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib
import os
from carbuisness.items import TTPaiItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

website = 'ttpai'

class TtpaiSpider(scrapy.Spider):
    name = "ttpai"
    allowed_domains = ["ttpai.cn"]
    start_urls = (
        'http://pai.ttpai.cn/',
    )
    def __init__(self, **kwargs):
        super(TtpaiSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 3000000
        self.page = 1
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(TtpaiSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):

        # print(response.body)

        lis = response.xpath("//*[@id='filter-form']/div[2]/div[2]/ul/li")
        print(lis)
        for li in lis:
            href = "http://pai.ttpai.cn" + li.xpath('./div[1]/a/@href').extract_first()
            yield scrapy.Request(href, callback=self.parse_detail)
        if self.page < 201:
            self.page = self.page + 1
            yield scrapy.Request('http://pai.ttpai.cn/', callback=self.parse, meta={'page': str(self.page)}, dont_filter=True)


    def parse_detail(self, response):
        div_num = 1
        if not response.xpath("//*[@id='car-info-nav']/div[1]/div[1]/div[1]/table/tr[7]/td[2]/text()"):
            div_num = 2
        item = TTPaiItem()
        item['title'] = response.xpath("//div[@class='car-title']/h1/span/text()").extract_first()
        item['car_type'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[7]/td[2]/text()").extract_first()
        item['location'] = ""
        item['regi_location'] = ""
        item['first_regi'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[4]/td[2]/text()").extract_first()
        item['miles'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[1]/td[2]/text()").extract_first()
        item['color'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[2]/td[2]/text()").extract_first()
        item['ex_times'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[10]/td[2]/text()").extract_first()
        item['use_type'] = response.xpath("//*[@id='car-info-nav']/div["+str(div_num)+"]/div[1]/div[1]/table/tr[6]/td[2]/span/text()").extract_first()
        item['car_level_main'] = response.xpath("//div[@class='section-degree']/span[1]/text()").extract_first()
        item['car_level_device'] = response.xpath("//div[@class='section-degree']/span[2]/text()").extract_first()
        item['car_level_outer'] = response.xpath("//div[@class='section-degree']/span[3]/text()").extract_first()
        item['car_level_inner'] = response.xpath("//div[@class='section-degree']/span[4]/text()").extract_first()
        item['report_url'] = response.url
        item['price'] = response.xpath("//div[@class='section-km clearfix']/ul/li[4]/span/text()").extract_first()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['desc'] = response.xpath("//div[@class='section-info']/p/text()").extract_first()
        item['status'] = response.url
        item['url'] = response.url
        yield item