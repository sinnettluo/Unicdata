# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeLatestOrderItem
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
import MySQLdb

website='autohome_latest_order'

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

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def parse(self, response):

        mysqldb = MySQLdb.connect("192.168.2.120", "root", "ABCabc123", "peoplez", port=3306)
        dbc = mysqldb.cursor()
        mysqldb.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select dealerId from autohome_store_net"
        dbc.execute(sql)
        res = dbc.fetchall()

        for row in res:
            url = "https://dealer.autohome.com.cn/Ajax/GetDealerLatestOrderList?dealerId=%s&companyId=%s" % (row[0], row[0])
            yield scrapy.Request(url, callback=self.parse_info)


    def parse_info(self, response):
        order_list = json.loads(response.body.replace("\/", "").decode("GBK"))
        for d_item in order_list:
            for order in d_item:
                item = AutohomeLatestOrderItem()
                item['dateString'] = order['DateString']
                item['orderType'] = order['OrderType']
                item['customerSex'] = order['CustomerSex']
                item['customerName'] = order['CustomerName']
                item['cityName'] = order['CityName']
                item['createTime'] = order['CreateTime']
                item['status'] = response.url + str(d_item.index(order)) + str(order_list.index(d_item)) + time.strftime('%Y-%m', time.localtime())
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                yield item




