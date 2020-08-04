# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import DiyidiandongPingce
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='diyidiandong_pingce'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://api.touchev.com:83/api/0190/index/index.do?jpushId=1507bfd3f79851701fd&deviceId=869622035270223&userId=&sss=b235a2d3468dd22be9a071cbf1016978&idx=0&first=no&appName=%E7%AC%AC%E4%B8%80%E7%94%B5%E5%8A%A8&lng=121.510961&network=wifi&naviId=12&networkOperator=CMCC&imei=869622035270223&deviceOsVer=7.0&deviceOs=android&appVer=1.9.2&tpToken=&page=1&lat=31.292386&channel=yingyongbao&appToken=&limit=20&deviceSysVar=RNE-AL00%7CHUAWEI']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
    #     self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
    #     super(KoubeiSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def start_requests(self):
        for i in range(1, 20):
            yield scrapy.Request(url="https://api.touchev.com:83/api/0190/index/index.do?jpushId=1507bfd3f79851701fd&deviceId=869622035270223&userId=&sss=b235a2d3468dd22be9a071cbf1016978&idx=0&first=no&appName=%E7%AC%AC%E4%B8%80%E7%94%B5%E5%8A%A8&lng=121.510961&network=wifi&naviId=12&networkOperator=CMCC&imei=869622035270223&deviceOsVer=7.0&deviceOs=android&appVer=1.9.2&tpToken=&page=" + str(i) + "&lat=31.292386&channel=yingyongbao&appToken=&limit=20&deviceSysVar=RNE-AL00%7CHUAWEI")

    def parse(self,response):
        articles = json.loads(response.text)
        for article in articles["data"]["list"]:
            data = {
                "appVer":"1.0",
                "targetId":str(article["subList"][0]["targetId"]),
                "targetType":str(article["subList"][0]["targetType"]),
            }
            yield scrapy.FormRequest(method="post", url="http://api.touchev.com:82/api/0130/article/detail", formdata=data, callback=self.parse_article)

    def parse_article(self, response):
        article_detail = json.loads(response.text)
        item = DiyidiandongPingce()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = str(article_detail["data"]["targetId"])
        item['title'] = article_detail["data"]["title"]
        item['h5Url'] = article_detail["data"]["h5Url"]
        item['htmlContent'] = article_detail["data"]["htmlContent"]
        item['summary'] = article_detail["data"]["summary"]

        # print(item)
        yield item