# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import WeixiuchangShanghaiItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='weixiuchang_shanghai'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://www.shanghaiqixiu.org/repair/micro/search/company?fl=pic,type,sid,name,addr,tel,distance,kw,lon,lat,bizScope,brand,category,grade,tag&q=&page=0,4&sort=_score%20desc,distance&point=31.2867,121.50446&fq=status:1+AND+type:164+AND+-kw:4s']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # super(KoubeiSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def start_requests(self):
        urls = []
        for i in range(676):
            url = "https://www.shanghaiqixiu.org/repair/micro/search/company?fl=pic,type,sid,name,addr,tel,distance,kw,lon,lat,bizScope,brand,category,grade,tag&q=&page="+str(i)+",4&sort=_score%20desc,distance&point=31.2867,121.50446&fq=status:1+AND+type:164+AND+-kw:4s"
            urls.append(scrapy.Request(url=url))
        return urls

    def parse(self,response):
        res = json.loads(response.text)
        for chang in res["content"]:
            item = WeixiuchangShanghaiItem()
            item['url'] = response.url
            item['status'] = chang["sid"]
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['category'] = chang["category"] if "category" in chang else "-"
            item['name'] = chang["name"] if "name" in chang else "-"
            item['addr'] = chang["addr"] if "addr" in chang else "-"
            item['lon'] = chang["lon"] if "lon" in chang else "-"
            item['sid'] = chang["sid"] if "sid" in chang else "-"
            item['scope'] = chang["bizScope"] if "bizScope" in chang else "-"
            item['grade'] = chang["grade"] if "grade" in chang else "-"
            item['tel'] = chang["tel"] if "tel" in chang else "-"
            item['tag'] = chang["tag"] if "tag" in chang else "-"
            item['brand'] = chang["brand"] if "brand" in chang else "-"
            item['lat'] = chang["lat"] if "lat" in chang else "-"
            # print(item)
            yield item




