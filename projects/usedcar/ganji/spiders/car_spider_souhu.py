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
import re


website ='souhu'
spidername_new = 'souhu_new'
spidername_update = 'souhu_update'


class CarSpider(scrapy.Spider):
    #basesetting
    name = website
    allowed_domains = ["sohu.com"]
    start_urls=['http://2sc.sohu.com/buycar/pg1.shtml',]


    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=3000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'


    #price select
    def parse(self,response):
        print(123123213)
        counts=response.xpath('//div[@class="totalCarsNum"]/span/text()').re('\d+')[0]
        listok=True
        if counts:
            counts=float(counts)
            if counts>2400:
                listok=False
        if listok:
            x=response.xpath('//div[@class="carShow"]/div')
            for temp in x:
                urlbase=temp.xpath('a[@class="car-link"]/@href').extract_first()
                url=response.urljoin(urlbase)
                datasave1=temp.extract()
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            next_page=response.xpath('//span[contains(text(),">")]/../@href').extract_first()
            if next_page:
                url=response.urljoin(next_page)
                yield scrapy.Request(url, self.parse)
        else:
            price=response.xpath('//div[@class="price-sc clearfix lab_block"]/a')
            for temp in price[1:9]:
                urlbase=temp.xpath('@href').extract_first()
                url=response.urljoin(urlbase)
                yield scrapy.Request(url, self.select2_parse)
    #type select
    def select2_parse(self,response):
        print("select2")
        counts = response.xpath('//div[@class="totalCarsNum"]/span/text()').re('\d+')[0]
        listok = True
        if counts:
            counts = float(counts)
            if counts > 2400:
                listok = False
        if listok:
            x=response.xpath('//div[@class="carShow"]/div')
            for temp in x:
                urlbase=temp.xpath('a[@class="car-link"]/@href').extract_first()
                url=response.urljoin(urlbase)
                datasave1=temp.extract()
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            next_page=response.xpath('//span[contains(text(),">")]/../@href').extract_first()
            if next_page:
                url=response.urljoin(next_page)
                yield scrapy.Request(url, self.select2_parse)
        else:
            x = response.xpath('//ul[@class="clearfix"]/li')
            for temp in x:
                urlbase = temp.xpath('a/@href').extract_first()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, self.select3_parse)
    #mileage select
    def select3_parse(self,response):
        print("select3")
        counts = response.xpath('//div[@class="totalCarsNum"]/span/text()').re('\d+')[0]
        listok = True
        if counts:
            counts = float(counts)
            if counts > 2400:
                listok = False
        if listok:
            x = response.xpath('//div[@class="carShow"]/div')
            for temp in x:
                urlbase = temp.xpath('a[@class="car-link"]/@href').extract_first()
                url = response.urljoin(urlbase)
                datasave1 = temp.extract()
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            next_page = response.xpath('//span[contains(text(),">")]/../@href').extract_first()
            if next_page:
                url = response.urljoin(next_page)
                yield scrapy.Request(url, self.select3_parse)
        else:
            x = response.xpath('//ul[@class="sc-option-list"]/li')
            for temp in x:
                urlbase = temp.xpath('a/@href').extract_first()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, self.select4_parse)

    #age select
    def select4_parse(self,response):
        print("select4")
        counts = response.xpath('//div[@class="totalCarsNum"]/span/text()').re('\d+')[0]
        listok = True
        if counts:
            counts = float(counts)
            if counts > 2400:
                listok = False
        if listok:
            x = response.xpath('//div[@class="carShow"]/div')
            for temp in x:
                urlbase = temp.xpath('a[@class="car-link"]/@href').extract_first()
                url = response.urljoin(urlbase)
                datasave1 = temp.extract()
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            next_page = response.xpath('//span[contains(text(),">")]/../@href').extract_first()
            if next_page:
                url = response.urljoin(next_page)
                yield scrapy.Request(url, self.select4_parse)
        else:
            x = response.xpath('//div[@class="lab_block"][1]/a')
            for temp in x[1:6]:
                urlbase = temp.xpath('@href').extract_first()
                url=response.urljoin(urlbase)
                yield scrapy.Request(url, self.select5_parse)

    #output select
    def select5_parse(self,response):
        print("select5")
        x = response.xpath('//div[@class="carShow"]/div')
        for temp in x:
            urlbase = temp.xpath('a[@class="car-link"]/@href').extract_first()
            url = response.urljoin(urlbase)
            datasave1 = temp.extract()
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
        next_page = response.xpath('//span[contains(text(),">")]/../@href').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.select5_parse)



    def parse_car(self, response):
        print(response)
        # requests count
        if self.tag == 'update':
            addcounts = self.request_next()
            if addcounts:
                self.size = min(self.size, self.carnum - self.reqcounts)
                for i in range(self.reqcounts, self.reqcounts + self.size):
                    url = self.urllist[i]
                    if url:
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
        # base infor
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        # base infor
        datasave1 = 'zero'
        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="ask-box"]/a')
        status = "sale" if status else "sold"
        price = response.xpath('//span[@class="car-price"]/text()')
        price = ".".join(price.re('\d+')) if price else "zero"
        datetime = response.xpath('//label[@class="message"]/text()')
        datetime = "-".join(datetime.re('\d+')) if datetime else "zero"
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
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
            carnum=self.carnum)
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
# website ='souhu'
# spidername_new = 'souhu_new'
# spidername_update = 'souhu_update'
#
# #main
# class CarSpider(scrapy.Spider):
#     #basesetting
#     name = website
#     allowed_domains = ["sohu.com"]
#     start_urls=['http://2sc.sohu.com',]
#
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider, self).__init__(**kwargs)
#         #setting
#         self.tag='original'
#         self.counts=0
#         self.carnum=3000000
#         self.dbname = 'usedcar'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df='none'
#         self.fa='none'
#
#     # get car list
#     def parse(self,response):
#        for id in range(1,self.carnum):
#             url = 'http://2sc.sohu.com/buycar/carinfo_sohu_' + str(id) + '.shtml'
#             if not (dfcheck(self.df, url, self.tag)):
#                 yield scrapy.Request(url,callback=self.parse_car)
#
# #     # get car infor
#       def parse_car(self, response):
#          # requests count
#          if self.tag == 'update':
#              addcounts = self.request_next()
#              if addcounts:
#                self.size = min(self.size, self.carnum - self.reqcounts)
#                  for i in range(self.reqcounts, self.reqcounts + self.size):
#                     url = self.urllist[i]
#                     if url:
#                          yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
#          # base infor
#          # count
#          self.counts += 1
#          logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
#          # dffile
#          dffile(self.fa, response.url, self.tag)
#          # base infor
#          datasave1 = 'zero'
#          # key and status (sold or sale, price,time)
#          status = response.xpath('//label[@class="car-contact fl bg_col"]')
#          status = "sold" if status else "sale"
#          price = response.xpath('//span[@class="car-price"]/text()')
#          price = ".".join(price.re('\d+')) if price else "zero"
#          datetime = response.xpath('//label[@class="message"]/text()')
#          datetime = "-".join(datetime.re('\d+')) if datetime else "zero"
#          # item loader
#          item = GanjiItem()
#          item['url'] = response.url
#          item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#          item['website'] = website
#          item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + datetime
#          item['pagetime'] = datetime
#          item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
#          yield item
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

