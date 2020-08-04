# -*- coding: utf-8 -*-
"""

C2017-41-3
链家的小区

"""

import scrapy
from carbuisness.items import LianjiaVillageItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import carbuisness.mydial


website='lianjia_village'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://bj.lianjia.com/']
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,
        }
    }

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000
        self.city_list = ["hk","you","ls","qh","sjz","san","ty","wx","wc","wn","xa"]

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        citylist = response.xpath('//div[@class="fc-main clear"]//ul/li/div/a')
        for href in citylist:
            city = href.xpath('text()').extract_first()
            metadata = {"city" : city}
            urlbase = href.xpath('@href').extract_first()
            cityfront = re.findall("(.*?)\.lianjia", urlbase)[0]
            citypinyin = re.findall("://(.*?)\.", urlbase)[0]
            if citypinyin not in self.city_list:
                url = cityfront + ".lianjia.com/xiaoqu/"
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle1, dont_filter=True)

    #上海和其他城市页面不一样，需要分开解析
    def parse_middle1(self, response):
        metadata = response.meta['metadata']
        if response.xpath('//h2[@class="total fl"]/span/text()'):   #正常页面
            # num = response.xpath('//h2[@class="total fl"]/span/text()').extract_first().strip()
            areas = response.xpath('//div[@data-role="ershoufang"]/div/a')
            for area in areas:
                urlbase = area.xpath('@href').extract_first()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle2,dont_filter=True)
            # else:
            #     yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_finaly, dont_filter=True)

        elif response.xpath('//div[@class="con-box"]//h2/span/text()'):   #类似于上海的页面
            num = response.xpath('//div[@class="con-box"]//h2/span/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@id="filter-options"]/dl[@class="dl-lst clear"]//a')
                flag = 0
                for area in areas:
                    if flag:
                        urlbase = area.xpath('@href').extract_first()
                        url = response.urljoin(urlbase)
                        yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle_sh_2,dont_filter=True)
                    else:
                        flag = 1
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
        if response.xpath('//div[@class="con-box"]//h2/span/text()'):
            num = response.xpath('//div[@class="con-box"]//h2/span/text()').extract_first().strip()
            #num = response.xpath('//span[@class="result-count strong-num"]/text()').extract_first().strip()
            if num>3000:
                areas = response.xpath('//div[@class="option-list sub-option-list gio_plate"]/a')
                flag = 0
                for area in areas:
                    if flag:
                        urlbase = area.xpath('@href').extract_first()
                        url = response.urljoin(urlbase)
                        addmeta = {"page": "1"}
                        metadata = dict(metadata, **addmeta)
                        yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle_sh_finaly,dont_filter=True)
                    else:
                        flag = 1
            else:
                addmeta = {"page": "1"}
                metadata = dict(metadata, **addmeta)
                yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle_sh_finaly, dont_filter=True)
        else:
            print response.url

    def parse_middle_finaly(self, response):
        metadata = response.meta['metadata']
        for href in response.xpath('//ul[@class="listContent"]/li/a'):
            url = href.xpath('@href').extract_first()
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
        if response.xpath(u'//a[contains(text(),"下一页")]/@href'):
            nextbase = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
            next = response.urljoin(nextbase)
            yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly, dont_filter=True)
        elif response.xpath('//div[@class="con-box"]//h2/span/text()'):
            num = response.xpath('//div[@class="con-box"]//h2/span/text()').extract_first().strip()
            pagenum = int(num) / 30 + 1
            if pagenum > int(metadata['page']):
                metadata['page'] = str(int(metadata['page']) + 1)
                try:
                    next = re.findall("(.*)\/d", response.url)[0] + "/d" + str(metadata['page']) + "/"
                    yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly,dont_filter=True)
                except:
                    next = response.url + "d" + str(metadata['page']) + "/"
                    yield scrapy.Request(next, meta={"metadata": metadata}, callback=self.parse_middle_finaly,dont_filter=True)

    def parse_middle_sh_finaly(self, response):
        metadata = response.meta['metadata']
        for href in response.xpath('//ul[@id="house-lst"]//div[@class="info-panel"]/h2/a'):
            urlbase = href.xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)


    def parse_info(self, response):
        metadata = response.meta['metadata']
        item = LianjiaVillageItem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['city'] = metadata['city']     # 城市

        # https://bj.lianjia.com/xiaoqu/1111027375142/
        # http://sh.lianjia.com/xiaoqu/5011000014388.html

        if response.xpath('//div[@class="detailHeader fl"]/h1/text()'):
            item['name'] = response.xpath('//div[@class="detailHeader fl"]/h1/text()').extract_first().strip()      # 小区名
        elif response.xpath('//div[@class="title fl"]/span[@class="t"]/h1/text()'):
            item['name'] = response.xpath('//div[@class="title fl"]/span[@class="t"]/h1/text()').extract_first().strip()
        else:
            item['name'] = "-"

        if response.xpath('//div[@class="detailHeader fl"]/div[@class="detailDesc"]/text()'):
            item['address'] = response.xpath('//div[@class="detailHeader fl"]/div[@class="detailDesc"]/text()').extract_first().strip()   # 小区地址
        elif response.xpath('//div[@class="title fl"]/span[@class="t"]/span[@class="adr"]/text()'):
            item['address'] = response.xpath('//div[@class="title fl"]/span[@class="t"]/span[@class="adr"]/text()').extract_first().strip()
        else:
            item['address'] = "-"

        if response.xpath('//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]//span[@class="xiaoquUnitPrice"]/text()'):  # 挂牌均价
            item['price'] = response.xpath('//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]//span[@class="xiaoquUnitPrice"]/text()').extract_first().strip()
        elif response.xpath('//div[@class="res-info fr"]/div[@class="priceInfo"]//span[@class="p"]/text()'):
            item['price'] = response.xpath('//div[@class="res-info fr"]/div[@class="priceInfo"]//span[@class="p"]/text()').extract_first().strip()
        else:
            item['price'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"建筑年代")]/../span[2]/text()'):   # 建筑年代
            item['build_year'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"建筑年代")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"建成年代")]/../span/text()'):
            item['build_year'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"建成年代")]/../span/text()').extract_first().strip()
        else:
            item['build_year'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"建筑类型")]/../span[2]/text()'):   # 建筑类型
            item['build_type'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"建筑类型")]/../span[2]/text()').extract_first()
        # elif response.xpath(''):
        #     item['build_type'] = response.xpath('').extract_first()
        else:
            item['build_type'] = "-"

        if response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业类型")]/../span/text()'):  # 物业类型
            item['property_type'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业类型")]/../span/text()').extract_first().strip()
        # elif response.xpath(''):
        #     item['property_type'] = response.xpath('').extract_first()
        else:
            item['property_type'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"物业费用")]/../span[2]/text()'):   # 物业费用
            item['property_fee'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"物业费用")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业费用")]/../span/text()'):
            item['property_fee'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业费用")]/../span/text()').extract_first().strip()
        else:
            item['property_fee'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"物业公司")]/../span[2]/text()'):   # 物业公司
            item['property_company'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"物业公司")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业公司")]/../span/text()'):
            item['property_company'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"物业公司")]/../span/text()').extract_first().strip()
        else:
            item['property_company'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"开发商")]/../span[2]/text()'):    # 开发商
            item['developers'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"开发商")]/../span[2]/text()').extract_first().strip()
        elif response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"开发商")]/../span/text()'):
            item['developers'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"开发商")]/../span/text()').extract_first().strip()
        else:
            item['developers'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"楼栋总数")]/../span[2]/text()'):   # 楼栋总数
            item['floor_num'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"楼栋总数")]/../span[2]/text()').extract_first()
        # elif response.xpath(''):
        #     item['floor_num'] = response.xpath('').extract_first()
        else:
            item['floor_num'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"房屋总数")]/../span[2]/text()'):   # 房屋总数
            item['house_num'] = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"房屋总数")]/../span[2]/text()').extract_first()
        # elif response.xpath(''):
        #     item['house_num'] = response.xpath('').extract_first()
        else:
            item['house_num'] = "-"

        if response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"附近门店")]/../span[2]//text()'):  # 附近门店
            nearby_stores = ""
            nearby_stores_list = response.xpath(u'//div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]//span[contains(text(),"附近门店")]/../span[2]//text()').extract()
            for i in nearby_stores_list:
                nearby_stores += i
            item['nearby_stores'] = nearby_stores
        elif response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"附近门店")]/../span/text()'):
            item['nearby_stores'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"附近门店")]/../span/text()').extract_first()
        else:
            item['nearby_stores'] = "-"

        if response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"区域")]/../span/a/text()'):   # 区域
            item['region'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"区域")]/../span/a/text()').extract_first().strip()
        # elif response.xpath(''):
        #     item[''] = response.xpath('').extract_first()
        else:
            item['region'] = "-"

        if response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"环线")]/../span/text()'):     # 环线
            item['loop_line'] = response.xpath(u'//div[@class="res-info fr"]/div[@class="col-2 clearfix"]//li//label[contains(text(),"环线")]/../span/text()').extract_first()
        # elif response.xpath(''):
        #     item['loop_line'] = response.xpath('').extract_first()
        else:
            item['loop_line'] = "-"

        if response.xpath('//div[@class="agentTitle clear"]/div[@class="fr"]//text()'):     # 评分
            score = ""
            score_list = response.xpath('//div[@class="agentTitle clear"]/div[@class="fr"]//text()').extract()
            for i in score_list:
                score += i
            item['score'] = score
        # elif response.xpath(''):
        #     item['score'] = response.xpath('').extract_first()
        else:
            item['score'] = "-"


        ####################################  小区顾问  #####################################
        item['adviser'] = {}    # 小区顾问

        if response.xpath('//div[@class="agentInfo fr"]//div[@class="fl"]/a/text()'):
            item['adviser']['name'] = response.xpath('//div[@class="agentInfo fr"]//div[@class="fl"]/a/text()').extract_first()    # 顾问姓名
        else:
            item['adviser']['name'] = "-"

        if response.xpath('//div[@class="agentInfo fr"]//div[@class="agentDesc"]/text()'):  # 顾问描述
            item['adviser']['desc'] = response.xpath('//div[@class="agentInfo fr"]//div[@class="agentDesc"]/text()').extract_first()
        else:
            item['adviser']['desc'] = "-"

        if response.xpath('//div[@class="agentInfo fr"]//div[@class="phone"]/text()'):     # 顾问电话
            item['adviser']['phone'] = response.xpath('//div[@class="agentInfo fr"]//div[@class="phone"]/text()').extract_first()
        else:
            item['adviser']['phone'] = "-"


    ####################################  小区顾问  #####################################

        yield item