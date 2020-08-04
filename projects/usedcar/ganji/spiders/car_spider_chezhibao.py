#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
import logging
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update

website ='chezhibao'
spidername_new = 'chezhibao_new'
spidername_update = 'chezhibao_update'

class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    start_urls = [
        # "http://m.chezhibao.com/optauction/list/1_0_0_0_0_0_0.htm?brand_=&mode_="
        "https://search.chezhibao.com/auctionHistory/list.htm?page=1&brand=0&mode=0&year=0&mileage=0"
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

    # def start_requests(self):
    #     for i in range(1,321):
    #         url="http://m.chezhibao.com/optauction/list/"+str(i)+"_0_0_0_0_0_0.htm?brand_=&mode_="
    #         yield scrapy.Request(url,callback=self.parse)

    def parse(self,response):

        next_page = response.xpath("//*[@class='_btn _next']/@href").extract_first()
        url = response.urljoin(next_page)
        yield scrapy.Request(url=url, callback=self.parse)

        divs = response.xpath("//*[@class='__loop']")
        for div in divs:
            url = response.urljoin(div.xpath('div[1]/div[1]/a/@href').extract_first())
            yield scrapy.Request(url=url, callback=self.parse_detail)



    def parse_detail(self, response):

        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['pagetime'] = "zero"
        item['datasave'] = [response.xpath('//html').extract_first()]
        yield item

