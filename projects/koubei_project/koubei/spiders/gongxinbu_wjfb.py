# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GongxinbuWJFBItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests

website='gongxinbu_wjfb'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://xxgk.miit.gov.cn/gdnps/wjfbindex.jsp",
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    # def start_requests(self):
    #     return [scrapy.FormRequest(method="post", url="http://220.191.209.149:8888/asset-server/asset/api/v0.1/charging-stations")]

    def parse(self, response):
        # page_num = response.xpath("//*[@id='allPageId']/text()").re("条  (\d+)页")[0]
        page_num = 390
        for i in range(1, int(page_num) + 1):
            url = "http://xxgk.miit.gov.cn/gdnps/searchIndex.jsp?params=%257B%2522goPage%2522%253A"+ str(i) +"%252C%2522orderBy%2522%253A%255B%257B%2522orderBy%2522%253A%2522publishTime%2522%252C%2522reverse%2522%253Atrue%257D%252C%257B%2522orderBy%2522%253A%2522orderTime%2522%252C%2522reverse%2522%253Atrue%257D%255D%252C%2522pageSize%2522%253A10%252C%2522queryParam%2522%253A%255B%257B%257D%252C%257B%257D%252C%257B%2522shortName%2522%253A%2522fbjg%2522%252C%2522value%2522%253A%2522%252F1%252F29%252F1146295%252F1652858%252F1652930%2522%257D%255D%257D&callback=jQuery111108606409841256462_1545986100348&_=1545986100356"
            yield scrapy.Request(url=url, callback=self.parse_api)

    def parse_api(self, response):
        json_str = response.text.replace("jQuery111108606409841256462_1545986100348(", "").replace(");", "")
        json_obj = json.loads(json_str)
        for wj in json_obj["resultMap"]:
            item = GongxinbuWJFBItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = wj["id"]
            item['title'] = wj["title"]
            item['name'] = wj["subjectName"]
            item['time'] = wj["publishTime"]
            content = wj["htmlContent"]
            r = re.compile(r'</?\w+[^>]*>', re.S)
            final_content = r.sub("", content).strip()
            item['content'] = final_content
            # print(item)
            yield item
