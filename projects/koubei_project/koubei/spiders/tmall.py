# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import TMallItem
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

website='tmall'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.cate_dict = {
            "https://coll.jd.com/list.html?sub=46994":"京东保养",
            "https://list.jd.com/list.html?cat=6728,6742,11849":"汽机油",
            "https://list.jd.com/list.html?cat=6728,6742,9248":"轮胎",
            "https://list.jd.com/list.html?cat=6728,6742,11850":"添加剂",
            "https://list.jd.com/list.html?cat=6728,6742,6756":"防冻液",
            "https://coll.jd.com/list.html?sub=23851":"滤清器",
            "https://list.jd.com/list.html?cat=6728,6742,9971":"蓄电池",
            "https://list.jd.com/list.html?cat=6728,6742,13992":"变速箱油/滤",
            "https://list.jd.com/list.html?cat=6728,6742,6766":"雨刷",
            "https://coll.jd.com/list.html?sub=23867":"刹车片/盘",
            "https://list.jd.com/list.html?cat=6728,6742,6767":"火花塞",
            "https://coll.jd.com/list.html?sub=23843":"车灯",
            "https://list.jd.com/list.html?cat=6728,6742,11951":"轮毂",
            "https://list.jd.com/list.html?cat=6728,6742,6769":"维修配件",
            "https://list.jd.com/list.html?cat=6728,6742,13246":"汽车玻璃",
            "https://list.jd.com/list.html?cat=6728,6742,13243":"减震器",
            "https://list.jd.com/list.html?cat=6728,6742,13244":"正时皮带",
            "https://list.jd.com/list.html?cat=6728,6742,13245":"汽车喇叭",
            "https://list.jd.com/list.html?cat=6728,6742,6795":"汽修工具",
            "https://list.jd.com/list.html?cat=6728,6742,12406":"改装配件",
            "https://coll.jd.com/list.html?sub=42052":"原厂件",
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        cookies = {
            "cna":"tZo0FU3KmiQCAWVRCXg2gCnA",
            "cookie1":"B0OlxyYi7690cF2AeVP6zfuT2qGCyMNyjIRIa%2Bhv9Ms%3D",
            "cookie2":"114afe2efd0dd8a575c5b220fb70e60f",
        }
        return [scrapy.Request(url="https://list.tmall.com/search_product.htm?q=%D3%EA%B9%CE%C6%F7", cookies=cookies)]


    # def parse(self, response):
    #     print(response.text)
    #     urls = response.xpath("//*[@clstag='h|keycount|head|category_09d05']/a/@href").extract()
    #     print(urls)
    #     for url in urls:
    #         meta = {
    #             "category": url.xpath("../text()").extract_first()
    #         }
    #         yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_product)

    def parse(self, response):

        next = response.xpath("//*[@class='ui-page-next']")
        if next:
            cookies = {
                "cna":"tZo0FU3KmiQCAWVRCXg2gCnA",
                "cookie1":"B0OlxyYi7690cF2AeVP6zfuT2qGCyMNyjIRIa%2Bhv9Ms%3D",
                "cookie2":"114afe2efd0dd8a575c5b220fb70e60f",
            }
            yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), cookies=cookies, callback=self.parse)


        # products = response.xpath("//*[@class='product  ']")
        #
        # for product in products:
        #
        #     item = TMallItem()
        #     item['url'] = response.url
        #     item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        #     item['title'] =  product.xpath("div/*[@class='productTitle']/a/@title").extract_first()
        #     item['price'] = product.xpath("div/*[@class='productPrice']/em/@title").extract_first()
        #     item['status'] = product.xpath("@data-id").extract_first()
        #
        #     print(item)