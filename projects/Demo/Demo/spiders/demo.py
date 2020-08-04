# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
# from .items import DemoSpider Item


class DemoSpider(scrapy.Spider):
    name = 'demo'
    # allowed_domains = ['demo.com']
    # start_urls = ['http://demo.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(DemoSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '',
        'MYSQL_DB': '',
        'MYSQL_TABLE': 'demo',
        'MONGODB_SERVER': '',
        'MONGODB_DB': '',
        'MONGODB_COLLECTION': 'demo',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://demo.com/"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        pass
