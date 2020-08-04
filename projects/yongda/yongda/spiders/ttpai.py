# -*- coding: utf-8 -*-
import scrapy
import time
import json
import logging
from yongda.items import chesupaiItem

website = 'ttpai'


class TtpaiSpider(scrapy.Spider):
    name = website
    allowed_domains = ['ttpai.cn']

    # start_urls = ['http://ttpai.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(TtpaiSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '127.0.0.1',
        'MYSQL_DB': 'yongda',
        'MYSQL_TABLE': 'ttpai',
        'MONGODB_SERVER': '127.0.0.1',
        'MONGODB_DB': 'yongda',
        'MONGODB_COLLECTION': 'ttpai',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://www.ttpai.cn/buy/quanguo/blist"
        yield scrapy.Request(
            url=url,
        )

    # get car list
    def parse(self, response):
        datacheck = len(response.xpath("//html").extract_first())
        if datacheck > 20000:
            # as list
            for href in response.xpath('//li[@class="item"]'):
                urlbase = href.xpath("a/@href").extract_first()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)

    # get car info
    def parse_car(self, response):
        # key and status (sold or sale, price,time)
        status = "sold"
        price = response.xpath('//strong[@class="s-orange"]/text()')
        price = ".".join(price.re('\d+')) if price else "zero"
        datetime = "zero"
        # item loader
        item = chesupaiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + str(datetime)
        item['pagetime'] = datetime
        # yield item
        print(item)
