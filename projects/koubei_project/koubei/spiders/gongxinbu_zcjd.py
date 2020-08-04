# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GongxinbuZCJDItem
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

website='gongxinbu_zcjd'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.miit.gov.cn/n1146295/n1652858/n1653018/index.html",
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
        lis = response.xpath("//div[@class='clist_con']/ul/li")
        for li in lis:
            url = li.xpath("a/@href").extract_first()
            title = li.xpath("a/text()").extract_first()
            time = li.xpath("span/a/text()").extract_first()
            meta = {"time": time, "title": title}
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_article)

        if response.url.find("index.html") >= 0:
            page_num = int(
                re.findall("maxPageNum \= (\d+)\;", response.text, re.S)[0])
            if page_num > 1:
                for i in range(2, page_num + 1):
                    next_url = "http://www.miit.gov.cn/n1146295/n1652858/n1653018/index_1274678_%d.html" % (i - 1)
                    yield scrapy.Request(url=next_url, callback=self.parse)

        # next = response.xpath("//a[text()='下页']")
        # print(next)
        # if next:
        #     str = next.xpath("@href").extract_first()
        #     yield scrapy.Request(url=response.urljoin(final_url), callback=self.parse)

    def parse_article(self, response):
        item = GongxinbuZCJDItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['time'] = response.meta["time"]
        item['title'] = response.meta["title"]
        try:
            content = response.xpath("//div[@id='notice_content']").extract()[0]
            url = re.findall("getResult\(\"(.*?)\"\)", content, re.S)[0]
            meta = {
                "url":item['url'],
                "status": item['status'],
                "time": item['time'],
                "title": item['title'],
            }
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_final)
        except Exception as e:
            content = response.xpath("//div[@class='ccontent center']").extract()[0]
            r = re.compile(r'</?\w+[^>]*>', re.S)
            final_content = r.sub("", content).strip()
            item['content'] = final_content
            yield item
            # print(item)


    def parse_final(self, response):
        item = GongxinbuZCJDItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.meta["url"]
        item['status'] = response.meta["status"]
        item['time'] = response.meta["time"]
        item['title'] = response.meta["title"]
        content = response.text
        r = re.compile(r'</?\w+[^>]*>', re.S)
        final_content = r.sub("", content).strip()
        item['content'] = final_content
        # print(item)
        yield item


