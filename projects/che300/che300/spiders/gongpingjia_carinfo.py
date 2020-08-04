# -*- coding: utf-8 -*-
import scrapy
from ..items import gongpingjia_carinfo
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import random
import json
import datetime
from datetime import date

website = 'gongpingjia_carinfo'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["jingzhengu.com"]

    start_urls = [
        'http://sh.gongpingjia.com/meta-data/new/get-brand/'
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 2000000000
        self.counts = 0
        self.today = date.today()
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #pro_city select
    #brandselect
    def parse(self,response):
        data = json.loads(response.xpath('//p/text()').extract_first())
        if data['status'] == "success":
            temp = data['brand_source']
            for da in temp:
                for d in da['list']:
                    brandname = d['name']
                    brandname_en = d['slug']
                    brandlogo = d['logo']
                    metadata={"brandname":brandname,"brandname_en":brandname_en}
                    url = "http://sh.gongpingjia.com/meta-data/new/get-model/?brand="+brandname_en
                    yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_familyinfo,dont_filter=True)

    def parse_familyinfo(self,response):
        meta = response.meta['metadata']
        data = json.loads(response.xpath('//p/text()').extract_first())
        if data['status'] == "success":
            temp = data['model_source']
            for da in temp:
                for d in da['list']:
                    factoryname = d['mum']
                    familyname = d['name']
                    familyname_en = d['slug']
                    fmailylogo = d['logo']
                    familydata={"factoryname":factoryname,"familyname":familyname,
                              "familyname_en":familyname_en,"fmailylogo":fmailylogo}
                    metadata=dict(familydata,**meta)
                    url = "http://sh.gongpingjia.com/meta-data/new/get-model-detail/?model="+familyname_en
                    yield scrapy.Request(url,meta={"metadata":metadata},callback=self.parse_vehileinfo,dont_filter=True)

    def parse_vehileinfo(self,response):
        meta = response.meta['metadata']
        data =json.loads(response.xpath("//p/text()").extract_first())
        if data['status'] == "success":
            temp = data['model_detail']
            for da in temp:
                for d in da['list']:
                    emission = d['emission_standard']
                    saledescid = d['detail_model_slug']
                    max_reg_year = d['max_reg_year']
                    min_reg_year = d['min_reg_year']
                    saledesc = d['model_detail']
                    guideprice = d['price_bn']
                    geartype = d['transmission']
                    output = d['volume']
                    makeyear = d['year']
                    vehiledata = {"emission": emission, "saledescid": saledescid,"max_reg_year":max_reg_year,
                                "min_reg_year":min_reg_year,"saledesc":saledesc,"guideprice":guideprice,
                                "geartype":geartype,"output":output,"makeyear":makeyear}

                    metadata=dict(vehiledata,**meta)
                    url = "http://sh.gongpingjia.com/api/city-group-by-alphabet/"
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.price_url,dont_filter=True)

    def price_url(self,response):
        meta = response.meta['metadata']
        brandname_en = meta['brandname_en']
        familyname_en = meta['familyname_en']
        saledescid = meta['saledescid']
        max_reg_year = meta['max_reg_year']
        min_reg_year = meta['min_reg_year']

        data = json.loads(response.xpath('//p/text()').extract_first())
        if data['status'] == 'success':
            for value in data['cities']:
                for i in data['cities'][value]:
                    city_py = i['pinyin']
                    city = i['name']
                    cityid = i['parent']
                    cityslug = i['slug']
                    url = "http://"+ cityslug +".gongpingjia.com/evaluate/eval-report/detail_param/"+ \
                           brandname_en +"/"+ familyname_en +"/"+ saledescid +"/"
                    sourceinfo = {"city_py": city_py, "city": city, "cityid": cityid, "cityslug":cityslug}
                    metadata = dict(sourceinfo, **meta)
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_priceinfo,dont_filter=True)

    def parse_priceinfo(self,response):
        # count
        print "response.url", response.url
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"
        # # item loader
        item = gongpingjia_carinfo()

        meta = response.meta['metadata']
        # print meta
        item["geartype"] = meta['geartype']
        item["makeyear"] = meta['makeyear']
        item["guideprice"] = meta['guideprice']
        item["emission"] = meta['emission']
        item["familyname_en"] = meta['familyname_en']
        item["min_reg_year"] = meta['min_reg_year']
        item["saledesc"] = meta['saledesc']
        item["city_py"] = meta['city_py']
        item["fmailylogo"] = meta['fmailylogo']
        item["brandname_en"] = meta['brandname_en']
        item["city"] = meta['city']
        item["familyname"] = meta['familyname']
        item["max_reg_year"] = meta['max_reg_year']
        item["cityid"] = meta['cityid']
        item["saledescid"] = meta['saledescid']
        item["factoryname"] = meta['factoryname']
        item["output"] = meta['output']
        item["brandname"] = meta['brandname']
        #
        item["cityslug"] = meta["cityslug"]
        #
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        #
        item["datasave"] = response.xpath('//div[@id="content"]').extract_first()

        item['status'] = md5(response.url).hexdigest()
        yield item



