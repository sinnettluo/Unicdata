# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import JiaotongbuItem
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

website='jiaotongbu'

class CarSpider(scrapy.Spider):

    name=website
    # start_urls = [
    #     "http://www.mot.gov.cn/",
    # ]

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


    def start_requests(self):
        urls = []
        for i in range(20):
            url = "http://was.mot.gov.cn:8080/govsearch/searPagenew.jsp?page="+ str(i) +"&pubwebsite=zfxxgk&indexPa=2&schn=601&sinfo=571&surl=zfxxgk/&curpos=%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%E9%83%A8%E4%BB%A4"
            urls.append(scrapy.Request(url=url))
        return  urls


    def parse(self, response):
        lis = response.xpath("//ul[@class='fl w100']/li")
        for li in lis:
            url = li.xpath("a/@href").extract_first()
            # time = li.xpath("span/text()").extract_first().strip()
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        item = JiaotongbuItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['index'] = response.xpath("//*[@class='col-md-9'][2]/text()").extract()[0].strip()
        item['wenhao'] = response.xpath("//*[@class='col-md-9'][3]/text()").extract()[0].strip()
        item['category'] = response.xpath("//*[@class='col-md-9'][1]/text()").extract()[1].strip()
        item['theme'] = response.xpath("//*[@class='col-md-9'][2]/text()").extract()[1].strip()
        item['industry'] = response.xpath("//*[@class='col-md-9'][3]/text()").extract()[1].strip()
        item['time'] = response.xpath("//*[@class='col-md-9'][4]/text()").extract()[0].strip()
        item['name'] = response.xpath("//*[@class='col-md-9'][1]/text()").extract()[0].strip()
        item['keyword'] = response.xpath("//*[@class='col-md-9'][4]/text()").extract()[1].strip()
        try:
            content = response.xpath("//*[@id='content_main']").extract()[0]
        except Exception as e:
            pass
        r = re.compile(r'</?\w+[^>]*>', re.S)
        final_content = r.sub("", content).strip()
        # print(final_content)
        item['content'] = final_content

        # print(item)
        yield item

