# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import HaicjItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
import MySQLdb

website='haicj'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        ""
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def start_requests(self):
        mysqlconnection = MySQLdb.connect('192.168.1.94', 'root', 'Datauser@2017', 'dazhong_zb', port=3306)
        dbc = mysqlconnection.cursor()
        dbc.execute(
            'SELECT vehicle_models FROM haicheji_id')
        result = dbc.fetchall()
        for each in result:
            url = "http://www.haicj.com/carinfo.jsp?clxh=%s&typeid=2" % each[0]
            yield scrapy.Request(url)



    def parse(self, response):
        item = HaicjItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['level'] = response.xpath('//*[@id="cljb"]/text()').extract_first()
        item['zhouju'] = response.xpath('//*[@id="zj"]/text()').extract_first()
        item['changkuangao'] = response.xpath('//*[@id="cd_kd_gd"]/text()').extract_first()
        item['title'] = response.xpath('//*[@id="carInfoBox"]/div[1]/i/text()').extract_first().replace("（", "").replace("）", "")
        item['factory'] = response.xpath('//*[@id="cjmc"]/text()').extract_first()
        item['body'] = response.xpath('//*[@id="csxs"]/text()').extract_first()
        item['pailiang'] = response.xpath('//*[@id="pl"]/text()').extract_first()
        item['fuel'] = response.xpath('//*[@id="rylx"]/text()').extract_first()
        item['paifang'] = response.xpath('//*[@id="pfbz"]/text()').extract_first()

        yield item