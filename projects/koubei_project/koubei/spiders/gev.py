# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GEVItem
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
import pymongo
import os

website='gev_fix'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
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

    def start_requests(self):
        request_list = list()
        for i in range(1, 140):
            url = "http://www.gev.org.cn/comp/news/list.do?compId=news_list-15476985505928450&cid=14&pageSize=6&currentPage=%d" % i
            request_list.append(scrapy.Request(url=url, headers=self.headers))
        return request_list


    def parse(self, response):
        articles = response.xpath("//*[@class='e_box e_ListBox-001 p_articles']")
        for article in articles:
            postdate = article.xpath("div[2]/div[1]/div[4]/div/div[2]/div/text()").extract_first()
            if postdate:
                postdate = postdate.strip()
            url = article.xpath("div[2]/div[1]/div[2]/a/@href").extract_first()
            meta = {
                "postdate":postdate,
            }
            yield scrapy.Request(url=response.urljoin(url), meta=meta, headers=self.headers, callback=self.parse_details)

    def parse_details(self, response):
        item = GEVItem()
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['title'] = response.xpath('//*[@class="e_title e_head-000 p_head "]/div/text()[2]').extract_first().strip()
        contents = response.xpath('//*[@class="js_infoDetail_content item_hide"]/div//p').extract()
        for content in contents:
            contents[contents.index(content)] = re.sub("<.*?>", '', content).strip()
        item['content'] = "\n".join(contents)
        item['postdate'] = response.meta["postdate"]
        imgs = response.xpath('//*[@class="js_infoDetail_content item_hide"]/div//img/@src').extract()
        item['imgs'] = json.dumps(imgs)


        page_id = str(re.findall("\d+", response.url)[0])
        os.makedirs("fix/" + page_id)

        for img in imgs:
            try:
                img_res = requests.request("get", url="http://www.gev.org.cn" + img, headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
                with open("fix/" + page_id + "/" + page_id + "_" + str(imgs.index(img)) + ".jpg", "ab") as f:
                    f.write(img_res.content)
                    f.close()
            except Exception as e:
                pass

        # print(item)
        yield item