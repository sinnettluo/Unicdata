# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeUsersItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import MySQLdb
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymongo

website='autohome_users'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["https://account.autohome.com.cn/"]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
        self.browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=options)

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

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        spec_id_list = list()
        spec_ids = collection.find({"$or": [{"factoryname":"上汽斯柯达"}, {"factoryname":"上汽大众"}]})
        for spec_id in spec_ids:
            spec_id_list.append(spec_id["autohomeid"])
        print(len(spec_id_list))
        print(spec_id_list)

        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'koubei', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select distinct(buyerid),spec_id from autohome_koubei_for_count"
        dbc.execute(sql)
        res = dbc.fetchall()

        for row in res:
            print(row)
            if str(row[1]) in spec_id_list:
                url = "https://i.autohome.com.cn/%s/info" % row[0]
                yield scrapy.Request(url=url, callback=self.parse_info)


    def parse_info(self, response):

        # print(response.body)
        item = AutohomeUsersItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url
        item["userid"] = re.findall("\d+", response.url)[0]
        for p in response.xpath("//*[@id='divuserinfo']/p"):
            if p.xpath("span/text()").extract_first().find("用户名") >= 0:
                item["username"] = p.xpath("text()").extract()[1]
            if p.xpath("span/text()").extract_first().find("昵称") >= 0:
                item["nickname"] = p.xpath("text()").extract_first()
            if p.xpath("span/text()").extract_first().find("性别") >= 0:
                item["sex"] = p.xpath("text()").extract()[1]
            if p.xpath("span/text()").extract_first().find("手机认证") >= 0:
                item["validation"] = p.xpath("em/text()").extract_first()
            if p.xpath("span/text()").extract_first().find("所在地") >= 0:
                item["location"] = p.xpath("text()").extract()[1]
            if p.xpath("span/text()").extract_first().find("生日") >= 0:
                item["birthday"] = p.xpath("text()").extract()[1]

        yield item
        # print(item)
