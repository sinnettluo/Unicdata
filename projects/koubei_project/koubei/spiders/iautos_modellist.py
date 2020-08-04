# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import IautosFamilyItem
# from scrapy.conf import settings
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

website ='iautos_modellist_fixed2'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['https://www.iautos.cn/chexing/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 200000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
        self.browser = webdriver.Chrome(
            executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", chrome_options=options)
        super(KoubeiSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        # print(response.text)
        brands = response.xpath("//*[@class='bn']")
        print(brands)
        for brand in brands:
            brandname = brand.xpath("text()").extract_first()
            url = brand.xpath("../@href").extract_first()
            meta = {
                "brandname": brandname,
            }
            if url:
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_factory)

    def parse_factory(self, response):
        factories = response.xpath("//*[@class='p-r-r-2-all-models']/dl/dt")
        # print(factories)
        for factory in factories:
            factoryname = factory.xpath("text()").extract_first()
            families = factory.xpath("//*[@class='p-r-r-2-all-models']/dl/dd["+str(factories.index(factory)+1)+"]/p")
            # print(families)
            for family in families:
                # print(family)
                familyname = family.xpath("a[1]/text()").extract_first()
                # print(familyname)
                url = family.xpath("a[1]/@href").extract_first()
                print(url)
                familyid = url.split("=")[-1]
                meta = {
                    "factoryname": factoryname,
                    "familyname": familyname,
                    "familyid": familyid,
                }
                meta = dict(meta, **response.meta)
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_ershouche)




    def parse_ershouche(self, response):
        item = IautosFamilyItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url
        item['brandname'] = response.meta["brandname"]
        item['factoryname'] =  response.meta["factoryname"]
        item['familyname'] = response.meta["familyname"]
        item['familyid'] = response.meta["familyid"]
        item['ershou_brand'] = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first().split("/")[-4]
        item['ershou_factory'] = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first().split("/")[-3]
        item['ershou_family'] = response.xpath("//*[@class='box3']/div[2]/a[3]/@href").extract_first().split("/")[-2]

        # print(item)
        yield item






