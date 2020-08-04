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

website='zgc_mobile_phone'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html"
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
        hrefs = response.xpath("//div[@id='J_BrandAll']/a")
        for href in hrefs:
            url = response.urljoin(href.xpath("@href").extract_first())
            yield scrapy.Request(url, callback=self.parse_series)

    def parse_series(self, response):
        hrefs = re.findall("/series/57/\d+_1\.html", response.body, re.S)
        for href in hrefs:
            brand_id = re.findall("subcate57_(\d+)_list", response.url)[0]
            series_id = re.findall("\d+", href)[1]
            url = "http://detail.zol.com.cn/series/57/%s/param_%s_0_1.html" % (brand_id, series_id)
            print(url)
            yield scrapy.Request(url, callback=self.parse_config)


    def parse_config(self, response):
        print(response.xpath('//*[@id="seriesParamTable"]/tr[3]/td[1]/div/span[1]/b/text()').extract_first())
        print(response.xpath('//*[@id="seriesParamTable"]/tr[1]/td[1]/a/text()').extract_first())
        print(response.xpath('//*[@id="seriesParamTable"]/tr[5]/td[1]/text()').extract_first())

