# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import ChezhiwangTousuItem
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

website='chezhiwang_tousu2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml"
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
        tousu_list = response.xpath("//*[@class='tslb_b']/table/tr")
        for tousu in tousu_list[1:]:
            url = tousu.xpath("td[5]/a/@href").extract_first()
            tags = tousu.xpath("td[6]/text()").extract_first()
            meta = {"tags": tags}
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_details)


        for i in range(2, 7346):
            url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-%d.shtml' % i

        # next = response.xpath("//*[@class='p_page']/a[contains(text(), '%s')]" % u"\u4e0b\u4e00\u9875")
        # print(next)
        # if next:
        #     url = next.xpath("@href").extract_first()
            yield scrapy.Request(response.urljoin(url), self.parse)


    def parse_details(self, response):
        item = ChezhiwangTousuItem()

        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url

        item['bianhao'] = response.xpath("//*[@class='jbqk']/ul/li[1]/text()[1]").extract_first().strip()
        item['time'] = response.xpath("//*[@class='jbqk']/ul/li[2]/text()[1]").extract_first().strip()
        item['brand'] = response.xpath("//*[@class='jbqk']/ul/li[3]/text()[1]").extract_first().strip()
        item['family'] = response.xpath("//*[@class='jbqk']/ul/li[4]/text()[1]").extract_first().strip()
        item['model'] = response.xpath("//*[@class='jbqk']/ul/li[5]/text()[1]").extract_first().strip()
        item['content'] = response.xpath("//*[@class='tsnr']/p[1]/text()").extract_first().strip() if response.xpath("//*[@class='tsnr']/p[1]/text()") else response.xpath("//*[@class='tsnr']/p[2]/text()").extract_first().strip()
        item['title'] = response.xpath("//*[@id='newstitle']/text()").extract_first().strip()
        item['tags'] = response.meta["tags"]
        # print(item)
        yield item