# -*- coding: utf-8 -*-
"""

C2017-43-2
易车 经销商(包括4S店和综合店)

"""
import scrapy
from carbuisness.items import yicheXiaoliangItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website ='yiche_xiaoliang_all'

class CarSpider(scrapy.Spider):
    name = website

    #选择城市，从这个入口获得城市信息
    start_urls = []

    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 100000

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        for i in range(2009, 2018):
            for j in range(1, 13):
                for t in ['changshang','pinpai']:
                    url = "http://index.bitauto.com/Interface/GetData.aspx?indexType=xiaoliang&brandType=%s&itemID=0&dateType=m&dateValue=%d&cityID=0&dateYear=%d&pageBlock=indexListMore&levelSpell=" % (t, j, i)
                    yield scrapy.Request(url=url, meta={'i':i, 'j':j, 't':t})
                for l in ['weixingche','xiaoxingche','jincouxingche','zhongxingche','zhongdaxingche','SUV','MPV']:
                    url = "http://index.bitauto.com/Interface/GetData.aspx?indexType=xiaoliang&brandType=level&itemID=0&dateType=m&dateValue=%d&cityID=0&dateYear=%d&pageBlock=indexListMore&levelSpell=%s" % (j, i, l)
                    yield scrapy.Request(url=url, meta={'i':i, 'j':j, 'l':l})
    def parse(self, response):
        lis = response.xpath("//div[@class='rank-list-qian']/ol/li")
        for li in lis:
            item = yicheXiaoliangItem()
            item['month'] = response.meta['j']
            item['year'] = response.meta['i']
            item['order_type'] = response.meta['t'] if response.meta.has_key('t') else response.meta['l']
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['item_name'] = li.xpath("./a/text()").extract_first()
            item['item_url'] = li.xpath("./a/@href").extract_first()
            item['item_order'] = lis.index(li) + 1
            item['item_sales'] = li.xpath("./span/text()").extract_first()
            item['status'] = response.url + str(item['month']) + str(item['year']) + item['order_type'] + str(item['item_order'])
            item['url'] = response.url
            yield item
        # boxes = response.xpath("//*[@class='rank-list-box']")
        # for box in boxes:
        #     item = yicheXiaoliangItem()
        #     item['month'] = response.meta['j']
        #     item['year'] = response.meta['i']
        #     item['order_type'] = box.xpath("./h5/a/text()").extract_first()
        #     item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        #     item['url'] = response.url
        #     lis = box.xpath("./ol/li")
        #     # print(lis)
        #     for li in lis:
        #         item['item_name'] = li.xpath("./a/text()").extract_first()
        #         item['item_url'] = li.xpath("./a/@href").extract_first()
        #         item['item_order'] = lis.index(li) + 1
        #         item['item_sales'] = li.xpath("./span/text()").extract_first()
        #         item['status'] = response.url + str(item['month']) + str(item['year']) + item['order_type'] + str(item['item_order'])
        #         yield item