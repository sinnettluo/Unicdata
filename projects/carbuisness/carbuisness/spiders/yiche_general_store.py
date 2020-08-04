# -*- coding: utf-8 -*-
"""

C2017-43-2
易车 经销商(包括4S店和综合店)

"""
import scrapy
from carbuisness.items import YicheGeneralStore
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website ='yiche_general_store_with_company'

class CarSpider(scrapy.Spider):
    name = website

    #选择城市，从这个入口获得城市信息
    start_urls = [
        'http://api.admin.bitauto.com/city/getcity.ashx?callback=City_Select._$JSON_callback.$JSON&requesttype=json&bizCity=1',
    ]

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 80000

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self, response):
        htmlstr = response.body
        in_json = htmlstr[34:-2]
        with open("a.txt", "w") as f:
            f.write(in_json)
        citylist = json.loads(in_json)
        for city in citylist:
            citycode = city['cityPinYin']
            cityid = city['cityId']
            cityname = city['cityName']
            # http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&objid=0&citycode=beijing%2F&cityid=201
            url = "http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand&objid=0&citycode=" \
                  + citycode + "%2F&cityid=" + cityid
            metadata = {"cityname":cityname}
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)


    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        urllist = re.findall('url:"/(.*?)/"', response.body)
        for urlbase in urllist:
            # http://dealer.bitauto.com/beijing/mercedesbenz/
            url = "http://dealer.bitauto.com/" + urlbase
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)

    def parse_middle2(self, response):
        metadata = response.meta['metadata']
        urllist = response.xpath('//div[@class="main-inner-section sm dealer-box"]//div[@class="col-xs-6 left"]/h6/a')
        for urlbase in urllist:
            url = urlbase.xpath('@href').extract_first()
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_info, dont_filter=True)
        next = response.xpath('//div[@class="pagination"]//a[@class="next_on"]/@href')
        if next:
            nextbase = next.extract_first()
            nexturl = response.urljoin(nextbase)
            print(nexturl)
            yield scrapy.Request(nexturl, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)

    def parse_info(self, response):
        metadata = response.meta['metadata']
        item = YicheGeneralStore()

        item['city'] = metadata['cityname']
        # http://dealer.bitauto.com/100019493/?leads_source=p036001
        if  response.xpath('//div[@class="jxs_info index_card"]/h2/strong/text()'):
            item['name'] = response.xpath('//div[@class="jxs_info index_card"]/h2/strong/text()').extract_first()  # 店名
        else:
            item['name'] = "-"

        if response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"级别")]/../div[1]/text()'):
            item['star_level'] = response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"级别")]/../div[1]/text()').extract_first() # 级别
        else:
            item['star_level'] = "-"

        if  response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"电话")]/../div[1]/em/@data-tel'):
            item['phone'] = response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"电话")]/../div[1]/em/@data-tel').extract_first()  # 电话
        else:
            item['phone'] = "-"

        if response.xpath('//meta[@name="description"]/@content'):
            phone_400 = response.xpath('//meta[@name="description"]/@content').extract_first()
            try:
                item['phone_400'] = re.findall(u"【电话：(.*?)】", phone_400)[0] # 400电话
            except:
                item['phone_400'] = "-"
        else:
            item['phone_400'] = "-"

        if response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"官网")]/../div[1]/a/@href'):
            item['official_url'] = response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"官网")]/../div[1]/a/@href').extract_first() # 官网
        else:
            item['official_url'] = "-"

        if  response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"地址")]/../div[1]/text()'):
            item['address'] = response.xpath(u'//div[@class="jxs_info index_card"]//ul[@class="info_list"]/li/b[contains(text(),"地址")]/../div[1]/text()').extract_first().replace("[","").replace("]","") # 地址
        else:
            item['address'] = "-"

        mainBrand = []
        for unit in response.xpath('//div[@class="sbox zy_sbox"]//dd'):
            brand_first = unit.xpath('h4/text()').extract_first()
            brand_second_base = unit.xpath('p/a/text()').extract()
            brand_second = ""
            flag = 0
            for x in brand_second_base:
                if flag:
                    brand_second += "+" + x
                else:
                    brand_second = x
                    flag = 1
            brand = {brand_first : brand_second}
            mainBrand.append(brand)

        if mainBrand:
            item['main_brand'] = mainBrand
        else:
            item['main_brand'] = "-"

        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = item['name'] + response.url  #
        item['company'] = response.xpath("//div[@class='inheader']/div[2]/h1/text()").extract_first()

        yield item
