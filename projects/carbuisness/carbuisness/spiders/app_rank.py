# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import appRankItem
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

website='app_rank'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://mi.talkingdata.com/app-rank.html"
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
        cat_dict = {}
        cats = response.xpath("//*[@class='trans']/span")
        for cat in cats:
            key = cat.xpath("@td-data").extract_first()
            value = cat.xpath('text()').extract_first()
            cat_dict[key] = value
        for item in cat_dict:
            lis = response.xpath("//ol[@td-parent='%d']/li" % int(item))
            for li in lis:
                tid = li.xpath("a/@td-data").extract_first()
                tname = li.xpath("a/text()").extract_first()
                url = "http://mi.talkingdata.com/rank/active.json?date=2017-12-01&typeId=%d&dateType=m&rankingStart=0&rankingSize=30" % int(tid)
                yield scrapy.Request(url,meta={"cat_id":key, "cat_name":value, "sub_cat_id":tid, "sub_cat_name":tname, "index":lis.index(li)}, callback=self.parse_detail)

    def parse_detail(self, response):
        obj = json.loads(response.body)
        for app in obj:
            item = appRankItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(obj.index(app))
            print(item['status'])
            item['cat'] = str(response.meta['cat_id']) + response.meta['cat_name']
            item['sub_cat'] = str(response.meta['sub_cat_id']) + response.meta['sub_cat_name']
            item['appName'] = app['appName']
            item['activeChangeRate'] = app['activeChangeRate']
            item['activeRate'] = app['activeRate']
            item['appIconUrl'] = app['appIconUrl']
            item['appId'] = app['appId']
            item['coverageChangeRate'] = app['coverageChangeRate']
            item['coverageRate'] = app['coverageRate']
            item['newApp'] = app['newApp']
            item['ranking'] = app['ranking']
            item['rankingChange'] = app['rankingChange']
            yield item