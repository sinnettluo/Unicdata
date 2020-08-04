# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import DianchebangItem
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='diandongbang_fix2'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://car.diandong.com/search/res/']

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
        lis = response.xpath("//*[@class='product-seach-list']")
        for li in lis:
            brandid = li.xpath("a[1]/@href").extract_first().split("/")[-1]
            brandname = li.xpath("a[1]/@title").extract_first()
            familyid = li.xpath("a[2]/@href").extract_first().split("/")[-1]
            familyname = li.xpath("a[2]/@title").extract_first()
            meta = {
                "brandid":brandid,
                "brandname": brandname,
                "familyid": familyid,
                "familyname": familyname,
            }
            # url = "http://car.diandong.com/duibi/chexi/%s" % familyid
            url = li.xpath("a[2]/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_middle)

    def parse_middle(self, response):
        url = response.xpath("/html/body/nav/div/a[2]/@href").extract_first()
        meta = response.meta
        yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_details)


    def parse_details(self, response):
        sum = len(response.xpath("//*[@class='select-wrap wrap']/table[1]/tbody/tr[1]/td"))
        for i in range(1, sum+1):
            item = DianchebangItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = response.url + "-" + str(i) + time.strftime('%Y-%m', time.localtime())
            item['familyid'] = response.meta["familyid"]
            item['familyname'] = response.meta["familyname"]
            item['brandid'] = response.meta["brandid"]
            item['brandname'] = response.meta["brandname"]
            item['factory'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[1]/td[%d]/text()" % (i+1)).extract_first()
            item['modelname'] = response.xpath("//*[@class='select-wrap wrap']/table[1]/tbody/tr[1]/td[%d]/div[1]/div[1]/p/text()" % (i+1)).extract_first()
            item['guideprice'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[1]/table[1]/tbody/tr[1]/td[%d]/text()" % (i+1)).extract_first()
            item['price'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[1]/table[1]/tbody/tr[2]/td[%d]/text()" % (i+1)).extract_first()
            item['type'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[3]/td[%d]/text()" % (i+1)).extract_first()
            item['length'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[4]/td[%d]/text()" % (i+1)).extract_first().split("*")[0]
            item['width'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[4]/td[%d]/text()" % (i+1)).extract_first().split("*")[1]
            item['height'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[4]/td[%d]/text()" % (i+1)).extract_first().split("*")[2]
            item['miles'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[2]/table[1]/tbody/tr[7]/td[%d]/text()" % (i+1)).extract_first()
            item['drivemode'] = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[7]/table[1]/tbody/tr[1]/td[%d]/text()" % (i+1)).extract_first()

            trs = response.xpath("//*[@class='param-wrap wrap']/div[2]/section[3]/table[1]/tbody/tr")
            for tr in trs:
                if tr.xpath("td[1]/text()").extract_first() == "座位数":
                    item['seats'] = tr.xpath("td[%d]/text()" % (i+1)).extract_first()
                if tr.xpath("td[1]/text()").extract_first() == "车身结构":
                    item['body'] = tr.xpath("td[%d]/text()" % (i+1)).extract_first()
                if tr.xpath("td[1]/text()").extract_first() == "车门数":
                    item['doors'] = tr.xpath("td[%d]/text()" % (i+1)).extract_first()

            yield item
            # print(item)