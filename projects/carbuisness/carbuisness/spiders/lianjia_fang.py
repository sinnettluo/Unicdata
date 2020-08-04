# -*- coding: utf-8 -*-
"""

C2017-41-2
二手房和新房分成两个程序，这是新房

"""
import scrapy
from carbuisness.items import LianjiaFangItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
import carbuisness.mydial
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver
website='lianjia_fang'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://bj.lianjia.com/']
    # custom_settings = {
    #     "DOWNLOADER_MIDDLEWARES":{
    #         'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,
    #     }
    # }



    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000
        self.city_none = ["dg",]
        self.city_type2 = ["hk", "ls", "qh", "san", "wc", "wn", "you"]

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        self.browser.set_page_load_timeout(8)
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    #
    #   这里分成两种不同类型的楼盘
    #   两种示例：
    #   http://you.lianjia.com/san
    #   http://sh.fang.lianjia.com
    #


    def parse(self, response):

        yield scrapy.Request("http://you.lianjia.com/", callback=self.parse_middle1_type2)

        print "do parse"
        citylist = response.xpath('//div[@class="fc-main clear"]//ul/li/div/a')
        if citylist:
            print "------------strat--------------"
        else:
            print "------------end--------------"
        for href in citylist:
            city = href.xpath('text()').extract_first()
            # proxy = getProxy()
            # metadata = {"city" : city}#, "proxy":proxy}
            urlbase = href.xpath('@href').extract_first()
            # cityfront = re.findall("(.*?)\.lianjia", urlbase)[0]
            # citypinyin = re.findall("://(.*?)\.", urlbase)[0]
            # if citypinyin not in self.city_none:
            #     if citypinyin not in self.city_type2:
            if urlbase.find("you.lianjia.com") < 0:
                url = urlbase + "loupan/"
                # addmeta = {"page": "1"}
                # metadata = dict(metadata, **addmeta)
                # yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle1, dont_filter=True)
                yield scrapy.Request(url, meta={"city": city}, callback=self.parse_middle1, dont_filter=True)
            # else:
            #     url = urlbase
            #     yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle1_type2,dont_filter=True)


    def parse_middle1(self, response):
        # print(response.body)
        # metadata = response.meta['metadata']
        areas = response.xpath('//ul[@class="resblock-list-wrapper"]/li/a')
        print(areas)
        for href in areas:
            area = href.xpath('@href').extract_first()
            url = response.urljoin(area)
            yield scrapy.Request(url, meta={"city": response.meta['city']}, callback=self.parse_info,dont_filter=True)
        if response.url.find("pg") < 0:
            next = response.xpath("//a[@class='next']/preceding-sibling::a[1]/text()").extract_first()
            if next:
                for i in range(2, int(next) + 1):
                    yield scrapy.Request(response.url+"pg%d" % i, meta={"city":response.meta['city']}, callback=self.parse_middle1)

        # if response.xpath('//span[@id="findCount"]/text()'):
        #     num = response.xpath('//span[@id="findCount"]/text()').extract_first()
        #     pagenum = int(num)/10 + 1
        #     if pagenum > int(metadata['page']):
        #         metadata['page'] = str(int(metadata['page']) + 1)
        #         try:
        #             next = re.findall("(.*)\/pg", response.url)[0] + "/pg" + str(metadata['page']) + "/"
        #             yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle1, dont_filter=True)
        #         except:
        #             next = response.url + "pg" + str(metadata['page']) + "/"
        #             yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle1,dont_filter=True)

    def parse_middle1_type2(self, response):
        lis = response.xpath("//ul[@class='animation city-list']/li")
        for li in lis:
            city = li.xpath("a/text()").extract_first()
            url = response.urljoin(li.xpath("a/@href").extract_first()) + "loupan"
            # print(url)
            yield scrapy.Request(url=url, meta={"city":city}, callback=self.parse_list_type2)
        # metadata = response.meta['metadata']
        # areas = response.xpath('//div[@class="lvjucity_lp"]/div/div[1]/p/a')
        # for href in areas:
        #     area = href.xpath('@href').extract_first()
        #     url = response.urljoin(area)
        #     yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
        # if response.xpath(u'//a[contains(text(),"下一页")]/@href'):
        #     nextbase = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        #     next = response.urljoin(nextbase)
        #     yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle1_type2, dont_filter=True)

    def parse_list_type2(self, response):

        # metadata = response.meta['metadata']
        areas = response.xpath('//ul[@class="project_list_box"]/li/a')
        for href in areas:
            area = href.xpath('@href').extract_first()
            url = response.urljoin(area)
            yield scrapy.Request(url, meta={"city": response.meta['city']}, callback=self.parse_info,dont_filter=True)
        if response.url.find("pg") < 0:
            next = response.xpath("//a[@class='next']/preceding-sibling::a[1]/text()").extract_first()
            if next:
                for i in range(2, int(next) + 1):
                    scrapy.Request(response.url+"pg%d" % i, meta={"city":response.meta["city"]}, callback=self.parse_list_type2)




    def parse_info(self, response):
        # print(response.body)
        print("########################")
        # metadata = response.meta['metadata']
        item = LianjiaFangItem()

            #   http://you.lianjia.com/san/loupan/p_lnsywbaaqe.html
        if response.xpath('//div[@class="lvju_xq_xrmida"]/p/text()'):                       # 楼盘名
            item['building_name'] = response.xpath('//div[@class="lvju_xq_xrmida"]/p/text()').extract_first()
            #   http://hui.fang.lianjia.com/loupan/p_bgylxsaaywi/
        elif response.xpath('//div[@class="name-box"]/a/h1/text()'):
            item['building_name'] = response.xpath('//div[@class="name-box"]/a/h1/text()').extract_first()
            #   http://sh.fang.lianjia.com/detail/zhengrongjingyuan/
        elif response.xpath('//div[@class="info-box"]/div/h1/text()'):
            item['building_name'] = response.xpath('//div[@class="info-box"]/div/h1/text()').extract_first()
        else:
            item['building_name'] = "-"

        if item['building_name'] != "-":
            if response.xpath(u'//span[contains(text(),"别名")]/text()'):                     # 楼盘别名
                building_name2 = response.xpath(u'//span[contains(text(),"别名")]/text()').extract_first().strip()
                try:
                    item['building_name2'] = re.findall(u"别名：(.*)", building_name2)[0]
                except:
                    item['building_name2'] = re.findall(u"别名/(.*)", building_name2)[0]
            else:
                item['building_name2'] = "-"

            if response.xpath('//div[@class="xq_a_price"]/span[2]/text()'):                     # 每平方米价格
                item['price_m2'] = response.xpath('//div[@class="xq_a_price"]/span[2]/text()').extract_first()
            elif response.xpath('//p[@class="jiage"]/span[2]/text()'):
                item['price_m2'] = response.xpath('//p[@class="jiage"]/span[2]/text()').extract_first().strip()
            elif response.xpath('//div[@class="price-row"]/div[1]/span[1]/span[1]/text()'):
                item['price_m2'] = response.xpath('//div[@class="price-row"]/div[1]/span[1]/span[1]/text()').extract_first().strip()
            else:
                item['price_m2'] = "-"

            if response.xpath(u'//div[@class="price-row"]//span[contains(text(),"总价")]/../span[2]/text()'):         # 总价
                item['price'] = response.xpath(u'//div[@class="price-row"]//span[contains(text(),"总价")]/../span[2]/text()').extract_first()
            else:
                item['price'] = "-"

            if response.xpath(u'//div[@class="content"]/ul/li/span[contains(text(),"建筑面积")]/../text()'):            # 建筑面积
                item['sizearea'] = response.xpath(u'//div[@class="content"]/ul/li/span[contains(text(),"建筑面积")]/../text()').extract_first()
            elif response.xpath(u'//span[contains(text(),"建筑面积：")]/../span[2]/text()'):
                item['sizearea'] = response.xpath(u'//span[contains(text(),"建筑面积：")]/../span[2]/text()').extract_first().strip()
            elif response.xpath('//span[@class="row"]/span[@class="num area"]/text()'):
                item['sizearea'] = response.xpath('//span[@class="row"]/span[@class="num area"]/text()').extract_first().strip()
            else:
                item['sizearea'] = "-"

            if response.xpath(u'//span[contains(text(),"物业类型")]/../text()'):                            # 物业类型
                item['house_type'] = response.xpath(u'//span[contains(text(),"物业类型")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业类型：")]/../span[2]/text()'):
                item['house_type'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业类型：")]/../span[2]/text()').extract_first()
            else:
                item['house_type'] = "-"

            if response.xpath(u'//span[contains(text(),"项目地址")]/../span[2]/text()'):                    # 地址
                item['building_address'] = response.xpath(u'//span[contains(text(),"项目地址")]/../span[2]/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"项目地址：")]/../span[2]/text()'):
                item['building_address'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"项目地址：")]/../span[2]/text()').extract_first()
            elif response.xpath(u'//td[contains(text(),"楼盘地址:")]/../td[2]//text()'):
                building_address = ""
                building_address_list = response.xpath(u'//td[contains(text(),"楼盘地址:")]/../td[2]//text()').extract()
                for x in building_address_list:
                    building_address += x.strip()
                item['building_address'] = building_address
            else:
                item['building_address'] = "-"

            if response.xpath('//div[@class="dynamic-row"]/a/text()'):              # 最新动态
                item['news'] = response.xpath('//div[@class="dynamic-row"]/a/text()').extract_first()
            else:
                item['news'] = "-"

            if response.xpath(u'//span[contains(text(),"售楼处地址")]/../div/p/text()'):         # 售楼处地址
                item['sales_offices_address'] = response.xpath(u'//span[contains(text(),"售楼处地址")]/../div/p/text()').extract_first().strip().replace("\n", "")
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"售楼处地址：")]/../span[2]/text()'):
                item['sales_offices_address'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"售楼处地址：")]/../span[2]/text()').extract_first().replace("\n", "")
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"售楼处地址：")]/../span[2]/text()'):
                item['sales_offices_address'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"售楼处地址：")]/../span[2]/text()').extract_first().strip().replace("\n", "")
            else:
                item['sales_offices_address'] = "-"

            if response.xpath(u'//span[contains(text(),"开发商")]/../div/p/text()'):           # 开发商
                item['developers'] = response.xpath(u'//span[contains(text(),"开发商")]/../div/p/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"开发商：")]/../span[2]/text()'):
                item['developers'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"开发商：")]/../span[2]/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"开发商：")]/../span[2]/text()'):
                item['developers'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"开发商：")]/../span[2]/text()').extract_first().strip()
            else:
                item['developers'] = "-"

            if response.xpath(u'//span[contains(text(),"物业公司")]/../div/p/text()'):          # 物业公司
                item['property_company'] = response.xpath(u'//span[contains(text(),"物业公司")]/../div/p/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业公司：")]/../span[2]/text()'):
                item['property_company'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业公司：")]/../span[2]/text()').extract_first()
            else:
                item['property_company'] = "-"

            if response.xpath('//div[@class="showteltxt"]/text()'):             # 电话
                item['phone'] = response.xpath('//div[@class="showteltxt"]/text()').extract_first().strip()
            elif response.xpath('//div[@class="btn_phone_ll LOGCLICK"]/span/text()'):
                item['phone'] = response.xpath('//div[@class="btn_phone_ll LOGCLICK"]/span/text()').extract_first().strip()
            elif response.xpath('//div[@class="phone-row"]/span[2]//text()'):
                phone = ""
                phone_list = response.xpath('//div[@class="phone-row"]/span[2]//text()').extract()
                for x in phone_list:
                    phone += x.strip()
                item['phone'] = phone
            else:
                item['phone'] = "-"

            if response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"装修状况：")]/../span[2]/text()'):     # 装修状况
                item['decoration_situation'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"装修状况：")]/../span[2]/text()').extract_first().strip()
            else:
                item['decoration_situation'] = "-"

            if response.xpath(u'//span[contains(text(),"最新开盘")]/../div/p/text()'):              # 最新开盘时间
                item['opening_quotation'] = response.xpath(u'//span[contains(text(),"最新开盘")]/../div/p/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"最新开盘：")]/../span[2]/text()'):
                item['opening_quotation'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"最新开盘：")]/../span[2]/text()').extract_first().strip()
            else:
                item['opening_quotation'] = "-"

            if response.xpath(u'//span[contains(text(),"最早交房")]/../div/p/text()'):          # 最早交房时间
                item['deliver_time'] = response.xpath(u'//span[contains(text(),"最早交房")]/../div/p/text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"交房时间：")]/../span[2]/text()'):
                item['deliver_time'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"交房时间：")]/../span[2]/text()').extract_first().strip()
            else:
                item['deliver_time'] = "-"

            if response.xpath(u'//div[@class="content"]//li//span[contains(text(),"物业费用：")]/../text()'):        # 物业费用
                item['property_fee'] = response.xpath(u'//div[@class="content"]//li//span[contains(text(),"物业费用：")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业费")]/../span[2]/text()'):
                item['property_fee'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"物业费")]/../span[2]/text()').extract_first().strip()
            else:
                item['property_fee'] = "-"

            if response.xpath(u'//div[@class="content"]//li//span[contains(text(),"水电燃气：")]/../text()'):            # 水电燃气
                item['water_and_electric'] = response.xpath(u'//div[@class="content"]//li//span[contains(text(),"水电燃气：")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"供水方式：")]/../span[2]/text()'):
                water = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"供水方式：")]/../span[2]/text()').extract_first()
                electric = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"供电方式：")]/../span[2]/text()').extract_first()
                item['water_and_electric'] = water + " " + electric
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"用水用电：")]/../span[2]/text()'):
                item['water_and_electric'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"用水用电：")]/../span[2]/text()').extract_first().strip()
            else:
                item['water_and_electric'] = "-"

            if response.xpath(u'//div[@class="content"]//li//span[contains(text(),"计划户数：")]/../text()'):            # 计划户数
                item['house_num'] = response.xpath(u'//div[@class="content"]//li//span[contains(text(),"计划户数：")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"规划户数：")]/../span[2]/text()'):
                item['house_num'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"规划户数：")]/../span[2]/text()').extract_first().strip()
            else:
                item['house_num'] = "-"

            if response.xpath(u'//div[@class="content"]//li//span[contains(text(),"产权年限：")]/../text()'):        # 产权年限
                item['pry'] = response.xpath(u'//div[@class="content"]//li//span[contains(text(),"产权年限：")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"产权年限：")]/../span[2]/text()'):
                item['pry'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"产权年限：")]/../span[2]/text()').extract_first().strip()
            else:
                item['pry'] = "-"

            if response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"容积率：")]/../span[2]/text()'):      # 容积率
                item['volume_ratio'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"容积率：")]/../span[2]/text()').extract_first().strip()
            else:
                item['volume_ratio'] = "-"

            if response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"绿化率：")]/../span[2]/text()'):          # 绿化率
                item['greening_rate'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"绿化率：")]/../span[2]/text()').extract_first().strip()
            else:
                item['greening_rate'] = "-"

            if response.xpath(u'//div[@class="content"]//li//span[contains(text(),"车位情况：")]/../text()'):            # 车位情况
                item['parking_condition'] = response.xpath(u'//div[@class="content"]//li//span[contains(text(),"车位情况：")]/../text()').extract_first()
            elif response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"车位")]/../span[2]/text()'):
                item['parking_condition'] = response.xpath(u'//div[@class="box-loupan"]//span[contains(text(),"车位")]/../span[2]/text()').extract_first().strip()
            else:
                item['parking_condition'] = "-"

            item['url'] = response.url
            item['website'] = website
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['status'] = item['building_name'] + response.url
            item['city'] = response.meta['city']

            yield item