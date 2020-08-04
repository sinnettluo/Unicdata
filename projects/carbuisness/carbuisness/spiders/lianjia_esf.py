# -*- coding: utf-8 -*-
"""

C2017-41-1
二手房和新房分成两个程序，这是二手房

"""
import scrapy
from carbuisness.items import LianjiaEsfItem
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

website='lianjia_esf_2018'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://bj.lianjia.com/']

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000
        self.city_list = ["hk","you","ls","qh","sjz","san","ty","wx","wc","wn","xa"]

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # k = 600
        # for i in range(0,5400):
        #     time.sleep(1)
        #     if i%k==0:
        #         t = (9 - (i/k)) * 10
        #         print u"距离程序运行还有 " + str(t) + u" 分钟"

    def parse(self, response):
        citylist = response.xpath('//div[@class="fc-main clear"]//ul/li/div/a')
        for href in citylist:
            city = href.xpath('text()').extract_first()
            # proxy = getProxy()
            metadata = {"city" : city}#, "proxy":proxy}
            urlbase = href.xpath('@href').extract_first()
            cityfront = re.findall("(.*?)\.lianjia", urlbase)[0]
            citypinyin = re.findall("://(.*?)\.", urlbase)[0]
            if citypinyin not in self.city_list:
                url = cityfront + ".lianjia.com/ershoufang"
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle1, dont_filter=True)

    # def parse_middle0(self, response):
    #     url = response.xpath(u'//ul/li/a[contains(text(),"二手房")]/@href').extract_first()
    #     yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle1, dont_filter=True)

    #上海和其他城市页面不一样，需要分开解析
    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        if response.xpath('//h2[@class="total fl"]/span/text()'):
            num = response.xpath('//h2[@class="total fl"]/span/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@data-role="ershoufang"]/div/a')
                for area in areas:
                    urlbase = area.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle2,dont_filter=True)
            else:
                yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_finaly, dont_filter=True)

        elif response.xpath('//div[@class="search-result"]/span/text()'):   #类似于上海的页面
            num = response.xpath('//div[@class="search-result"]/span/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@class="level1"]/a[@class="level1-item "]')
                for area in areas:
                    urlbase = area.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle_sh_2,dont_filter=True)
            else:
                yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_sh_finaly,dont_filter=True)
        # else:
            # print response.url

    def parse_middle2(self, response):
        metadata = response.meta['metadata']
        if response.xpath('//h2[@class="total fl"]/span/text()'):
            num = response.xpath('//h2[@class="total fl"]/span/text()').extract_first().strip()
            #num = response.xpath('//span[@class="result-count strong-num"]/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')
                for area in areas:
                    urlbase = area.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    addmeta = {"page":"1"}
                    metadata = dict(metadata, **addmeta)
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle_finaly,dont_filter=True)
            else:
                addmeta = {"page": "1"}
                metadata = dict(metadata, **addmeta)
                yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_finaly, dont_filter=True)
        else:
            print "don't get num ... " + response.url

    def parse_middle_sh_2(self, response):
        metadata = response.meta['metadata']
        if response.xpath('//div[@class="search-result"]/span/text()'):
            num = response.xpath('//div[@class="search-result"]/span/text()').extract_first().strip()
            #num = response.xpath('//span[@class="result-count strong-num"]/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@class="level2-item"]/a[@class=""]')
                for area in areas:
                    urlbase = area.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    addmeta = {"page": "1"}
                    metadata = dict(metadata, **addmeta)
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle_sh_finaly,dont_filter=True)
            else:
                addmeta = {"page": "1"}
                metadata = dict(metadata, **addmeta)
                yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_sh_finaly, dont_filter=True)
        else:
            print response.url

    def parse_middle_finaly(self, response):
        metadata = response.meta['metadata']
        for href in response.xpath('//ul[@class="sellListContent"]/li/a'):
            url = href.xpath('@href').extract_first()
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
        if response.xpath(u'//a[contains(text(),"下一页")]/@href'):
            nextbase = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
            next = response.urljoin(nextbase)
            yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly, dont_filter=True)
        elif response.xpath('//h2[@class="total fl"]/span/text()'):
            num = response.xpath('//h2[@class="total fl"]/span/text()').extract_first().strip()
            pagenum = int(num) / 30 + 1
            if pagenum > int(metadata['page']):
                metadata['page'] = str(int(metadata['page']) + 1)
                try:
                    next = re.findall("(.*)\/pg", response.url)[0] + "/pg" + str(metadata['page']) + "/"
                    yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly,dont_filter=True)
                except:
                    next = response.url + "pg" + str(metadata['page']) + "/"
                    yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly,dont_filter=True)

    def parse_middle_sh_finaly(self, response):
        metadata = response.meta['metadata']
        for href in response.xpath('//div[@class="info"]/div[1]/a'):
            urlbase = href.xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)


    def parse_info(self, response):
        # https://hui.lianjia.com/ershoufang/105100900489.html
        metadata = response.meta['metadata']
        item = LianjiaEsfItem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        if response.xpath('//div[@class="price"]/span/text()'):
            item['price'] = response.xpath('//div[@class="price"]/span/text()').extract_first()
        elif response.xpath('//div[@class="price "]/span/text()'):
            item['price'] = response.xpath('//div[@class="price "]/span/text()').extract_first()        # 价格
        elif response.xpath(u'//span[@class="price-num"]/text()'):
            item['price'] = response.xpath(u'//span[@class="price-num"]/text()').extract_first()
        else:
            item['price'] = "-"

        if response.xpath('//div[@class="unitPrice"]/span/text()'):
            item['price_m2'] = response.xpath('//div[@class="unitPrice"]/span/text()').extract_first()  # 每平米价格
        elif response.xpath(u'//span[@class="u-bold"]/text()'):
            item['price_m2'] = response.xpath(u'//span[@class="u-bold"]/text()').extract_first()
        else:
            item['price_m2'] = "-"

        item['loop_information'] = response.xpath(u'//span[contains(text(),"环线信息")]/../span[2]/text()').extract_first() \
            if response.xpath(u'//span[contains(text(),"环线信息")]/../span[2]/text()').extract_first() else "-"                # 环线信息

        build_name = "-"
        if response.xpath(u'//span[contains(text(),"小区名称")]/../a[1]/text()'):                               # 小区名称
            build_names = response.xpath(u'//span[contains(text(),"小区名称")]/../a[1]/text()').extract()
            flag = 1
            for x in build_names:
                if flag:
                    build_name = x.strip()
                    flag = 0
                else:
                    build_name += x.strip()
        elif response.xpath(u'//span[contains(text(),"小区名称")]/../span[2]/span//text()'):
            build_names = response.xpath(u'//span[contains(text(),"小区名称")]/../span[2]/span//text()').extract()
            flag = 1
            for x in build_names:
                if flag:
                    build_name = x.strip()
                    flag = 0
                else:
                    build_name += x.strip()
        item['build_name'] = build_name

        address = "-"
        if response.xpath(u'//span[contains(text(),"所在区域")]/../span[2]//a/text()'):                                 # 地址
            address_list = response.xpath(u'//span[contains(text(),"所在区域")]/../span[2]//a/text()').extract()
            flag = 1
            for x in address_list:
                if flag:
                    address = x
                    flag = 0
                else:
                    address += x
        elif response.xpath(u'//span[contains(text(),"所在地址")]/../span[2]/text()'):
            address_list = response.xpath(u'//span[contains(text(),"所在地址")]/../span[2]/text()').extract()
            flag = 1
            for x in address_list:
                if flag:
                    address = x
                    flag = 0
                else:
                    address += x
        item['address'] = address

        if response.xpath(u'//span[contains(text(),"链家编号")]/../span[2]/text()'):                                                # 链家编号
            item['house_id'] = response.xpath(u'//span[contains(text(),"链家编号")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"房源编号")]/../span[2]/text()'):
            item['house_id'] = response.xpath(u'//span[contains(text(),"房源编号")]/../span[2]/text()').extract_first().strip()
        else:
            item['house_id'] = "-"

        property_phone = "-"
        if response.xpath('//div[@class="brokerInfoText fr"]/div[@class="phone"]//text()'):                                 # 物业电话
            property_phones = response.xpath('//div[@class="brokerInfoText fr"]/div[@class="phone"]//text()').extract()
            flag = 1
            for x in property_phones:
                if flag:
                    property_phone = x
                    flag = 0
                else:
                    property_phone += x.strip()
        elif response.xpath(u'//div[@class="agent-info"]/p[@class="agent-row3"]//text()'):
            property_phones = response.xpath(u'//div[@class="agent-info"]/p[@class="agent-row3"]//text()').extract()
            flag = 1
            for x in property_phones:
                if flag:
                    property_phone = x.strip()
                    flag = 0
                else:
                    property_phone += x.strip()
        item['property_phone'] = property_phone

        if response.xpath(u'//span[contains(text(),"房屋户型")]/../text()'):                                                # 房屋户型
            item['house_type'] = response.xpath(u'//span[contains(text(),"房屋户型")]/../text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"房屋户型")]/../span[2]/text()'):
            item['house_type'] = response.xpath(u'//span[contains(text(),"房屋户型")]/../span[2]/text()').extract_first()
        else:
            item['house_type'] = "-"

        if response.xpath(u'//span[contains(text(),"配备电梯")]/../span[2]/text()'):                                        # 配备电梯
            item['elevator'] = response.xpath(u'//span[contains(text(),"配备电梯")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"配备电梯")]/../text()'):
            item['elevator'] = response.xpath(u'//span[contains(text(),"配备电梯")]/../text()').extract_first()
        else:
            item['elevator'] = "-"

        if response.xpath(u'//span[contains(text(),"建筑面积")]/../span[2]/text()'):                                        # 建筑面积
            item['sizearea'] = response.xpath(u'//span[contains(text(),"建筑面积")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"建筑面积")]/../text()'):
            item['sizearea'] = response.xpath(u'//span[contains(text(),"建筑面积")]/../text()').extract_first()
        else:
            item['sizearea'] = "-"

        if response.xpath(u'//span[contains(text(),"供暖方式")]/../span[2]/text()'):                                            # 供暖方式
            item['heating_type'] = response.xpath(u'//span[contains(text(),"供暖方式")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"供暖方式")]/../text()'):
            item['heating_type'] = response.xpath(u'//span[contains(text(),"供暖方式")]/../text()').extract_first()
        else:
            item['heating_type'] = "-"

        if response.xpath(u'//span[contains(text(),"所在楼层")]/../span[2]/text()'):                                               # 所在楼层
            item['floor_NO'] = response.xpath(u'//span[contains(text(),"所在楼层")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"所在楼层")]/../text()'):
            item['floor_NO'] = response.xpath(u'//span[contains(text(),"所在楼层")]/../text()').extract_first()
        else:
            item['floor_NO'] = "-"

        if response.xpath(u'//span[contains(text(),"装修情况")]/../span[2]/text()'):                                                    # 装修情况
            item['decoration_situation'] = response.xpath(u'//span[contains(text(),"装修情况")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"装修情况")]/../text()'):
            item['decoration_situation'] = response.xpath(u'//span[contains(text(),"装修情况")]/../text()').extract_first()
        else:
            item['decoration_situation'] = "-"

        if response.xpath(u'//span[contains(text(),"房屋朝向")]/../span[2]/text()'):                                                       # 房屋朝向
            item['orientations'] = response.xpath(u'//span[contains(text(),"房屋朝向")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"房屋朝向")]/../text()'):
            item['orientations'] = response.xpath(u'//span[contains(text(),"房屋朝向")]/../text()').extract_first().strip()
        else:
            item['orientations'] = "-"

        if response.xpath(u'//span[contains(text(),"车位情况")]/../span[2]/text()'):                                                        # 车位情况
            item['parking_condition'] = response.xpath(u'//span[contains(text(),"车位情况")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"车位情况")]/../text()').extract_first():
            item['parking_condition'] = response.xpath(u'//span[contains(text(),"车位情况")]/../text()').extract_first().strip()
        else:
            item['parking_condition'] = "-"

        if response.xpath(u'//span[contains(text(),"上次交易")]/../span[2]/text()'):                                                        # 上次交易
            item['transaction_last'] = response.xpath(u'//span[contains(text(),"上次交易")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"上次交易")]/../text()'):
            item['transaction_last'] = response.xpath(u'//span[contains(text(),"上次交易")]/../text()').extract_first().strip()
        else:
            item['transaction_last'] = "-"

        if response.xpath(u'//span[contains(text(),"房本年限")]/../span[2]/text()'):                                                        # 房本年限
            item['age_limit'] = response.xpath(u'//span[contains(text(),"房本年限")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"产权年限")]/../text()'):
            item['age_limit'] = response.xpath(u'//span[contains(text(),"产权年限")]/../text()').extract_first()
        else:
            item['age_limit'] = "-"

        if response.xpath(u'//span[contains(text(),"售房原因")]/../span[2]/text()'):                                                        # 售房原因
            item['sale_reason'] = response.xpath(u'//span[contains(text(),"售房原因")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"售房原因")]/../text()'):
            item['sale_reason'] = response.xpath(u'//span[contains(text(),"售房原因")]/../text()').extract_first()
        else:
            item['sale_reason'] = "-"

        if response.xpath(u'//span[contains(text(),"房屋类型")]/../span[2]/text()'):                                                        # 房屋类型
            item['building_type'] = response.xpath(u'//span[contains(text(),"房屋类型")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"房屋用途")]/../text()'):
            item['building_type'] = response.xpath(u'//span[contains(text(),"房屋用途")]/../text()').extract_first().strip()
        else:
            item['building_type'] = "-"

        if response.xpath(u'//span[contains(text(),"挂牌均价")]/../span[2]/text()'):                                                        # 挂牌均价
            item['average_price'] = response.xpath(u'//span[contains(text(),"挂牌均价")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"挂牌均价")]/../text()'):
            item['average_price'] = response.xpath(u'//span[contains(text(),"挂牌均价")]/../text()').extract_first().strip()
        else:
            item['average_price'] = "-"

        if response.xpath(u'//span[contains(text(),"建筑年代")]/../span[2]/text()'):                                                            # 建筑年代
            item['build_age'] = response.xpath(u'//span[contains(text(),"建筑年代")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"建筑年代")]/../text()'):
            item['build_age'] = response.xpath(u'//span[contains(text(),"建筑年代")]/../text()').extract_first().strip()
        else:
            item['build_age'] = "-"

        if response.xpath(u'//span[contains(text(),"物业类型")]/../span[2]/text()'):                                                            # 物业类型
            item['property_type'] = response.xpath(u'//span[contains(text(),"物业类型")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"物业类型")]/../text()'):
            item['property_type'] = response.xpath(u'//span[contains(text(),"物业类型")]/../text()').extract_first().strip()
        else:
            item['property_type'] = "-"

        if response.xpath(u'//span[contains(text(),"楼栋总数")]/../span[2]/text()'):                                                            # 楼栋总数
            item['building_num'] = response.xpath(u'//span[contains(text(),"楼栋总数")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"楼栋总数")]/../text()'):
            item['building_num'] = response.xpath(u'//span[contains(text(),"楼栋总数")]/../text()').extract_first()
        else:
            item['building_num'] = "-"

        if response.xpath(u'//span[contains(text(),"房屋总数")]/../span[2]/text()'):                                                            # 房屋总数
            item['house_num'] = response.xpath(u'//span[contains(text(),"房屋总数")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"房屋总数")]/../text()'):
            item['house_num'] = response.xpath(u'//span[contains(text(),"房屋总数")]/../text()').extract_first()
        else:
            item['house_num'] = "-"

        if response.xpath(u'//span[contains(text(),"物业公司")]/../span[2]/text()'):                                                            # 物业公司
            item['property_company'] = response.xpath(u'//span[contains(text(),"物业公司")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//span[contains(text(),"物业公司")]/../text()'):
            item['property_company'] = response.xpath(u'//span[contains(text(),"物业公司")]/../text()').extract_first().strip()
        else:
            item['property_company'] = "-"

        if response.xpath(u'//span[contains(text(),"开发商")]/../span[2]/text()'):                                                         # 开发商
            item['developers'] = response.xpath(u'//span[contains(text(),"开发商")]/../span[2]/text()').extract_first()
        elif response.xpath(u'//span[contains(text(),"开发商")]/../text()'):
            item['developers'] = response.xpath(u'//span[contains(text(),"开发商")]/../text()').extract_first()
        else:
            item['developers'] = "-"

        listing_houses = "-"
        if response.xpath(u'//span[contains(text(),"挂牌房源")]/../text()'):                                                            # 挂牌房源
            listing_housess = response.xpath(u'//span[contains(text(),"挂牌房源")]/../text()').extract()
            flag = 1
            for x in listing_housess:
                if flag:
                    listing_houses = x.strip()
                    flag = 0
                else:
                    listing_houses += "," + x.strip()
        elif response.xpath(u'//span[contains(text(),"挂牌房源")]/../span[2]//text()'):
            listing_housess = response.xpath(u'//span[contains(text(),"挂牌房源")]/../span[2]//text()').extract()
            flag = 1
            for x in listing_housess:
                if flag:
                    listing_houses = x.strip()
                    flag = 0
                else:
                    listing_houses += "," + x.strip()
        item['listing_houses'] = listing_houses

        item['shortdesc'] = response.xpath(u'//h1/text()').extract_first() \
            if response.xpath(u'//h1/text()').extract_first() else "-"          # 标题描述

        item['city'] = metadata['city']                                             # 城市

        label = "-"
        if response.xpath(u'//div[contains(text(),"房源标签")]/../div[2]/a/text()'):                                                    # 房源标签
            flag = 1
            label_list = response.xpath(u'//div[contains(text(),"房源标签")]/../div[2]/a/text()').extract()
            for x in label_list:
                if flag:
                    label = x
                    flag = 0
                else:
                    label += "," + x
        item['label'] = label

        if response.xpath(u'//div[contains(text(),"核心卖点")]/../div[2]/text()'):                                                                  # 核心卖点
            item['core_selling_point'] = response.xpath(u'//div[contains(text(),"核心卖点")]/../div[2]/text()').extract_first().strip()

        if response.xpath(u'//div[contains(text(),"交通出行")]/../div[2]/text()'):                                                                  # 交通出行
            item['traffic_trip'] = response.xpath(u'//div[contains(text(),"交通出行")]/../div[2]/text()').extract_first().strip()

        if response.xpath(u'//div[contains(text(),"小区介绍")]/../div[2]/text()'):                                                                  # 小区介绍
            item['community_introduction'] = response.xpath(u'//div[contains(text(),"小区介绍")]/../div[2]/text()').extract_first().strip()

        if response.xpath(u'//div[contains(text(),"户型介绍")]/../div[2]/text()'):                                                                  # 户型介绍
            item['apartment_description'] = response.xpath(u'//div[contains(text(),"户型介绍")]/../div[2]/text()').extract_first().strip()

        if response.xpath(u'//div[contains(text(),"周边配套")]/../div[2]/text()'):                                                                  # 周边配套
            item['periphery'] = response.xpath(u'//div[contains(text(),"周边配套")]/../div[2]/text()').extract_first().strip()

        if response.xpath(u'//div[contains(text(),"装修描述")]/../div[2]/text()'):                                                                  # 装修描述
            item['decoration_describe'] = response.xpath(u'//div[contains(text(),"装修描述")]/../div[2]/text()').extract_first().strip()

        yield item