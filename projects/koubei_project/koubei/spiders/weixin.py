# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import WeixinItem
import time
# from scrapy.conf import self.settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
# from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import pymongo

# from .. import settings

weixinname = settings["WEIXIN"]

website='new_weixin_%s' % weixinname

class CarSpider(scrapy.Spider):

    name=website
    # start_urls = [
    #     "https://bj.sp.anjuke.com/zu/p1/"
    # ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=self.settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["wx"]
        collection = db["msg_%s" % weixinname]

        res = collection.find()

        url_list = list()

        for row in res:
            if "app_msg_ext_info" in row["msg"]:
                url = row["msg"]["app_msg_ext_info"]["content_url"].replace("http", "https")
                title = row["msg"]["app_msg_ext_info"]["title"]
                digest = row["msg"]["app_msg_ext_info"]["digest"]
                meta = {
                    "title": title,
                    "digest": digest
                }
                if url:
                    url_list.append(scrapy.Request(url=url, meta=meta))
                for i in row["msg"]["app_msg_ext_info"]["multi_app_msg_item_list"]:
                    url = i["content_url"].replace("http", "https")
                    title = i["title"]
                    digest = i["digest"]
                    meta = {
                        "title": title,
                        "digest": digest
                    }
                    if url:
                        url_list.append(scrapy.Request(url=url, meta=meta))
        return url_list


    def parse(self, response):
        print(response.text)
        try:
            content = response.xpath("//*[@id='js_content']").extract()[0]
        except Exception as e:
            content = response.xpath("//*[@class='details']").extract()[0]
        r = re.compile(r'</?\w+[^>]*>', re.S)
        final_content = r.sub("", content).strip()
        print(final_content)

        item = WeixinItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item["content"] = final_content
        item["title"] = response.meta["title"]
        item["digest"] = response.meta["digest"]
        # item["publish_time"] = response.xpath("//*[@id='publish_time']/text()").extract_first()
        print(item)
        # yield item