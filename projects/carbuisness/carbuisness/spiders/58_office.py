# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import w58officeitem
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

website='58_office'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.58.com/ershouche/changecity/"
    ]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # options = webdriver.ChromeOptions()
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        # self.browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
        #                            chrome_options=options)

        # profile = webdriver.FirefoxProfile()
        # profile.add_extension("modify_headers-0.7.1.1-fx.xpi")
        # profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
        # profile.set_preference("modifyheaders.config.active", True)
        # profile.set_preference("modifyheaders.headers.count", 1)
        # profile.set_preference("modifyheaders.headers.action0", "Add")
        # profile.set_preference("modifyheaders.headers.name0", "User-Agent")
        # profile.set_preference("modifyheaders.headers.value0",
        #                        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        # profile.set_preference("modifyheaders.headers.enabled0", True)
        # self.browser = webdriver.Firefox(executable_path=settings['FIREFOX_PATH'], firefox_profile=profile)

        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # desired_capabilities[
        #     "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        # desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'], desired_capabilities=desired_capabilities)


        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()



    def parse(self, response):

        print(response.body)
        sblist = ['http://hk.58.com/ershouche/', 'http://am.58.com/ershouche/', 'http://tw.58.com/ershouche/',
                  'http://diaoyudao.58.com/', 'http://cn.58.com/ershouche/']
        for href in response.xpath('//dl[@id="clist"]/dd/a/@href'):
            url = str(response.urljoin(href.extract()))
            if url not in sblist:
                urlbase=re.findall('\/\/(.*)\.58',url)[0]
                url="http://"+urlbase+".58.com/zhaozu/"
                yield scrapy.Request(url, callback=self.middle3_parse, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

    def middle1_parse(self,response):

        x = response.xpath('//div[@class="filter-wrap"]/dl[1]/dd/a')
        print(x)
        for i in range(1,len(x)-1):
            urlbase=x[i].xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle2_parse, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

    def middle2_parse(self,response):

        x = response.xpath('//dl[@class="secitem secitem-fist"]/dd/div/a')
        for temp in x:
            urlbase = temp.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.middle3_parse, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

    def middle3_parse(self,response):
        x = response.xpath('//div[@class="content-wrap"]/div/ul/li')
        for temp in x:
            url = temp.xpath('div[@class="list-info"]/h2/a/@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_info, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})
        next_page=response.xpath(u'//span[contains(text(),"下一页")]/../@href').extract_first()
        if next_page:
            url=str(next_page)
            yield scrapy.Request(url,callback=self.middle3_parse, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

    def parse_info(self,response):


        # print(response.body)


        item=w58officeitem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        item['city']=response.xpath('//div[contains(@class,"nav-top-bar")]/a[1]/text()').re(u'(.*)58同城')[0] \
            if response.xpath('//div[contains(@class,"nav-top-bar")]/a[1]/text()').re(u'(.*)58同城') else "-"              # 城市

        item['shortdesc']=response.xpath('//div[@class="house-title"]/h1/text()').extract_first().strip() \
            if response.xpath('//div[@class="house-title"]/h1/text()') else "-"              # 简短描述

        district = ""                   # 小区
        if response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[5]/a/text()'):
            district_list = response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[5]/a/text()').extract()
            # flag = 0
            # for i in district_list:
            #     if flag:
            #         district += "," + i
            #     else:
            #         district = i
            #         item['detailed_address'] = i        # 详细地址
            #         flag = 1
        # if district:
        #     item['district'] = district             # 这里逻辑是正确的，不要乱改
        # else:
        #     item['detailed_address'] = "-"

        # item['building']=response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[4]/span[2]/text()').extract_first().strip() \
        #     if response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[4]/span[2]/text()') else "-"                   # 楼盘

        # item['section'] = response.xpath(u'//ul[@class="info"]/li/i[contains(text(),"地段")]/../text()').extract_first().strip() \
        #     if response.xpath(u'//ul[@class="info"]/li/i[contains(text(),"地段")]/../text()') else "-"                    # 地段
        item['section'] = "not found"

        # item['type1'] = response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[2]/span[2]/a/text()').extract_first().strip() \
        #     if response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[2]/span[2]/a/text()') else "-"  # 类别
        #
        # item['area'] = response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[1]/span[2]/text()').extract_first().strip() \
        #     if response.xpath(u'//ul[@class="house_basic_title_content xzl-house_basic_title_content"]/li[1]/span[2]/text()') else "-"  # 面积

        item['type1'] = response.xpath("//div[@class='house-basic-right fr']/div[1]/p[3]/span[1]/a/text()").extract_first().strip() \
            if response.xpath("//div[@class='house-basic-right fr']/div[1]/p[3]/span[1]/a/text()") else "-"

        item['area'] = response.xpath(
            "//*[@class='house-basic-right fr']/div[1]/p[1]/span[1]/text()").extract_first().strip() \
            if response.xpath("//*[@class='house-basic-right fr']/div[1]/p[1]/span[1]/text()") else "-"


        item['price'] = response.xpath(u'//span[@class="house_basic_title_money_num"]/text()').extract_first().strip() \
            if response.xpath(u'//span[@class="house_basic_title_money_num"]/text()') else "-"  # 价格

        item['agent']=response.xpath('//div[@class="house_basic_jingji_all"]/div/a/text()').extract_first().strip() \
            if response.xpath('//div[@class="house_basic_jingji_all"]/div/a/text()').extract_first() else response.xpath('//div[@class="house_basic_jingji"]/p/span/text()').extract_first().strip()                # 联系人

        item['agentcompany'] = response.xpath('//p[@class="jjr-item jjr-belong"]/span[2]/text()').extract_first().strip() \
            if response.xpath('//p[@class="jjr-item jjr-belong"]/span[2]/text()').extract_first() else "-"

        item['posttime']=response.xpath(u'//p[@class="house-update-info"]/span[1]/text()').extract_first() \
            if response.xpath(u'//p[@class="house-update-info"]/span[1]/text()').extract_first() else "-"  # 发布时间

        item['browse']=response.xpath('//p[@class="house-update-info"]/span[2]/text()').extract_first() \
            if response.xpath('//p[@class="house-update-info"]/span[2]/text()').extract_first() else "-"                         # 浏览次数

        item['phone']=response.xpath('//div[@class="house-chat-phone"]/p[@class="phone-num"]/text()').extract_first().strip() \
            if response.xpath('//div[@class="house-chat-phone"]/p[@class="phone-num"]/text()').extract_first() else "-"                         # 联系电话

        # item['creditlevel']=response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() \
        #     if response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() else "-"    # 联系人信用等级
        item['creditlevel'] = "not found"

        # item['agentcompany']=response.xpath(u'//i[contains(text(),"所属公司：")]/../text()[1]').extract_first() \
        #     if response.xpath(u'//i[contains(text(),"所属公司：")]/../text()[1]').extract_first() else "-"       # 联系人所属公司
        # item['agentcompany'] = "not found"

        item['desc'] = response.xpath('//div[@class="general-item general-miaoshu"]/div/text()').extract_first() \
            if response.xpath('//div[@class="general-item general-miaoshu"]/div/text()') else "-"                                            # 描述

        yield item