# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Chehang168Modellist
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

website='chehang168_modellist3'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://www.chehang168.com/index.php?c=tool&m=parameter"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

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


    # def start_requests(self):
    #
    #     request_list = []
    #
    #     connection = pymongo.MongoClient("192.168.1.94", 27017)
    #     db = connection["newcar"]
    #     collection = db["autohome_newcar"]
    #
    #     result = collection.distinct("autohomeid")
    #     for r in result:
    #         url = "https://carif.api.autohome.com.cn/car/getspecelectricbutie.ashx?_callback=GetSpecElectricSubsidy&speclist=%s&cityid=310100&type=1" % str(r)
    #         request_list.append(scrapy.Request(url, meta={"autohomeid": r}, callback=self.parse))
    #     return request_list


    def parse(self, response):

        brands = response.xpath("//*[@class='ch_choose w980']/select[1]/option")
        for brand in brands:
            brandurl = brand.xpath("@value").extract_first()
            brandname = brand.xpath("text()").extract_first()
            brandcode = brandurl.split("=")[-1]
            meta = {
                "brandname":brandname,
                "brandcode":brandcode,
            }
            yield scrapy.Request(url=response.urljoin(brandurl), meta=meta, callback=self.parse_family)

    def parse_family(self, response):
        fs = response.xpath("//*[@class='ch_choose w980']/select[2]/optgroup")
        for factory in fs:
            factoryname = factory.xpath("@value").extract_first()
            familys = factory.xpath("option")
            for family in familys:
                familyurl = family.xpath("@value").extract_first()
                familyname = family.xpath("text()").extract_first()
                familycode = familyurl.split("=")[-1]
                meta = {
                    "factoryname":factoryname,
                    "familyname": familyname,
                    "familycode": familycode,
                }
                meta = dict(meta, **response.meta)
                yield scrapy.Request(url=response.urljoin(familyurl), meta=meta, callback=self.parse_model)

    def parse_model(self, response):
        models = response.xpath("//*[@class='ch_choose w980']/select[3]/option")
        for model in models:
            modelurl = model.xpath("@value").extract_first()
            modelname = model.xpath("text()").extract_first()
            modelcode = modelurl.split("=")[-1]
            meta = {
                "modelname":modelname,
                "modelcode":modelcode,
            }
            meta = dict(meta, **response.meta)
            yield scrapy.Request(url=response.urljoin(modelurl), meta=meta, callback=self.parse_config)

    def parse_config(self, response):
        item = Chehang168Modellist()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        item['brandname'] = response.meta['brandname']
        item['brandcode'] = response.meta['brandcode']
        # item['factoryname'] = response.meta['factoryname']
        item['familyname'] = response.meta['familyname']
        item['familycode'] = response.meta['familycode']
        # item['modelname'] = response.meta['modelname']
        item['modelcode'] = response.meta['modelcode']

        # item['modelname'] = response.xpath("//table[@class='ch_patb']/tr[3]/td[2]/text()").extract_first()
        # item['import_type'] = response.xpath("//table[@class='ch_patb']/tr[4]/td[2]/text()").extract_first()
        # item['guide_price'] = response.xpath("//table[@class='ch_patb']/tr[5]/td[2]/text()").extract_first()
        # item['factoryname'] = response.xpath("//table[@class='ch_patb']/tr[6]/td[2]/text()").extract_first()
        # item['level'] = response.xpath("//table[@class='ch_patb']/tr[7]/td[2]/text()").extract_first()
        # item['engine'] = response.xpath("//table[@class='ch_patb']/tr[8]/td[2]/text()").extract_first()
        # item['gearbox'] = response.xpath("//table[@class='ch_patb']/tr[9]/td[2]/text()").extract_first()
        # item['pailiang'] = response.xpath("//table[@class='ch_patb']/tr[10]/td[2]/text()").extract_first()
        # item['length'] = response.xpath("//table[@class='ch_patb']/tr[11]/td[2]/text()").extract_first().split("*")[0]
        # item['width'] = response.xpath("//table[@class='ch_patb']/tr[11]/td[2]/text()").extract_first().split("*")[1]
        # item['height'] = response.xpath("//table[@class='ch_patb']/tr[11]/td[2]/text()").extract_first().split("*")[2]
        # item['body'] = response.xpath("//table[@class='ch_patb']/tr[12]/td[2]/text()").extract_first()
        # item['jinqixingshi'] = response.xpath("//table[@class='ch_patb']/tr[36]/td[2]/text()").extract_first()
        # item['fuel_type'] = response.xpath("//table[@class='ch_patb']/tr[50]/td[2]/text()").extract_first()
        # item['emission'] = response.xpath("//table[@class='ch_patb']/tr[55]/td[2]/text()").extract_first()
        # item['drive_mode'] = response.xpath("//table[@class='ch_patb']/tr[61]/td[2]/text()").extract_first()
        # item['zhouju'] = response.xpath("//table[@class='ch_patb']/tr[21]/td[2]/text()").extract_first()
        # item['doors'] = response.xpath("//table[@class='ch_patb']/tr[28]/td[2]/text()").extract_first()
        # item['seats'] = response.xpath("//table[@class='ch_patb']/tr[29]/td[2]/text()").extract_first()


        rownames = response.xpath("//table[@class='ch_patb']/tr/td[1]/text() | //table[@class='ch_patb']/tr/td[1]/b/text()").extract()
        for rowname in rownames:
            if rowname == "车型名称":
                item['modelname'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "进口类型":
                item['import_type'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "厂商指导价(元)":
                item['guide_price'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "厂商":
                item['factoryname'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "级别":
                item['level'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "发动机":
                item['engine'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "变速箱":
                item['gearbox'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "排量(L)":
                item['pailiang'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "长度(mm)":
                item['length'] = \
                response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "宽度(mm)":
                item['width'] = \
                response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "高度(mm)":
                item['height'] = \
                response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "车身结构":
                item['body'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "进气形式":
                item['jinqixingshi'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "燃料形式":
                item['fuel_type'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "环保标准":
                item['emission'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "驱动方式":
                item['drive_mode'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "轴距(mm)":
                item['zhouju'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "车门数(个)":
                item['doors'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()
            if rowname == "座位数(个)":
                item['seats'] = response.xpath("//table[@class='ch_patb']/tr["+str(rownames.index(rowname) + 2)+"]/td[2]/text()").extract_first()




        # print(item)
        yield item


