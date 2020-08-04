# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeErrorItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
# import MySQLdb
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
# from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymongo

website='autohome_error'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []


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
        #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
        # self.browser = webdriver.Chrome(
        #     executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=options)

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

    def start_requests(self):

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]
        families = collection.distinct("familyid")


        urls = []
        for family in families:
            for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"]:
                meta = {"category_id":i}
                url = "https://k.m.autohome.com.cn/app/seriesQuality/getCategory?seriesId=%s&cid=%s" % (family, i)
                request = scrapy.Request(url=url, meta=meta)
                urls.append(request)
        return urls

    def parse(self, response):

        # print(response.body)

        item = AutohomeErrorItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        # item["waiguan1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[1]/dl/dd/span/span/text()').extract_first()
        # item["xingshi1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[2]/dl/dd/span/span/text()').extract_first()
        # item["caozuo1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[3]/dl/dd/span/span/text()').extract_first()
        # item["dianzi1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[4]/dl/dd/span/span/text()').extract_first()
        # item["zuoyi1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[5]/dl/dd/span/span/text()').extract_first()
        # item["kongtiao1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[6]/dl/dd/span/span/text()').extract_first()
        # item["neishi1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[7]/dl/dd/span/span/text()').extract_first()
        # item["fadongji1"] = response.xpath('//*[@id="quality-chart-box-01"]/div[2]/div[2]/a[8]/dl/dd/span/span/text()').extract_first()
        # item["waiguan2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[8]/dl/dd/span/span/text()').extract_first()
        # item["xingshi2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[7]/dl/dd/span/span/text()').extract_first()
        # item["caozuo2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[6]/dl/dd/span/span/text()').extract_first()
        # item["dianzi2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[5]/dl/dd/span/span/text()').extract_first()
        # item["zuoyi2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[4]/dl/dd/span/span/text()').extract_first()
        # item["kongtiao2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[3]/dl/dd/span/span/text()').extract_first()
        # item["neishi2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[2]/dl/dd/span/span/text()').extract_first()
        # item["fadongji2"] = response.xpath('//*[@id="quality-chart-box-02"]/div[2]/div[2]/a[1]/dl/dd/span/span/text()').extract_first()
        item["familyid"] = re.findall("\d+", response.url)[0]
        item["category_id"] = response.meta["category_id"]
        item["json"] = response.body

        # print(item)
        if item["json"] and item["json"] != "\"[]\"":
            yield item