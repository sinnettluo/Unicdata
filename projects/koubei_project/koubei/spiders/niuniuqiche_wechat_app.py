# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import KBBItem
# from scrapy.conf import settings
import pymongo


website ='niuniuqiche_wechat_app'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['https://www.niuniuqiche.com/wechat_app/v2/brands/brand_list']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')


    # def start_requests(self):
    #
    #     return [scrapy.Request(url="https://www.kbb.com/cars-for-sale/cars/used-cars/", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})]


    def parse(self, response):
       pass