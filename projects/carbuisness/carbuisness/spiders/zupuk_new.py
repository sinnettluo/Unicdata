# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import w58officeitem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from carbuisness.items import ZupukItem

website='zupuk_new'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.zupuk.com/"
    ]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        # hrefs = response.xpath("//*[@class='part_div3']/a")
        # print(hrefs)
        # for href in hrefs:
        #     city_url = href.xpath("@href").extract_first()
        #     print(city_url)
        #     city_name = re.findall("^http://(.*?).zupuk.com/$", city_url)[0]
        #     yield scrapy.Request(url="http://%s.zupuk.com/shangpu/m-121n-100000/" % city_name, callback=self.parse_list)
        yield scrapy.Request(url="http://%s.zupuk.com/shangpu/m-121n-100000/" % "beijing", callback=self.parse_list)

    def parse_list(self, response):

        lis = response.xpath("//*[@id='ul_list']/li")
        for li in lis:
            shangpu_url = li.xpath("./p[2]/a/@href").extract_first()
            # address = re.findall("地址：(.*?)<", response.body)
            # if address:
            #     print(address[0])
            yield scrapy.Request(url=response.urljoin(shangpu_url), callback=self.parse_detail)

        nexts = response.xpath("//*[@class='next']/a")
        for next in nexts:
            if next.xpath("text()").extract_first() == u"下一页":
                detail_url = next.xpath("@href").extract_first()
                print(response.urljoin(detail_url))
                yield scrapy.Request(url=response.urljoin(detail_url), callback=self.parse_list)

    def parse_detail(self, response):
        item = ZupukItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["price"] = response.xpath("//div[@class='zhaozushow_left_content1']/div[2]/ul/li[1]/p[2]/span/text()").extract_first()
        item["area"] = response.xpath("//div[@class='zhaozushow_left_content1']/div[2]/ul/li[2]/p[2]/span/text()").extract_first()
        item["address"] = re.findall("<p style=\"width\:600px\;\">(.*?)<", response.body)
        if item["address"]:
            item["address"] = item["address"][0]
        item["type"] = response.xpath("//div[@class='zhaozushow_left_content1']/div[2]/ul/li[5]/p[2]/a/text()").extract_first()
        item["title"] = response.xpath("//div[@class='zhaozushow_left_content1']/div[2]/h1/text()").extract_first()
        item["store_id"] = response.xpath("//div[@class='zhaozushow_left_content1']/div[1]/p/span/text()").extract_first()
        item["status"] = response.url
        item["city"] = response.xpath("//span[@class='currentcity']/text()").extract_first()
        item['posttime'] = response.xpath("//div[@class='zhaozushow_left_content1_top']/p[3]/span/text()").extract_first()
        if not item['posttime']:
            item['posttime'] = response.xpath(
                "//div[@class='zhaozushow_left_content1_top']/p[2]/span/text()").extract_first()
        yield item
