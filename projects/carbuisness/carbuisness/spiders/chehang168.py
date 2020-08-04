# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import CheHang168Item
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

website='chehang168'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=index"
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
        brands = json.loads(response.text)
        for brand in brands["l"]["l"][2:]:
            for b in brand["l"]:
                brandid = b["pbid"]
                brandname = b["name"]
                meta = {
                    "brandid": brandid,
                    "brandname": brandname,
                }
                url = "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=infoPseries&pbid=%s" % brandid
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)
        # url_others = "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=infoPseries&pbid=168"
        # yield scrapy.Request(url=url_others, callback=self.parse_others)

    # def parse_others(self, response):
    #     brands = json.loads(response.text)
    #     for brand in brands["l"]["l"]:
    #         brandname = brand["t"]
    #         for family in brand["l"]:
    #             familyname = family["t"]
    #             familyid = family["id"]
    #             url = "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=infoList&psid=%s&mid=0&color=&mode=0&province=&type=0&page=1&price_min=&price_max=" % familyid
    #             yield scrapy.Request(url=url, callback=self.parse_model)

    def parse_family(self, response):
        factories = json.loads(response.text)
        for factory in factories["l"][0]["l"]:
            factoryname = factory["t"]
            for family in factory["l"]:
                familyname = family["t"]
                familyid = family["id"]
                meta = {
                    "factoryname": factoryname,
                    "familyname": familyname,
                    "familyid": familyid,
                }
                url = "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=infoList&psid=%s&mid=0&color=&mode=0&province=&type=0&page=1&price_min=&price_max=" % familyid
                yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_price)

    def parse_price(self, response):
        prices = json.loads(response.text)
        try:
            sum = prices["l"]["mid"][0]["l"][0]["count"]
            total_page = int(sum) / 20 if int(sum) % 20 == 0 else int(sum) / 20 + 1
            for i in range(2, total_page + 1):
                url = "http://api.chehang168.com/a_v48.php?U=08_PNqZ_gwuE87K7Bf&c=info&m=infoList&psid=%s&mid=0&color=&mode=0&province=&type=0&page=%d&price_min=&price_max=" % (response.meta["familyid"], i)
                yield scrapy.Field(url=url, meta=response.meta, callable=self.parse_price)
        except Exception as e:
            print(str(e))

        for price in prices["l"]["l"]:
            item = CheHang168Item()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(prices["l"]["l"].index(price))
            item['priceid'] = price["id"]
            item['title'] = price["title"]
            item['mode'] = price["mode"]
            item['title2'] = price["title2"]
            item['name'] = price["name"]
            item['uid'] = price["uid"]
            item['price'] = price["price"]
            item['pdate'] = price["pdate"]
            item['guideprice'] = price["price_show"]["price1"]
            item['discount'] = price["price_show"]["price2"]

            yield item

