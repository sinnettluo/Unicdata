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
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
import re

website ='auto51'
spidername_new = 'auto51_new'
spidername_update = 'auto51_update'


class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["51auto.com"]
    start_urls =["http://m.51auto.com/quanguo/pabmdcigf"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 1000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        self.browser.set_page_load_timeout(10)
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self,response):
        # print(response.body)
        # x=response.xpath('//div[@class="vehicle-section"]/a')
        x  = response.xpath('//div[@class="carlist"]/a')
        print(x)
        # for temp in x:
        #     url = temp.xpath('@href').extract_first()
        #     yield scrapy.Request(url,callback=self.parse_car)
        if x != []:
            count = response.xpath("//div[@class='pagination_box']/div/div/span/text()").extract_first()
            count = int(re.findall("^1\/(.*?)$", count)[0])
            print(count)
            for i in range(count):
                pageNum = i + 1
                yield scrapy.Request("http://m.51auto.com/quanguo/pabmdcigf?page=%d" % pageNum, callback=self.parse_list)
        # next_page=response.xpath('//div[@class="pagination"]/a[@class="page-down"]/@href').extract_first()
        # if next_page:
        #     yield scrapy.Request(next_page,self.parse)


    def parse_list(self, response):
        x = response.xpath('//div[@class="carlist"]/a')
        print(x)
        for temp in x:
            url = temp.xpath('@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_car)


    def parse_car(self,response):
        if self.tag == 'update':
            addcounts = self.request_next()
            if addcounts:
                self.size = min(self.size, self.carnum - self.reqcounts)
                for i in range(self.reqcounts, self.reqcounts + self.size):
                    url = self.urllist[i]
                    if url:
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag, urltag='num')
        #key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="p-rel nocar-text"]')
        if status:
            status= "sold"
            price = response.xpath('//p[@style="text-align: center;color: #EF4C07;font-weight:bold;margin-bottom:12px;"]/text()')
            price = round(float(".".join(price.re('\d+')[:2]))/0.3,2)
        else:
            status = "sale"
            price = response.xpath('//div[@class="grid-c-l car-price"]/strong/text()')
            price = ".".join(price.re('\d+'))
        datetime = "zero"

        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]
        yield item



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























