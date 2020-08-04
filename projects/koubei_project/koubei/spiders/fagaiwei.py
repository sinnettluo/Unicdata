# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import FagaiweiItem
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

website='fagaiwei'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.ndrc.gov.cn/zcfb/zcfbl/",
        "http://www.ndrc.gov.cn/zcfb/gfxwj/",
        "http://www.ndrc.gov.cn/zcfb/zcfbgg/",
        "http://www.ndrc.gov.cn/zcfb/zcfbghwb/",
        "http://www.ndrc.gov.cn/zcfb/zcfbtz/",
        "http://www.ndrc.gov.cn/zcfb/jd/",
        "http://www.ndrc.gov.cn/zcfb/zcfbqt/",
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.type = {
            "http://www.ndrc.gov.cn/zcfb/zcfbl/": "发展改革委令",
            "http://www.ndrc.gov.cn/zcfb/gfxwj/": "规范性文件",
            "http://www.ndrc.gov.cn/zcfb/zcfbgg/": "公告",
            "http://www.ndrc.gov.cn/zcfb/zcfbghwb/": "规划文本",
            "http://www.ndrc.gov.cn/zcfb/zcfbtz/": "通知",
            "http://www.ndrc.gov.cn/zcfb/jd/": "解读",
            "http://www.ndrc.gov.cn/zcfb/zcfbqt/": "其他",
        }

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
        if response.url in self.type:
            c_type = self.type[response.url]
        else:
            c_type = response.meta["type"]
        lis = response.xpath("//li[@class='li']")
        for li in lis:
            time = li.xpath("font/text()").extract_first()
            url = response.urljoin(li.xpath("a/@href").extract_first())
            print(url)
            meta = {
                "type": c_type,
                "time": time
            }
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_article)

        page_num = int(re.findall("createPageHTML\((\d+)\, \d+\, \"index\"\, \"html\"\)", response.text, re.S)[0])
        if page_num > 1 and not re.findall("\d+", response.url):
            for i in range(2, page_num+1):
                next_url = response.url + "index_%d.html" % (i-1)
                yield scrapy.Request(url=next_url, meta={"type":c_type}, callback=self.parse)


    def parse_article(self, response):
        item = FagaiweiItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url
        item['type'] = response.meta["type"]
        try:
            content = response.xpath("//*[@class='TRS_Editor']").extract()[0]
        except Exception as e:
            content = response.xpath("//*[@class='txt1']").extract()[0]
        r = re.compile(r'</?\w+[^>]*>', re.S)
        final_content = r.sub("", content).strip()
        # print(final_content)
        item['content'] = final_content
        item['time'] = response.meta["time"]
        yield item
        # print(item)

