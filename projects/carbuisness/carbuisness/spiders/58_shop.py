# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import w58shopitem
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

website='58_shop'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.58.com/ershouche/changecity/",
        # "http://lz.58.com/shangpu/31705810263345x.shtml"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


        # self.browser = webdriver.Firefox(executable_path=settings['FIREFOX_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # desired_capabilities[
        #     "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        # desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'],
        #                                    desired_capabilities=desired_capabilities)

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

        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    def parse(self, response):
        print(response.body)
        print "do parse"
        sblist = ['http://hk.58.com/ershouche/', 'http://am.58.com/ershouche/', 'http://tw.58.com/ershouche/',
                  'http://diaoyudao.58.com/', 'http://cn.58.com/ershouche/']

        for href in response.xpath('//dl[@id="clist"]/dd/a/@href'):
            url = str(response.urljoin(href.extract()))
            if url not in sblist:
                urlbase=re.findall('\/\/(.*)\.58',url)[0]
                url="http://"+urlbase+".58.com/shangpucz/"
                print(url)
                # proxy = getProxy()
                # metadata = {"proxy": proxy}
                yield scrapy.Request(url,callback=self.middle1_parse)
                # yield scrapy.Request(url="http://sh.58.com/shangpucz/", callback=self.middle1_parse)
                # yield scrapy.Request(url="http://bj.58.com/shangpucz/", callback=self.middle1_parse)

    def middle1_parse(self,response):
        # metadata = response.meta['metadata']
        x = response.xpath('//div[@class="filter-wrap"]/dl[1]/dd/a')
        for i in range(1,len(x)-1):
            urlbase=x[i].xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url,callback=self.middle2_parse)

    def middle2_parse(self,response):
        # metadata = response.meta['metadata']
        x = response.xpath('//dl[@class="secitem secitem-fist"]/dd/div/a')
        for temp in x:
            urlbase = temp.xpath('@href').extract_first()
            url=response.urljoin(urlbase)
            yield scrapy.Request(url, callback=self.middle3_parse)

    def middle3_parse(self,response):
        # metadata = response.meta['metadata']
        x = response.xpath('//div[@class="content-wrap"]/div/ul/li')
        for temp in x:
            url = temp.xpath('div[@class="list-info"]/h2/a/@href').extract_first()
            yield scrapy.Request(url,callback=self.parse_info)
        next_page=response.xpath(u'//span[contains(text(),"下一页")]/../@href').extract_first()
        if next_page:
            url=str(next_page)
            yield scrapy.Request(url,callback=self.middle3_parse)

    def parse_info(self,response):
        # metadata = response.meta['metadata']
        item=w58shopitem()
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['city'] = response.xpath("//div[@class='header-wrap clearfix']/div/a/text()").extract_first()
        print(item['city'])
        item['city'] = re.findall('^(.*?)58', item['city'])[0]
        item['shortdesc'] = response.xpath("//div[@class='house-title']/h1/text()").extract_first()
        districts = response.xpath("//ul[@class='house_basic_title_content']/li[6]/a")
        item['district'] = ""
        for district in districts:
            item['district'] = item['district'] + district.xpath("text()").extract_first()
        item['address'] = response.xpath("//ul[@class='house_basic_title_content']/li[6]/span[2]/text()").extract_first()
        item['type1'] = response.xpath("//ul[@class='house_basic_title_content']/li[1]/a/text()").extract_first()
        item['area'] = response.xpath("//ul[@class='house_basic_title_content']/li[1]/span[2]/text()").extract_first()
        item['price'] = response.xpath("//span[@class='house_basic_title_money_num']/text()").extract_first()
        item['agent'] = response.xpath("//div[@class='house_basic_jingji']/p/span/text()").extract_first()
        item['posttime'] = response.xpath("//p[@class='house-update-info']/span/text()").extract_first()
        item['browse'] = response.xpath("//*[@id='totalcount']/text()").extract_first()
        item['phone'] = response.xpath("//*[@id='houseChatEntry']/div/p[1]/text()").extract_first()
        item['creditlevel'] = "not found"
        item['agentcompany'] = "not found"

        # item['city']=response.xpath('//span[@id="crumbs"]/a[1]/text()').re(u'(.*)58同城')[0] \
        #     if response.xpath('//span[@id="crumbs"]/a[1]/text()').re(u'(.*)58同城') else "-"
        # item['shortdesc']=response.xpath('//div[@class="w headline"]/h1/text()').extract_first().strip() \
        #     if response.xpath('//div[@class="w headline"]/h1/text()').extract_first() else "-"
        # item['district']=response.xpath('//ul[@class="info"]/li/a[1]/text()').extract_first().strip() \
        #     if response.xpath('//ul[@class="info"]/li/a[1]/text()').extract_first() else "-"
        # item['address']=response.xpath(u'//li[contains(text(),"临近")]/text()').extract_first() \
        #     if response.xpath(u'//li[contains(text(),"临近")]/text()').extract_first() else "-"
        # item['type1']=response.xpath(u'//li[contains(text(),"类型")]/text()').re(u'类型：(.*)')[0].strip() \
        #     if response.xpath(u'//li[contains(text(),"类型")]/text()').re(u'类型：(.*)') else "-"
        # item['area']=response.xpath(u'//li[contains(text(),"面积")]/text()').re('\d+')[0] \
        #     if response.xpath(u'//li[contains(text(),"面积")]/text()').re('\d+') else "-"
        # item['price']=response.xpath(u'//li[contains(text(),"租金：")]/em/text()').extract_first() \
        #     if response.xpath(u'//li[contains(text(),"租金：")]/em/text()').extract_first() else "-"
        # item['agent']=response.xpath('//ul[@class="userinfo"]/li[2]/a/text()').extract_first().strip() \
        #     if response.xpath('//ul[@class="userinfo"]/li[2]/a/text()').extract_first() else "-"
        # item['posttime']=response.xpath(u'//div[contains(text(),"发布时间：")]/text()').re(u'发布时间：(.*)')[0].strip() \
        #     if response.xpath(u'//div[contains(text(),"发布时间：")]/text()').re(u'发布时间：(.*)') else "-"
        # item['browse']=response.xpath('//em[@id="totalcount"]/text()').extract_first() \
        #     if response.xpath('//em[@id="totalcount"]/text()').extract_first() else "-"
        # item['phone']=response.xpath('//span[@class="phone"]/text()').extract_first().strip() \
        #     if response.xpath('//span[@class="phone"]/text()').extract_first() else "-"
        # item['creditlevel']=response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() \
        #     if response.xpath(u'//i[contains(text(),"信用等级：")]/../a/img/@title').extract_first() else "-"
        # item['agentcompany']=response.xpath(u'//i[contains(text(),"所属公司：")]/../text()[1]').extract_first() \
        #     if response.xpath(u'//i[contains(text(),"所属公司：")]/../text()[1]').extract_first() else "-"
        yield item