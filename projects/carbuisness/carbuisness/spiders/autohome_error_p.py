# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeErrorItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import MySQLdb
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymongo

website='autohome_error_p'

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
            url1 = "https://k.m.autohome.com.cn/seriesQuality/indexh5?sid=%s&carType=1" % family
            url2 = "https://k.m.autohome.com.cn/seriesQuality/indexh5?sid=%s&carType=2" % family
            urls.append(scrapy.Request(url=url1, meta={"category_id":1, "familyid": family}))
            urls.append(scrapy.Request(url=url2, meta={"category_id":2, "familyid": family}))
        return urls


        # urls = []
        # for family in families:
        #     for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"]:
        #         meta = {"category_id":i}
        #         url = "https://k.m.autohome.com.cn/app/seriesQuality/getCategory?seriesId=%s&cid=%s" % (family, i)
        #         request = scrapy.Request(url=url, meta=meta)
        #         urls.append(request)
        # return urls

    def parse(self, response):

        # print(response.body)
        data = re.findall("data\: \[(.*?)\]", response.body, re.S)[0]
        if data:
            # print(data)
            data_obj = json.loads("[" + data + "]")
            item = AutohomeErrorItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item["status"] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
            item["waiguan1"] = "-"
            item["xingshi1"] = "-"
            item["caozuo1"] = "-"
            item["dianzi1"] = "-"
            item["zuoyi1"] = "-"
            item["kongtiao1"] = "-"
            item["neishi1"] = "-"
            item["fadongji1"] = "-"
            item["biansuxitong1"] = "-"
            if response.meta["category_id"] == 1:
                for d in data_obj:
                    item["waiguan1"] = d["value"] if d["id"] == "01" and item["waiguan1"] == "-" else item["waiguan1"]
                    item["xingshi1"] = d["value"] if d["id"] == "02" and item["xingshi1"] == "-" else item["xingshi1"]
                    item["caozuo1"] = d["value"] if d["id"] == "03" and item["caozuo1"] == "-" else item["caozuo1"]
                    item["dianzi1"] = d["value"] if d["id"] == "04" and item["dianzi1"] == "-" else item["dianzi1"]
                    item["zuoyi1"] = d["value"] if d["id"] == "05" and item["zuoyi1"] == "-" else item["zuoyi1"]
                    item["kongtiao1"] = d["value"] if d["id"] == "06" and item["kongtiao1"] == "-" else item["kongtiao1"]
                    item["neishi1"] = d["value"] if d["id"] == "07" and item["neishi1"] == "-" else item["neishi1"]
                    item["fadongji1"] = d["value"] if d["id"] == "08" and item["fadongji1"] == "-" else item["fadongji1"]
                    item["biansuxitong1"] = d["value"] if d["id"] == "09" and item["biansuxitong1"] == "-" else item["biansuxitong1"]
            else:
                for d in data_obj:
                    item["fadongji1"] = d["value"] if d["id"] == "10" and item["fadongji1"] == "-" else item["fadongji1"]
                    item["neishi1"] = d["value"] if d["id"] == "11" and item["neishi1"] == "-" else item["neishi1"]
                    item["kongtiao1"] = d["value"] if d["id"] == "12" and item["kongtiao1"] == "-" else item["kongtiao1"]
                    item["zuoyi1"] = d["value"] if d["id"] == "13" and item["zuoyi1"] == "-" else item["zuoyi1"]
                    item["dianzi1"] = d["value"] if d["id"] == "14" and item["dianzi1"] == "-" else item["dianzi1"]
                    item["caozuo1"] = d["value"] if d["id"] == "15" and item["caozuo1"] == "-" else item["caozuo1"]
                    item["xingshi1"] = d["value"] if d["id"] == "16" and item["xingshi1"] == "-" else item["xingshi1"]
                    item["waiguan1"] = d["value"] if d["id"] == "17" and item["waiguan1"] == "-" else item["waiguan1"]
            item["familyid"] = response.meta["familyid"]
            item["category_id"] = response.meta["category_id"]
            item["json"] = data
            item["sum"] = response.xpath("//*[@class='piechart']/h4/span[2]/text()[1]").extract_first().strip()

            # print(item)
            yield item