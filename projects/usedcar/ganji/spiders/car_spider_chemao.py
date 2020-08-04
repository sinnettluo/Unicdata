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


website ='chemao'
spidername_new = 'chemao_new'
spidername_update = 'chemao_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["chemao.com"]
    custom_settings = {
        "RETRY_TIMES":2
    }
    start_urls = ["http://www.chemao.com", ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 3000000
        self.size = 300000
        self.start = 1700000
        self.counts = self.start
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

    def parse(self,response):
        # self.start = 0 if self.df == 'none' else len(self.df)-1
        # self.counts = self.start
        #global carnum
        # self.size = min(self.carnum-self.counts, self.size)
        for i in range(self.counts, self.counts+self.size+1):
            url = "http://www.chemao.com/show" + str(i) + ".html"
            if not (dfcheck(self.df, str(i), self.tag)):
                yield scrapy.Request(url, callback=self.parse_car)
        # self.counts = self.counts + self.size

    #error
    # def error_parse_original(self, response):
    #     request_count = self.crawler.stats.get_value('downloader/request_count')
    #     if request_count  >= self.counts - self.size / 10 and self.counts < self.carnum:
    #         self.size =min(self.size,self.carnum-self.counts)
    #         for i in range(self.counts+1, self.counts + self.size+1):
    #             url = "http://www.chemao.com/show" + str(i) + ".html"
    #             if not (dfcheck(self.df, str(i), self.tag)):
    #                 yield scrapy.Request(url,callback=self.parse_car, errback=self.error_parse_original)
    #             if request_count >= self.counts:
    #                 self.counts = self.counts + self.size

    # get car infor
    def parse_car(self, response):
        # requests count
        if self.tag == 'update':
            addcounts = self.request_next()
            if addcounts:
                self.size = min(self.size, self.carnum - self.reqcounts)
                for i in range(self.reqcounts, self.reqcounts + self.size):
                    url = self.urllist[i]
                    if url:
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
        else:
            #counts
            # request_count = self.crawler.stats.get_value('downloader/request_count')
            # if request_count >= self.counts - self.size / 10 and self.counts < self.carnum:
            #     self.size = min(self.size, self.carnum - self.counts)
            #     for i in range(self.counts+1, self.counts + self.size+1):
            #         url = "http://www.chemao.com/show" + str(i) + ".html"
            #         if not (dfcheck(self.df, str(i), self.tag)):
            #             yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse_original)
            #         if request_count >= self.counts:
            #             self.counts = self.counts + self.size
        #key and status (sold or sale, price,time)
        # dffile
            dffile(self.fa, response.url, self.tag, urltag='num')
            status = response.xpath('//div[@class="shelf-wram"]')
            if status:
                status= "sold"
                price = ".".join(response.xpath('//span[@class="p"]/text()').re('\d+'))
            else:
                status = "sale"
                price = ".".join(response.xpath('//span[@class="s4"]/text()').re('\d+'))
            datetime = response.xpath('//span[@class="Tahoma"]/text()').extract_first()

            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [response.xpath('//html').extract_first()]
            yield item


# new
class CarSpider_new(CarSpider):
    # basesetting
    name = spidername_new

    def __init__(self, **kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum,
            urltag='num'
        )
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")


# update
class CarSpider_update(CarSpider, update):
    # basesetting
    name = spidername_update

    def __init__(self, **kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)

        # settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag = 'update'
        # do
        super(update, self).start_requests()