# #-*- coding: UTF-8 -*-
# import scrapy
# from ganji.items import GanjiItem
# import time
# import logging
# from hashlib import md5
# from SpiderInit import spider_original_Init
# from SpiderInit import spider_new_Init
# from SpiderInit import spider_update_Init
# from SpiderInit import dfcheck
# from SpiderInit import dffile
# from Car_spider_update import update
#
#
# website ='auto51'
# spidername_new = 'auto51_new'
# spidername_update = 'auto51_update'
#
# #main
# class CarSpider(scrapy.Spider):
#     # basesetting
#     name = website
#     allowed_domains = ["51auto.com"]
#     start_urls =["http://m.51auto.com",]
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider, self).__init__(**kwargs)
#         # setting
#         self.tag = 'original'
#         self.counts = 0
#         self.carnum = 3900000
#         self.size = 100000
#         self.start = 0
#         self.counts = self.start
#         self.dbname = 'usedcar'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df = 'none'
#         self.fa = 'none'
#
#     def parse(self,response):
#         self.start =0 if self.df=='none' else len(self.df)
#         self.counts = self.start
#         if self.counts +self.size+1 < self.carnum:
#             for i in range(self.counts+1,self.counts+self.size+1):
#                 url='http://m.51auto.com/buycar/'+ str(i)+'.html'
#                 if not (dfcheck(self.df, str(i), self.tag)):
#                     yield scrapy.Request(url,callback=self.parse_car,errback=self.error_parse_original)
#             self.counts= self.counts +self.size
#         else:
#             for i in range(self.counts+1,self.carnum+1):
#                 url='http://m.51auto.com/buycar/'+ str(i)+'.html'
#                 if not (dfcheck(self.df, str(i), self.tag)):
#                     yield scrapy.Request(url,callback=self.parse_car,errback=self.error_parse_original)
#             self.counts= self.carnum
#
#     # get car infor
#     def error_parse_original(self, response):
#         request_count = self.crawler.stats.get_value('downloader/request_count')
#         print str(request_count) +"-error"
#         if request_count + self.start >= self.counts - self.size/2 and self.counts < self.carnum:
#             if self.counts + self.size + 1 < self.carnum:
#                 for i in range(self.counts + 1, self.counts + self.size + 1):
#                     url = 'http://m.51auto.com/buycar/' + str(i) + '.html'
#                     if not (dfcheck(self.df, str(i), self.tag)):
#                         yield scrapy.Request(url,
#                                              callback=self.parse_car,errback=self.error_parse_original)
#                 if request_count + self.start >= self.counts:
#                     self.counts = self.counts + self.size
#             else:
#                 for i in range(self.counts + 1, self.carnum + 1):
#                     url = 'http://m.51auto.com/buycar/' + str(i) + '.html'
#                     if not (dfcheck(self.df, str(i), self.tag)):
#                         yield scrapy.Request(url,
#                                              callback=self.parse_car,errback=self.error_parse_original)
#                 if request_count + self.start >= self.counts:
#                     self.counts = self.carnum
#     # get car infor
#     def parse_car(self, response):
#         # requests count
#         if self.tag == 'update':
#             addcounts = self.request_next()
#             if addcounts:
#                 self.size = min(self.size, self.carnum - self.reqcounts)
#                 for i in range(self.reqcounts, self.reqcounts + self.size):
#                     url = self.urllist[i]
#                     if url:
#                         yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
#         else:
#             request_count = self.crawler.stats.get_value('downloader/request_count')
#             if request_count+ self.start>= self.counts-self.size/2 and self.counts < self.carnum:
#                 if self.counts + self.size + 1 < self.carnum:
#                     for i in range(self.counts + 1, self.counts + self.size + 1):
#                         url = 'http://m.51auto.com/buycar/' + str(i) + '.html'
#                         yield scrapy.Request(url, callback=self.parse_car,errback=self.error_parse_original)
#                     if request_count+ self.start>= self.counts:
#                         self.counts = self.counts + self.size
#                 else:
#                     for i in range(self.counts + 1, self.carnum + 1):
#                         url = 'http://m.51auto.com/buycar/' + str(i) + '.html'
#                         yield scrapy.Request(url, callback=self.parse_car,errback=self.error_parse_original)
#                     if request_count + self.start >= self.counts:
#                         self.counts = self.carnum
#         if len(response.xpath('//html').extract_first())>=2000:
#             # dffile
#             dffile(self.fa, response.url, self.tag,urltag='num')
#             # base infor
#             datasave1 = "zero"
#             # key and status (sold or sale, price,time)
#             status = response.xpath('//div[@class="p-rel nocar-text"]')
#             status = "sold" if status else "sale"
#             price = '.'.join(response.xpath('//span[@class="price"]/text()').re('\\d+'))
#             price = price if price else "zero"
#             datetime =  "zero"
#             # item loader
#             item = GanjiItem()
#             item['url'] = response.url
#             item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#             item['website'] = website
#             item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
#             item['pagetime'] = datetime
#             item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
#             yield item
#
# #new
# class CarSpider_new(CarSpider):
#
#     #basesetting
#     name = spidername_new
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider_new, self).__init__(**kwargs)
#         #tag
#         self.tag='new'
#         # spider setting
#         self.df =spider_new_Init(
#                 spidername=spidername_new,
#                 dbname=self.dbname,
#                 website=website,
#                 carnum=self.carnum,
#                 urltag='num'
#         )
#         filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
#         self.fa = open(filename, "a")
#
# #update
# class CarSpider_update(CarSpider,update):
#
#     #basesetting
#     name = spidername_update
#
#     def __init__(self, **kwargs):
#         # load
#         super(CarSpider_update, self).__init__(**kwargs)
#         #settings
#         self.urllist = spider_update_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum
#         )
#         self.carnum = len(self.urllist)
#         self.tag='update'
#         #do
#         super(update, self).start_requests()
