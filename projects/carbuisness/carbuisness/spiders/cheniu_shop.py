# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import cheniuShopItem
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

website='cheniu_shop'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://niu.souche.com/filter_screening?parameter=area&parent_code=&national=0"
    ]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self, response):
        provice = json.loads(response.body)
        for item in provice['data']['select_list']:
            for row in item['rows']:
                url = "https://niu.souche.com/filter_screening?parameter=area&parent_code=%s&national=0" % row['code']
                yield scrapy.Request(url=url, meta={'province_code':row['code']}, callback=self.parse_sub_area)

    def parse_sub_area(self, response):
        sub_area = json.loads(response.body)
        for item in sub_area['data']['select_list']:
            for row in item['rows']:
                url = "https://niu.souche.com/yellowpage/markets?token=71520225864334699&cityName=&cityCode=%s" % row['code']
                print(url)
                yield scrapy.Request(url=url, meta={'province_code':response.meta['province_code'], 'sub_area_code':row['code']}, callback=self.parse_district)

    def parse_district(self, response):
        district = json.loads(response.body)
        for item in district['data']['select_list']:
            for row in item['rows']:
                if row['id'].find("-0") < 0:
                    page_count = row['shopCount']/20 + 1
                    if page_count > 250:
                        page_count = 250
                    for i in range(page_count + 1):
                        url = "https://niu.souche.com/yellowpage/shops?id=%s&page=%d&size=20&token=71520225864334699" % (row['id'], i+1)
                        print(url)

                        with open("blm/carbusiness/cheniu_shop.blm") as f:
                            content = f.read()
                            url_list = content.split("\n")
                            f.close()

                        for j in range(20):
                            i = md5(url+"-"+str(j)).hexdigest()
                            if i not in url_list:
                                yield scrapy.Request(url=url, meta={'index':j, 'province_code':response.meta['province_code'], 'sub_area_code':response.meta['sub_area_code'], 'district_code':row['id']}, callback=self.parse_list)
                                break
                            else:
                                print("old url...for %d" % j)

    def parse_list(self, response):
        shops = json.loads(response.body)
        for shop in shops['data']['list']:
            if shops['data']['list'].index(shop) >= response.meta['index']:
                print("yes %d" % shops['data']['list'].index(shop))
                item = cheniuShopItem()
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['url'] = response.url
                item['status'] = response.url + "-" + str(shops['data']['list'].index(shop))
                item['user_mobile'] = shop['user_mobile']
                item['user_name'] = shop['user_name']
                item['user_avatar'] = shop['user_avatar']
                item['user_identity_plate'] = shop['user_identity_plate']['url'] if shop['user_identity_plate'].has_key('url') else "-"
                item['shop_code'] = shop['shop_code']
                item['shop_name'] = shop['shop_name']
                item['shop_identity_plate'] = shop['shop_identity_plate']['url'] if shop['shop_identity_plate'].has_key('url') else "-"
                item['address'] = shop['address']
                item['protocol'] = shop['protocol']
                item['for_sale'] = shop['for_sale']
                item['shop_identity_status'] = shop['shop_identity_status']
                item['shop_tags'] = shop['shop_tags']
                item['province_code'] = response.meta['province_code']
                item['sub_area_code'] = response.meta['sub_area_code']
                item['district_code'] = response.meta['district_code']
                yield item









