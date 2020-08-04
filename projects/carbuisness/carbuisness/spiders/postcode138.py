# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import PostCode138Item
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
from lxml import etree
import requests
import codecs

website='postcode138'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://alexa.ip138.com/post/search.asp"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


        with codecs.open("D:/county.txt", "r", "utf-8") as f:
            filecontent = f.read()
            # print(filecontent)
            indexlist = re.findall("\d+\_\d+\_\d+|\d+\_\d+", filecontent)
            indexlist.append("0")
            # print(indexlist)
            datalist = re.findall("\[(.*?)\]", filecontent, re.S)
            # print(datalist)
        self.datadict = {}
        for index in indexlist:
            self.datadict[index] = datalist[indexlist.index(index)]

        # print(self.datadict)

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        # rids = response.xpath("//*[@id='regionid']/option")[1:]
        # print(rids)
        rids = self.datadict["0"].split(",")
        for rid in rids:
            regionid = rid.split("|")[1].replace("\"", "")
            regionname = rid.split("|")[0].replace("\"", "")
            cids = self.datadict["0_%d" % (int(regionid)-1)].split(",")
            for cid in cids:
                cityid = cid.split("|")[1].replace("\"", "")
                cityname = cid.split("|")[0].replace("\"", "")
                try:
                    coids = self.datadict["0_%d_%d" % (int(regionid)-1, cids.index(cid))].split(",")
                    for coid in coids:
                        countyid = coid.split("|")[1].replace("\"", "")
                        countyname = coid.split("|")[0].replace("\"", "")
                        data = {
                            "regionid":regionid,
                            "cityid":cityid,
                            "countyid":countyid,
                            "address":""
                        }
                        meta = dict(data, **{
                            "regionname":regionname,
                            "cityname":cityname,
                            "countyname":countyname
                        })
                        print(data)
                        url = "http://alexa.ip138.com/post/search.asp?page=1&regionid=%d&cityid=%d&countyid=%d&address=" % (int(regionid), int(cityid), int(countyid))
                        # print(data)
                        yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)
                except Exception as e:
                    countyid = ""
                    countyname = ""
                    data = {
                        "regionid": regionid,
                        "cityid": cityid,
                        "countyid": countyid,
                        "address": ""
                    }
                    meta = dict(data, **{
                        "regionname": regionname,
                        "cityname": cityname,
                        "countyname": countyname
                    })
                    print(data)
                    url = "http://alexa.ip138.com/post/search.asp?page=1&regionid=%d&cityid=%d&countyid=%s&address=" % (int(regionid), int(cityid), countyid)
                    # print(data)
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)

    def parse_list(self, response):
        trs = response.xpath("//table[@class='t12']/tr")[1:-1]
        print(trs)
        for tr in trs:
            item = PostCode138Item()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(trs.index(tr))
            item['regionid'] = response.meta["regionid"]
            item['regionname'] = response.meta["regionname"]
            item['cityid'] = response.meta["cityid"]
            item['cityname'] = response.meta["cityname"]
            item['countyid'] = response.meta["countyid"]
            item['countyname'] = response.meta["countyname"]
            item['address'] = tr.xpath("td[1]/text()").extract_first()
            item['postcode'] = tr.xpath("td[2]/text()").extract_first()
            # print(item)
            yield item

        next = response.xpath("//a")
        for a in next:
            if a.xpath("text()").extract_first() == u"\u4e0b\u4e00\u9875":
                yield scrapy.Request(url=response.urljoin(a.xpath("@href").extract_first()), meta=response.meta, callback=self.parse_list)

            







