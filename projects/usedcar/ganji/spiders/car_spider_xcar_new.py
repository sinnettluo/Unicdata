# -*- coding: utf-8 -*-
import scrapy


class CarSpiderXcarNewSpider(scrapy.Spider):
    name = "xcarnew"
    # allowed_domains = ["used.xcar.com.cn"]
    start_urls = (
        'http://poe.qq.com/',
    )

    def parse(self, response):
        print(123)
        pass
