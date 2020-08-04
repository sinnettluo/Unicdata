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
# website ='hx2car'
# spidername_new = 'hx2car_new'
# spidername_update = 'hx2car_update'
#
# #main
# class CarSpider(scrapy.Spider):
#     #basesetting
#     name = website
#     allowed_domains = ["hx2car.com"]
#     start_urls = [
#         "http://www.hx2car.com/car/daquan.htm"
#     ]
#
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider, self).__init__(**kwargs)
#         #setting
#         self.tag='original'
#         self.counts=0
#         self.carnum=300000
#         self.dbname = 'usedcar'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df='none'
#         self.fa='none'
#
#     # get family list
#     def parse(self, response):
#         # car_item
#         for href in response.xpath('//p[@class="brand"]/a/@href'):
#             url = response.urljoin(href.extract())
#             yield scrapy.Request(url, callback=self.parse_list)
#
#
#     # get car list
#     def parse_list(self, response):
#         # car_item
#         for href in response.xpath('//div[@class="Datu_cars"]/div'):
#             urlbase = href.xpath('div/a/@href').extract_first()
#             datasave1 = href.extract()
#             url = response.urljoin(urlbase)
#             if not (dfcheck(self.df, url, self.tag)):
#                 yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)
#             # next page
#             next_page = response.xpath('//a[@class="num"]/@href').extract_first()
#             if next_page:
#                 url = response.urljoin(next_page)
#                 yield scrapy.Request(url, self.parse_list)
#
#
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
#         # base infor
#         # count
#         self.counts += 1
#         logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
#         # dffile
#         dffile(self.fa, response.url, self.tag)
#         # datasave
#         if response.meta.has_key('datasave1'):
#             datasave1 = response.meta['datasave1']
#         else:
#             datasave1 = 'zero'
#         # key and status (sold or sale, price,time)
#         status = response.xpath(u'//span[@class="num" and contains(text(),"过期")]')
#         status = "sold" if status else "sale"
#         price = response.xpath('//div[@class="price"]/span/text()')
#         price = ".".join(price.re('\d+')) if price else "zero"
#         pagetime = response.xpath('//div[@class="title_infoL"]/span/i/text()')
#         pagetime = pagetime.extract_first() if pagetime else "zero"
#         # item loader
#         item = GanjiItem()
#         item['url'] = response.url
#         item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#         item['website'] = website
#         item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + pagetime
#         item['pagetime'] = pagetime
#         item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
#         yield item
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
#                 carnum=self.carnum)
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
import MySQLdb

website ='hx2car'
spidername_new = 'hx2car_new'
spidername_update = 'hx2car_update'

#main
class CarSpider(scrapy.Spider):
    #basesetting
    name = website
    allowed_domains = ["hx2car.com"]
    start_urls = [
        "http://www.hx2car.com/car/daquan.htm"
    ]


    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=300000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    # get family list
    def parse(self, response):
        # yield scrapy.Request("http://www.hx2car.com/details/155826958", callback=self.parse_car)
        for href in response.xpath('//p[@class="brand"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_list)

    # def parse(self, response):
    #     mysqlconnection = MySQLdb.connect('192.168.1.94', 'root', 'Datauser@2017', 'dazhong_zb', port=3306)
    #     dbc = mysqlconnection.cursor()
    #     dbc.execute(
    #         'SELECT carid FROM hx2car_outlier')
    #     result = dbc.fetchall()
    #     for each in result:
    #         yield scrapy.Request(url="http://www.hx2car.com/details/%s" % each[0], callback=self.parse_car, dont_filter=True)
    #     mysqlconnection.close()

    # get car list
    def parse_list(self, response):
        # car_item
        for href in response.xpath('//div[@class="Datu_cars"]/div'):
            urlbase = href.xpath('div/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)
            # next page
            next_page = response.xpath('//a[@class="num"]/@href').extract_first()
            if next_page:
                url = response.urljoin(next_page)
                yield scrapy.Request(url, self.parse_list)


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
        # base infor
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        # datasave
        if response.meta.has_key('datasave1'):
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'
        # key and status (sold or sale, price,time)
        status = response.xpath(u'//span[@class="num" and contains(text(),"过期")]')  #xpath不能解析
        status = "sold" if status else "sale"
        # price = response.xpath('//div[@class="price"]/span/text()')
        price = response.xpath('//span[@class="cf60 price"]/span/text()')
        price = ".".join(price.re('\d+')) if price else "zero"
        # pagetime = response.xpath('//div[@class="title_infoL"]/span/i/text()')
        pagetime = response.xpath('//div[@class="title_infoL"]/span[1]/i[2]/text()')
        pagetime = pagetime.extract_first() if pagetime else "zero"
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + pagetime
        item['pagetime'] = pagetime
        item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
        yield item

#new
class CarSpider_new(CarSpider):

    #basesetting
    name = spidername_new

    def __init__(self, **kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        #tag
        self.tag='new'
        # spider setting
        self.df =spider_new_Init(
                spidername=spidername_new,
                dbname=self.dbname,
                website=website,
                carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self, **kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        #do
        super(update, self).start_requests()