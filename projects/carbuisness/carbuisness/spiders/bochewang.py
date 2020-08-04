# -*- coding: utf-8 -*-
"""
C2017-41
bochewang 博车网

"""
import scrapy
from carbuisness.items import BochewangCarItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='bochewang_car'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['http://bochewang.com.cn/AuctioningCar/Index/?t=636396123452239556']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        print "do parse"
        car_list = response.xpath('//div[@class="tab"]/div/div/a')
        for car_info in car_list:
            carurl_temp = car_info.xpath('@href').extract_first()
            carurl = response.urljoin(carurl_temp)
            yield scrapy.Request(carurl,callback=self.parse_middle1)

    def parse_middle1(self,response):
        print "do parse_middle1"
        car_list = response.xpath('//div[@class="content"]/div[@class="gd-item"]//tr/td[3]/a')
        for car_info in car_list:
            carurl_temp = car_info.xpath('@href').extract_first()
            carurl = response.urljoin(carurl_temp)
            yield scrapy.Request(carurl, callback=self.parse_info)

    def parse_info(self,response):
        print "do parse_car"
        item = BochewangCarItem()
        item['website'] = website
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        item['modelname'] = response.xpath(u'//tr/td[contains(text(),"车辆型号")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"车辆型号")]/following-sibling::td[1]/text()') else "-"

        item['license_plate_num'] = response.xpath(u'//tr/td[contains(text(),"车牌")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"车牌")]/following-sibling::td[1]/text()') else "-"

        item['subject_species'] = response.xpath(u'//tr/td[contains(text(),"标的种类")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"标的种类")]/following-sibling::td[1]/text()') else "-"

        item['displacement'] = response.xpath(u'//tr/td[contains(text(),"排量")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"排量")]/following-sibling::td[1]/text()') else "-"

        item['frame_number'] = response.xpath(u'//tr/td[contains(text(),"车架号")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"车架号")]/following-sibling::td[1]/text()') else "-"

        item['date_of_initial_arrival'] = response.xpath(u'//tr/td[contains(text(),"初登日期")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"初登日期")]/following-sibling::td[1]/text()') else "-"

        item['engine_number'] = response.xpath(u'//tr/td[contains(text(),"发动机号")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"发动机号")]/following-sibling::td[1]/text()') else "-"

        item['effective_annual_inspection'] = response.xpath(u'//tr/td[contains(text(),"年检有效期")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"年检有效期")]/following-sibling::td[1]/text()') else "-"

        item['purchase_price'] = response.xpath(u'//tr/td[contains(text(),"购置价")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"购置价")]/following-sibling::td[1]/text()') else "-"

        item['secondhand_ticket'] = response.xpath(u'//tr/td[contains(text(),"是否二手票")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"是否二手票")]/following-sibling::td[1]/text()') else "-"

        item['compulsory_insurance'] = response.xpath(u'//tr/td[contains(text(),"交强险")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"交强险")]/following-sibling::td[1]/text()') else "-"

        item['cause_of_loss'] = response.xpath(u'//tr/td[contains(text(),"损失原因")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"损失原因")]/following-sibling::td[1]/text()') else "-"

        item['vehicle_and_vessel_tax'] = response.xpath(u'//tr/td[contains(text(),"车船税")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"车船税")]/following-sibling::td[1]/text()') else "-"

        item['address'] = response.xpath(u'//tr/td[contains(text(),"暂存地")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"暂存地")]/following-sibling::td[1]/text()') else "-"

        item['nature'] = response.xpath(u'//tr/td[contains(text(),"性质")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"性质")]/following-sibling::td[1]/text()') else "-"

        item['mileage'] = response.xpath(u'//tr/td[contains(text(),"行驶里程")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"行驶里程")]/following-sibling::td[1]/text()') else "-"

        if response.xpath(u'//tr/td[contains(text(),"起拍价")]/following-sibling::td[1]/text()'):
            starting_price = response.xpath(u'//tr/td[contains(text(),"起拍价")]/following-sibling::td[1]/text()').extract_first()
            item['starting_price'] = re.findall(u"¥(\S+)", starting_price)[0]
        else:
            item['starting_price'] = "-"

        item['commission_rate'] = response.xpath(u'//tr/td[contains(text(),"佣金比例")]/following-sibling::td[1]/text()').extract_first() \
            if response.xpath(u'//tr/td[contains(text(),"佣金比例")]/following-sibling::td[1]/text()') else "-"

        item['supplementary'] = response.xpath(u'//div[@class="buy_left"]/div/h3[contains(text(),"备注")]/../div/text()').extract_first().strip() \
            if response.xpath(u'//div[@class="buy_left"]/div/h3[contains(text(),"备注")]/../div/text()') else "-"

        if response.xpath(u'//span[contains(text(),"当前价")]/text()'):
            at_the_present_price = response.xpath(u'//span[contains(text(),"当前价")]/text()').extract_first()
            item['price1'] = re.findall(u"¥(\S+)", at_the_present_price)[0]

        if response.xpath(u'//span[contains(text(),"当前价")]/span[contains(text(),"结束")]/text()'):
            sold_date = response.xpath(u'//span[contains(text(),"当前价")]/span[contains(text(),"结束")]/text()').extract_first()
            item['sold_date'] = re.findall(u"于(.*?)结束", sold_date)[0]
        else:
            item['sold_date'] = "-"

        bid_record = []
        bid_record_list = response.xpath('//table[@id="tbPriceHis"]//tr')
        for bid_record_base in bid_record_list:
            str1=''
            # bid_record['bidder'] = bid_record_base.xpath('td[1]/text()').extract_first()
            # bid_record['bid_time'] = bid_record_base.xpath('td[2]/text()').extract_first()
            # bid_record['bid_price'] = bid_record_base.xpath('td[3]/text()').extract_first()
            str1=str( bid_record_base.xpath('td[1]/text()').extract_first())+"-"+str(bid_record_base.xpath('td[2]/text()').extract_first())+"-"+str(bid_record_base.xpath('td[3]/text()').extract_first())
            bid_record.append(str1)

        item['bid_record']=bid_record

        yield item



