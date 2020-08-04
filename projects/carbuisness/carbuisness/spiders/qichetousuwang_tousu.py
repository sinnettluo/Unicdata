# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import QicheTousuItem
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

website='qichetousuwang_tousu'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.qctsw.com/tousu/tslist/1_0_1.html"
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
        ts_list = response.xpath("//*[@class='tousuList']/ul/li")
        for ts in ts_list:
            id = ts.xpath("h3").re("var id=\"(\d+)\"")[0]
            url = "/tousu/content/%s.html" % id
            # print(url)
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse_details)

        total = response.xpath("//a[@title='Total record']/text()").re("\d+")[0]
        total_page = int(total)/20 if int(total)%20 == 0 else int(total)/20 + 1
        for i in range(1, total_page):
            list_url = "http://www.qctsw.com/tousu/tslist/1_%d_1.html" % i
            yield scrapy.Request(url=list_url, callback=self.parse)


    def parse_details(self, response):
        item = QicheTousuItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url

        item['bianhao'] = response.xpath("//div[@class='tableBox']/table/tr[1]/td[1]/b/text()").extract_first().strip()
        item['time'] = response.xpath("//div[@class='titleNav fix']/p[2]/em[1]/b/text()").extract_first().strip()
        item['brand'] = response.xpath("//div[@class='tableBox']/table/tr[1]/td[2]/a[1]/text()").extract_first().strip()
        item['family'] = response.xpath("//div[@class='tableBox']/table/tr[1]/td[2]/a[2]/text()").extract_first().strip()
        item['model'] = response.xpath("//div[@class='tableBox']/table/tr[2]/td[2]/text()").extract_first().strip()
        item['content'] = "".join(response.xpath("//*[@class='articleContent']/p/text()").extract())
        item['title'] = response.xpath("//*[@class='articleTit']/text()").extract_first().strip()
        tags = response.xpath("//*[@class='pBox fix']")
        tag_list = list()
        for tag in tags:
            tagname = tag.xpath("a/text()").extract_first().strip() if tag.xpath("a/text()") else ""
            if tag.xpath("a/b"):
                tagname = tagname + "(" + tag.xpath("a/b/text()").extract_first().strip() + ")"
            tag_list.append(tagname)
        item["tags"] = "|".join(tag_list)
        # item['company'] = scrapy.Field()
        # item['satisfied'] = scrapy.Field()
        item['user'] = response.xpath("//div[@class='tableBox']/table/tr[2]/td[1]/text()").extract_first().strip()
        item['location'] = response.xpath("//div[@class='tableBox']/table/tr[4]/td[1]/a[1]/text()").extract_first().strip() + "-" + response.xpath("//div[@class='tableBox']/table/tr[4]/td[1]/a[2]/text()").extract_first().strip()
        item['car_status'] = response.xpath("//div[@class='tableBox']/table/tr[5]/td[1]/a/text()").extract_first().strip()
        item['miles'] = response.xpath("//div[@class='tableBox']/table/tr[6]/td[1]/text()").extract_first().strip() if response.xpath("//div[@class='tableBox']/table/tr[6]/td[1]/text()") else "-"
        item['buy_date'] = response.xpath("//div[@class='tableBox']/table/tr[7]/td[1]/text()").extract_first().strip()
        item['car_type'] = response.xpath("//div[@class='tableBox']/table/tr[3]/td[2]/a/text()").extract_first().strip()
        item['sstore'] = response.xpath("//div[@class='tableBox']/table/tr[4]/td[2]/text()").extract_first().strip()
        item['sstore_contact'] = response.xpath("//div[@class='tableBox']/table/tr[5]/td[2]/text()").extract_first().strip()
        item['sstore_tel'] = response.xpath("//div[@class='tableBox']/table/tr[6]/td[2]/text()").extract_first().strip()
        item['requirements'] = "|".join(response.xpath("//div[@class='tableBox']/table/tr[7]/td[2]/i/a/text()").extract())

        # print(item)
        yield item