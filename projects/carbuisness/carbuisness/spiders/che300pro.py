# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import che300proItem
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

website='che300pro_new'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://www.che300.com"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        citys = response.xpath("//*[@class='ucarselecttype_pinpaibottom_ul select_province']/p")
        city_num_list = []
        for city in citys:
            city_num_list.append(city.xpath("@id").extract_first())
        print(city_num_list)

        sign_list = ['8FE16C101A8D5D52', 'D2994335257466F6', '418AFDBBA32CBBDF', 'FB0B58176498D9E8', 'DA0C7D9DFF49DF2D', 'D42CBB6B49FB9046', '68BBDBC81E59DC96', 'BBCFAB376A4CCA9A', '531A8FCEBDB5053A', '2F19CE9FE5E0A6D6', '5B37989522ACF36E', 'B2C8E3AF9E2FC970', '115A2369F15CF572', 'C27F4F3808440EC8', '0F0F27F540A64593', 'F54B7D48D81B78AD', '00D2BD6A369A14C5', '8949A30ED3612D13', 'D4F89AD2287273A6', '88E2348E23CEC145', 'F575B54730B871FA', '8E5391098CA01E0D', 'F4100B9614900E66', 'BC0AC96C320F2843', '7DD8EF5B3F877C5F', '8EDA12888FC5A480', '563142703B0E2A76', '7083591A7DCC8972', 'ED2CF14859D3E864', 'AF176A7BB35E3D97', '6179F72FEBA71CD1', '42EAEC2DFB7BE312', 'BEDB7B081AD5C705', '867C1C79885BE62E', '358E21C8D5238F69', '7A897A46388C06BE', 'A1411C1B7C6C9315', 'CC53302DD8703E67', '10093ACE4489025B', '16CF71EFDB19E1FD', '965B666B76FA9069', 'A933834BBA913906', '0179DA6AB8074ED2', '61F9ABC1F15D28E7', '155694AA669DDD13', 'F108304B2063D332', '53F9300CBB17405A', '1F45CB40D27A4510', '718541B974A7F343', '957FD6A9639FA0FB', 'D45650F7C71F7EA7', '295C89D00D16560C']

        for city_num in city_num_list:
            for i in range(0, len(sign_list)):
                data = {
                    "page_size": "20",
                    "sort": '{"score": "desc"}',
                    "app_type": 'android_price',
                    "sign": sign_list[i],
                    "city_id": city_num,
                    "page": str(i+1),
                }
                print(data)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                }
                yield scrapy.FormRequest(url="http://dingjia.che300.com/demo/dealer/index_new", meta={'city_id':city_num}, formdata=data, headers=headers, callback=self.parse_dshop)


    def parse_dshop(self, response):
        print(response.body)
        obj = json.loads(response.body)
        dshops = obj["data"]["record"]
        for dshop in dshops:
            item = che300proItem()
            item['city']= response.meta['city_id']
            item['dealer_id'] = dshop["dealer_id"]
            item['dealer_name'] = dshop["dealer_name"]
            item['score'] = dshop["score"]
            item['address'] = dshop["address"]
            item['detail_url'] = dshop["detail_url"]
            item['onsale_count'] = dshop["onsale_count"]
            item['onsale_brands'] = dshop["onsale_brands"]
            item['is_top'] = dshop["is_top"]
            item['is_certified'] = dshop["is_certified"]
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = str(dshop)
            m2 = hashlib.md5()
            m2.update(item['status'])
            item['status'] = m2.hexdigest()
            yield item