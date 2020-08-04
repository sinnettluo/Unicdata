# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import AutohomeCustomPriceItem
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
import MySQLdb

website='autohome_custom_price2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "https://www.autohome.com.cn/beijing/"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):

        # yield scrapy.Request("https://jiage.autohome.com.cn/price/carlist/p-28763", callback=self.parse_list, dont_filter=True)

        mysqldb = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", "newcar_test", port=3306)
        dbc = mysqldb.cursor()
        mysqldb.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select autohomeid from autohomeall"
        dbc.execute(sql)
        res = dbc.fetchall()

        for row in res:
            url = "https://jiage.autohome.com.cn/price/carlist/p-%s-1-0-0-0-0-1-110100" % row[0]
            yield scrapy.Request(url=url, meta={"autohomeid":row[0]}, callback=self.parse_list)

        # url = "https://jiage.autohome.com.cn/price/carlist/p-1000001"
        # yield scrapy.Request(url=url, meta={"autohomeid": "1000001"}, callback=self.parse_list)

    def parse_list(self, response):
        print(response.xpath("//*[@class='nextbtn iconfont iconfont-youjiantou']"))
        if response.xpath("//*[@class='nextbtn iconfont iconfont-youjiantou']"):
            print("$$$$$$$$$$$$$$next page$$$$$$$$$$$$$$")
            page_num = re.findall("\-1\-0\-0\-0\-0\-(.*?)\-110100", response.url)[0]
            next_num = int(page_num) + 1
            url = re.sub("\-1\-0\-0\-0\-0\-(.*?)\-110100", str(next_num), response.url)
            yield scrapy.Request(url=url, meta={"autohomeid":response.meta["autohomeid"]}, callback=self.parse_list)
        else:
            print("$$$$$$$$$$$$$$no next page$$$$$$$$$$$$$$")



        price_boxes = response.xpath("//*[@class='car-lists']")
        for box in price_boxes:
            item = AutohomeCustomPriceItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            # item['status'] = response.url + "-" + str(price_boxes.index(box))
            item['username'] =  box.xpath('//*[@class="car-lists-item-use-name-detail "]/text()').extract_first()
            item['autohomeid'] = response.meta["autohomeid"]
            item['userid'] = box.xpath('//*[@class="car-lists-item-use-name-detail "]/@href').re("\d+")[0]
            item['fapiao'] = box.xpath('//*[@class="mark-receipt"]/text()').extract_first()
            brand_and_family = response.xpath("//*[@class='athm-sub-nav__car__name']/a//text()").extract()
            item['car_model'] = "".join(brand_and_family) + box.xpath('//*[@class="car-lists-item-top-middle"]/p/text()').extract_first()

            item['guide_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[2].replace("'", "").replace("'", "")
            item['total_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[1].replace("'", "").replace("'", "")
            item['naked_price'] = response.xpath("/html/ul/li[%d]/text()" % (price_boxes.index(box) + 1)).extract_first().split("-")[0].replace("'", "").replace("'", "")

            item['tax'] = box.xpath('li/div[2]/ol/li[5]/span[2]/text()').extract_first()
            item['jiaoqiangxian'] = box.xpath('li/div[2]/ol/li[6]/span[2]/text()').extract_first()
            item['chechuanshui'] = box.xpath('li/div[2]/ol/li[4]/span[2]/text()').extract_first()
            item['shangyexian'] = box.xpath('li/div[2]/ol/li[7]/span[2]/text()').extract_first()
            item['shangpaifei'] = box.xpath('li/div[2]/ol/li[8]/span[2]/text()').extract_first()
            item['pay_mode'] = box.xpath('li/div[2]/ol/li[9]/span[2]/text()').extract_first()
            # item['promotion_set'] = "".join(box.xpath('li/div[2]/ol/li[10]/span[2]//text()').extract())
            item['buy_date'] = box.xpath('//*[@class="bought-time"]/time/text()').extract_first()
            item['buy_location'] = box.xpath('//*[@class="bought-location"]/text()').extract_first()
            item['dealer'] = box.xpath('//*[@class="business"]/a/text()').extract_first() if box.xpath('//*[@class="business"]/a') else "-"
            item['dealerid'] = box.xpath('//*[@class="business"]/a/@href').re("\d+")[0] if box.xpath('//*[@class="business"]/a') else "-"
            item['tel'] = box.xpath('//*[@class="tel-wrapper grey"]/tel/text()').extract_first() if box.xpath('//*[@class="tel-wrapper grey"]/tel') else "-"
            item['dealer_addr'] = box.xpath('//*[@class="loc-wrapper grey"]/span/text()').extract_first() if box.xpath('//*[@class="loc-wrapper grey"]/span') else "-"
            item['star_level'] = int(box.xpath('//*[@class="score-num"]/@style').re("\d+")[0])/20 if box.xpath('//*[@class="score-num"]') else "-"
            item['service_level'] = box.xpath('//*[@class="evaluate"]/text()').extract_first() if box.xpath('//*[@class="evaluate"]') else "-"
            # item['cutting_skill'] = "".join(box.xpath('li/div[2]/ol/li[11]/span[2]//text()').extract())
            item['cutting_skill'] = "-"
            item['status'] = str(item['autohomeid']) + "-" + str(item['userid']) + "-" + str(
                item['buy_location']) + "-" + str(item['buy_date']) + "-" + str(item['naked_price']) + time.strftime('%Y-%m', time.localtime())

            # print(item)
            yield item

        # price_boxes = response.xpath("//*[@class='price-boxs']")
        # for box in price_boxes:
        #     item = AutohomeCustomPriceItem()
        #     item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        #     item['url'] = response.url
        #     # item['status'] = response.url + "-" + str(price_boxes.index(box))
        #     item['username'] = box.xpath('div[1]/div[2]/a/text()').extract_first()
        #     item['autohomeid'] = response.meta["autohomeid"]
        #     item['userid'] = box.xpath('div[1]/div[2]/a/@href').re("\d+")[0]
        #     item['fapiao'] = box.xpath('div[1]/div[3]/span/text()').extract_first()
        #     item['car_model'] = box.xpath('div[2]/span[1]/a/text()').extract_first()
        #     item['guide_price'] = box.xpath('div[2]/span[2]/span/text()').extract_first()
        #     item['total_price'] = box.xpath('div[3]/ul/li[1]/h3/em/text()').extract_first()
        #     item['naked_price'] = box.xpath('div[3]/ul/li[2]/span[2]/text()').extract_first()
        #     item['tax'] = box.xpath('div[3]/ul/li[2]/span[4]/text()').extract_first()
        #     item['jiaoqiangxian'] = box.xpath('div[3]/ul/li[2]/span[6]/text()').extract_first()
        #     item['chechuanshui'] = box.xpath('div[3]/ul/li[3]/span[2]/text()').extract_first()
        #     item['shangyexian'] = box.xpath('div[3]/ul/li[3]/span[4]/text()').extract_first()
        #     item['shangpaifei'] = box.xpath('div[3]/ul/li[3]/span[6]/text()').extract_first()
        #     item['pay_mode'] = box.xpath('div[3]/ul/div/li/span[2]/text()').extract_first()
        #     item['promotion_set'] = box.xpath('div[3]/ul/li[4]/span[2]/text()').extract_first()
        #     item['buy_date'] = box.xpath('div[3]/ul/li[5]/span[2]/text()').extract_first()
        #     item['buy_location'] = box.xpath('div[3]/ul/li[5]/span[4]/text()').extract_first()
        #     item['dealer'] = box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[1]/span/a/text()').extract_first() if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[1]/span/a/text()') else "-"
        #     item['dealerid'] = box.xpath('div[3]/ul/li[6]/span[2]/span[1]/p[1]/span/a/@href').re("\d+")[0] if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[1]/span/a/@href') else "-"
        #     item['tel'] = box.xpath('div[3]/ul/li[6]/span[2]/span[1]/p[2]/em/text()').extract_first() if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[2]/em/text()') else "-"
        #     item['dealer_addr'] = box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[3]/span[1]/text()').extract_first() if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[1]/p[3]/span[1]/text()') else "-"
        #     item['star_level'] = int(
        #         box.xpath('div[3]/ul/li[6]/span[2]/span[2]/div/span/b/@style').re("\d+")[0]) / 20 if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[2]/div/span/b/@style') else "-"
        #     item['service_level'] = box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[2]/span/span/text()').extract_first() if box.xpath(
        #         'div[3]/ul/li[6]/span[2]/span[2]/span/span/text()') else "-"
        #     item['cutting_skill'] = box.xpath('div[3]/ul/li[7]/span[2]/text()').extract_first()
        #     item['status'] = str(item['autohomeid']) + "-" + str(item['userid']) + "-" + str(
        #         item['buy_location']) + "-" + str(item['buy_date']) + "-" + str(item['naked_price'])
        #
        #     yield item