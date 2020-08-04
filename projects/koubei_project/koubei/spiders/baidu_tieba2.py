# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import TiebaItem
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
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

name = {'jilixinnengyuan': '吉利新能源'}

for ename in name:
    website = 'baidu_tieba_' + ename


class CarSpider(scrapy.Spider):
    name = website
    start_urls = []

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 800000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

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
        for ename in name:
            for i in range(400):
                url = "http://tieba.baidu.com/f?ie=utf-8&kw=%s&pn=%d" % (name[ename], i * 50)
                urls.append(scrapy.FormRequest(method="post", url=url))
        return urls

    def parse(self, response):

        threads = response.xpath("//*[@class=' j_thread_list clearfix']")
        for thread in threads:
            title = thread.xpath(".//*[@class='j_th_tit ']/text()").extract_first().strip()
            url = thread.xpath(".//*[@class='j_th_tit ']/@href").extract_first()
            data = json.loads(thread.xpath("@data-field").extract_first())
            meta = {
                "title": title,
                "id": data["id"]
            }
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_post)

    def parse_post(self, response):

        anchors = response.xpath("//a")
        for anchor in anchors:
            if anchor.xpath("text()").extract_first() == "下一页":
                yield scrapy.Request(url=response.urljoin(anchor.xpath("@href").extract_first()), meta=response.meta,
                                     callback=self.parse_post)

        posts = response.xpath("//*[contains(@class, 'j_l_post')]")
        # posts = response.xpath("//*[@class='l_post j_l_post l_post_bright  ']")
        for post in posts:
            item = TiebaItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["content"] = post.xpath(".//*[contains(@class,'j_d_post_content')]/text()").extract_first().strip()

            item["id"] = response.meta["id"]
            item["title"] = response.meta["title"]

            data = json.loads(post.xpath("@data-field").extract_first())
            item["post_id"] = data["content"]["post_id"]
            item["post_date"] = data["content"]["date"] if "post_date" in data["content"] else post.xpath(
                "//*[@class='post-tail-wrap']/span[4]/text()").extract_first()
            item["user_id"] = data["author"]["user_id"] if "user_id" in data["author"] else "999999"
            item["author_name"] = data["author"]["user_name"]
            item["author_sex"] = data["author"]["user_sex"] if "user_sex" in data["author"] else "4"

            item["status"] = str(item["post_id"])
            yield item
