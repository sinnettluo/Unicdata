# -*- coding: utf-8 -*-
"""

C2017-43-1
汽车之家 综合店

"""
import scrapy
from carbuisness.items import AutohomeGeneralStore
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings

website ='autohome_general_store'

class CarSpider(scrapy.Spider):
    name = website
    # allowed_domains = ["autohome.com.cn"]
    #选择城市，从这个入口获得城市信息
    start_urls = [
        'http://dealer.autohome.com.cn/Ajax?actionName=GetAreasAjax&ajaxProvinceId=0&ajaxCityId=310100&ajaxBrandid=0&ajaxManufactoryid=0&ajaxSeriesid=0',
    ]

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 80000

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    def parse(self, response):

        print(response.body)

        citylist = []
        citylist_base = json.loads(re.findall("<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">(.*?)</pre>", response.body)[0])
        # city_unit = []
        # HotCites = citylist_base['HotCites'] #这个列表在下面是重复出现的
        AreaInfoGroups = citylist_base['AreaInfoGroups']
        for i in AreaInfoGroups:
            j = i['Values']
            for k in j:
                citylist.append(k)
        for city in citylist:
            city_pinyin = city['Pinyin']
            url = "http://dealer.autohome.com.cn/" \
                  + city_pinyin \
                  + "?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=1&kindId=1&orderType=0&isSales=0"
            # print url
            yield scrapy.Request(url, callback=self.parse_middle1, dont_filter=True)

    def parse_middle1(self, response):


        next_page = response.xpath("//*[@id='pagination']/a")
        print(next_page)
        for item in next_page:
            if item.xpath("text()").extract_first() == u"下一页":
                yield scrapy.Request(response.urljoin(item.xpath("@href").extract_first()),
                                     callback=self.parse_middle1, dont_filter=True)

        # if response.xpath(u'//div[@class="tab"]/a[contains(text(),"综合经销商")]'):
            # print response.url
        urllist = response.xpath('//ul[@class="list-box"]/li/a')
        for href in urllist:
            urlbase = href.xpath('@href').extract_first()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        item = AutohomeGeneralStore()

        if response.xpath('//div[@id="breadnav"]/a[2]/text()'):
            item['city'] = response.xpath('//div[@id="breadnav"]/a[2]/text()').extract_first()
        else:
            item['city'] = "-"

        if response.xpath(u'//div[@class="allagency-cont"]/p[contains(text(),"所属级别")]/text()'):
            starLevel = response.xpath(u'//div[@class="allagency-cont"]/p[contains(text(),"所属级别")]/text()').extract_first()#所属级别
            item['star_level'] = re.findall(u"：(.*)", starLevel)[0]
        else:
            item['star_level'] = "-"

        if  response.xpath(u'//div[@class="cont-text"]/div[@class="text-main"]/text()'):
            item['name'] = response.xpath(u'//div[@class="cont-text"]/div[@class="text-main"]/text()').extract_first()  #
        else:
            item['name'] = "-"

        if  response.xpath('//div[@class="allagency-cont"]//span[@class="dealer-api-phone"]/text()'):
            item['phone'] = response.xpath('//div[@class="allagency-cont"]//span[@class="dealer-api-phone"]/text()').extract_first()  #
        else:
            item['phone'] = "-"

        if  response.xpath('//div[@class="allagency-cont"]//p[@class="address"]/a/text()'):
            item['address'] = response.xpath('//div[@class="allagency-cont"]//p[@class="address"]/a/text()').extract_first()  #
        else:
            item['address'] = "-"

        mainBrand = []
        for unit in response.xpath('//div[@class="brandtree-cont"]/dl'):
            brand_first = unit.xpath('dt/a/text()').extract_first()
            brand_second_base = unit.xpath('dd/a/text()').extract()
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
        item['status'] = item['name'] + response.url  # url

        yield item
