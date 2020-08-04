# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import JDItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests

website='jd_fix2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        # "https://coll.jd.com/list.html?sub=46994",
        "https://list.jd.com/list.html?cat=6728,6742,11849",
        # "https://list.jd.com/list.html?cat=6728,6742,9248",
        # "https://list.jd.com/list.html?cat=6728,6742,11850",
        # "https://list.jd.com/list.html?cat=6728,6742,6756",
        "https://coll.jd.com/list.html?sub=23851",
        # "https://list.jd.com/list.html?cat=6728,6742,9971",
        # "https://list.jd.com/list.html?cat=6728,6742,13992",
        # "https://list.jd.com/list.html?cat=6728,6742,6766",
        # "https://coll.jd.com/list.html?sub=23867",
        # "https://list.jd.com/list.html?cat=6728,6742,6767",
        # "https://coll.jd.com/list.html?sub=23843",
        # "https://list.jd.com/list.html?cat=6728,6742,11951",
        # "https://list.jd.com/list.html?cat=6728,6742,6769",
        # "https://list.jd.com/list.html?cat=6728,6742,13246",
        # "https://list.jd.com/list.html?cat=6728,6742,13243",
        # "https://list.jd.com/list.html?cat=6728,6742,13244",
        # "https://list.jd.com/list.html?cat=6728,6742,13245",
        # "https://list.jd.com/list.html?cat=6728,6742,6795",
        # "https://list.jd.com/list.html?cat=6728,6742,12406",
        # "https://coll.jd.com/list.html?sub=42052",
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000

        self.cate_dict = {
            "https://coll.jd.com/list.html?sub=46994":"京东保养",
            "https://list.jd.com/list.html?cat=6728,6742,11849":"汽机油",
            "https://list.jd.com/list.html?cat=6728,6742,9248":"轮胎",
            "https://list.jd.com/list.html?cat=6728,6742,11850":"添加剂",
            "https://list.jd.com/list.html?cat=6728,6742,6756":"防冻液",
            "https://coll.jd.com/list.html?sub=23851":"滤清器",
            "https://list.jd.com/list.html?cat=6728,6742,9971":"蓄电池",
            "https://list.jd.com/list.html?cat=6728,6742,13992":"变速箱油/滤",
            "https://list.jd.com/list.html?cat=6728,6742,6766":"雨刷",
            "https://coll.jd.com/list.html?sub=23867":"刹车片/盘",
            "https://list.jd.com/list.html?cat=6728,6742,6767":"火花塞",
            "https://coll.jd.com/list.html?sub=23843":"车灯",
            "https://list.jd.com/list.html?cat=6728,6742,11951":"轮毂",
            "https://list.jd.com/list.html?cat=6728,6742,6769":"维修配件",
            "https://list.jd.com/list.html?cat=6728,6742,13246":"汽车玻璃",
            "https://list.jd.com/list.html?cat=6728,6742,13243":"减震器",
            "https://list.jd.com/list.html?cat=6728,6742,13244":"正时皮带",
            "https://list.jd.com/list.html?cat=6728,6742,13245":"汽车喇叭",
            "https://list.jd.com/list.html?cat=6728,6742,6795":"汽修工具",
            "https://list.jd.com/list.html?cat=6728,6742,12406":"改装配件",
            "https://coll.jd.com/list.html?sub=42052":"原厂件",
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()


    # def start_requests(self):
    #     urls = []
    #     for i in range(20):
    #         url = "http://was.mot.gov.cn:8080/govsearch/searPagenew.jsp?page="+ str(i) +"&pubwebsite=zfxxgk&indexPa=2&schn=601&sinfo=571&surl=zfxxgk/&curpos=%E4%BA%A4%E9%80%9A%E8%BF%90%E8%BE%93%E9%83%A8%E4%BB%A4"
    #         urls.append(scrapy.Request(url=url))
    #     return  urls


    # def parse(self, response):
    #     print(response.text)
    #     urls = response.xpath("//*[@clstag='h|keycount|head|category_09d05']/a/@href").extract()
    #     print(urls)
    #     for url in urls:
    #         meta = {
    #             "category": url.xpath("../text()").extract_first()
    #         }
    #         yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_product)

    def parse(self, response):

        category = ""

        # print(response.text)
        products = response.xpath("//*[@class='gl-item']")
        for product in products:
            name = product.xpath(".//*[@class='p-name']/a/em/text()").extract_first().strip()
            id = product.xpath("div/@data-sku").extract_first()
            try:
                store = product.xpath(".//*[@class='p-shopname']/a/text()").extract_first().strip()
            except Exception as e:
                try:
                    storeid = product.xpath("div/@venderid").extract_first().strip()
                    storeid_zy = product.xpath("div/@jdzy_shop_id").extract_first().strip()
                    if storeid == storeid_zy:
                        store = "自营"
                    else:
                        store = "非自营"
                except Exception as e1:
                    try:
                        storeid = product.xpath("@venderid").extract_first().strip()
                        storeid_zy = product.xpath("@jdzy_shop_id").extract_first().strip()
                        if storeid == storeid_zy:
                            store = "自营"
                        else:
                            store = "非自营"
                    except Exception as e2:
                        store = "无法判断"

            for cate in self.cate_dict:
                if response.url.find(cate) >= 0:
                    category = self.cate_dict[cate]
            meta = {
                "store":store,
                "name": name,
                "id": id,
                "category": category,
            }
            url = "https://p.3.cn/prices/mgets?callback=jQuery7280208&ext=11101100&type=1&area=2_2823_51974_0&skuIds=J_"+str(id)+"&pdbp=0&pdtk=&pdpin=&pin=&pduid=364417154&source=list_pc_front&_=1560329333694"
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_price)

        next = response.xpath("//*[@class='pn-next']")
        if next:
            yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), callback=self.parse)


    # def parse_price(self, response):
    #     price = json.loads(response.text.replace("jQuery7280208([", "").replace("]);", ""))["p"]
    #     meta = dict({"price":price}, **response.meta)
    #     url = "https://chat1.jd.com/api/checkChat?my=list&pidList="+str(response.meta["id"])+"&callback=jQuery6087705&_=1560330959600"
    #     yield scrapy.Request(url=url, meta=meta, callback=self.parse_seller)


    def parse_price(self, response):
        # print(response.text.replace("jQuery8088936([", "").replace("])", ""))
        price = json.loads(response.text.replace("jQuery7280208([", "").replace("]);", ""))["p"]
        item = JDItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['category'] = response.meta['category']
        item['status'] = response.meta['id']
        item['name'] = response.meta['name']
        item['store'] = response.meta['store']
        item['price'] = price

        # print(item)
        yield item