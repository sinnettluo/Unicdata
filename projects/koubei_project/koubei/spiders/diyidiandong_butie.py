# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import DiyidiandongButieItem
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='diyidiandong_butie5'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://car.d1ev.com/find/']

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

    def parse(self, response):
        brands = response.xpath("//*[@class='pingpai_content']/div[2]/ul/li")
        for brand in brands:
            brandname = brand.xpath("a/p/text()").extract_first()
            brandid = brand.xpath("a/p/@value").extract_first()
            url = brand.xpath("a/@href").extract_first()
            meta = {
                "brandname": brandname,
                "brandid": brandid,
            }
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)

    def parse_family(self, response):
        families = response.xpath("//*[@id='selCarResult']//*[@class='am-fl']")
        for family in families:
            familyname = family.xpath("a/p[1]/text()").extract_first()
            familyid = family.xpath("a/@href").re("\d+")[1]
            url = family.xpath("a/@href").extract_first()
            meta = {
                "familyname": familyname,
                "familyid": familyid,
            }
            meta = dict(meta, **response.meta)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_details)

    def parse_details(self, response):
        diandong = response.xpath("//*[@class='diandong']/text()").extract_first()
        butiejiage = response.xpath("//*[@class='am-fl wrapper_info']/ul/li/span/text()").extract_first()
        mileage = response.xpath("//*[@class='infocard']/div/div[3]/div/p[2]/text()").extract_first()

        models = response.xpath("//*[@id='Slide1']/ul/li")
        print(models)
        for model in models:
            item = DiyidiandongButieItem()
            item['diandong'] = diandong
            item['butiejiage'] = butiejiage
            item['mileage'] = mileage

            item['modelname'] = model.xpath("div[1]/span/text()").extract_first()
            item['ckg'] = model.xpath(""
                                      "").extract_first()
            item['gonglv'] = model.xpath("div[2]/ul[2]/li[2]/span/text()").extract_first()
            item['charge_time'] = model.xpath("div[2]/ul[2]/li[3]/span/text()").extract_first()
            item['fast_charge'] = model.xpath("div[2]/ul[2]/li[4]/span/text()").extract_first()

            item['guide_price'] = model.xpath("div[2]/ul[1]/li[1]/span/text()").extract_first()
            item['butiehoujiage'] = model.xpath("div[2]/ul[1]/li[2]/span/text()").extract_first()

            item['modelid'] = model.xpath("div[1]/a[1]/@modelid").extract_first()

            item['url'] = response.url
            item['status'] = model.xpath("div[1]/a[1]/@modelid").extract_first() + "-" + time.strftime('%Y-%m', time.localtime())
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

            item["brandname"] = response.meta["brandname"]
            item["brandid"] = response.meta["brandid"]
            item["familyname"] = response.meta["familyname"]
            item["familyid"] = response.meta["familyid"]

            # print(item)
            yield item