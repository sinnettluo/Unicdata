# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import CaizhengbuItem
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

website='che300'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/",
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
        tds = response.xpath("//*[@class='ZIT']/tr/td")
        for td in tds:
            title = td.xpath("a/text()").extract_first()
            time = td.xpath("text()[3]").extract_first().strip()
            url = td.xpath("a/@href").extract_first()
            meta = {"time":time, "title":title}
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_article)


        if not re.findall("\d+", response.url):
            page_num = int(re.findall("createPageHTML\((\d+)\, \d+\, \"index\"\, \"htm\"\)", response.text, re.S)[0])
            if page_num > 1:
                for i in range(2, page_num+1):
                    next_url = response.url + "index_%d.html" % (i-1)
                    yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_article(self, response):
        item = CaizhengbuItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['time'] = response.meta["time"]
        item['title'] = response.meta["title"]
        try:
            content = response.xpath("//div[@class='TRS_Editor']/div[@class='TRS_Editor']").extract()[0]
        except Exception as e:
            try:
                content = response.xpath("//div[@class='TRS_Editor']").extract()[0]
            except Exception as e:
                # try:
                #     content = response.xpath("//*[@class='font_t_pai']").extract()[0]
                # except Exception as e:
                try:
                    content = response.xpath("//div[@class='Custom_UnionStyle']").extract()[0]
                except Exception as e:
                    content = ''.join(response.xpath("//p[@class='Custom_UnionStyle']/text()").extract())
        r = re.compile(r'</?\w+[^>]*>', re.S)
        final_content = r.sub("", content).strip()
        item['content'] = final_content
        yield item
        # print(item)