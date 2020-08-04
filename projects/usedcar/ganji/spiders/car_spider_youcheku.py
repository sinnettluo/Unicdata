#-*- coding: UTF-8 -*-
import logging
import scrapy
import time
from hashlib import md5
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ganji.redial import Redial
from Car_spider_update import update
from SpiderInit import dfcheck
from SpiderInit import dffile
from SpiderInit import spider_new_Init
from SpiderInit import spider_original_Init
from SpiderInit import spider_update_Init
from ganji.items import GanjiItem

website ='youcheku'
spidername_new = 'youcheku_new'
spidername_update = 'youcheku_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    # allowed_domains = ["used.xcar.com.cn"]
    # start_urls=('http://used.xcar.com.cn',)
    start_urls = ['http://www.youcku.com/Mobile/Wholesale/index']

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=2000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'
        self.headers = {
            'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Host':'used.xcar.com.cn',
            'Upgrade-Insecure-Requests':'1',
        }
        # rd = Redial()
        # rd.connect()

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, cookies={'_Xdwuv': '5046671120584'}, headers=self.headers, dont_filter=True)


    # def parse(self,response):
    #     for i in range(1, 34):
    #         for j in range(1, 3):
    #             url = "http://used.xcar.com.cn/search/" + str(i) + "-0-0-0-0-0-0-0-0-0-0-0-0-0-0-"+ str(j) +"-0/"
    #             yield scrapy.Request(url,callback=self.parse_list, cookies={'_Xdwuv': '5046671120584'})

    #get car list
    # def parse_list(self, response):
    #     #car_item
    #     for href in response.xpath('//li[@class="li_hover"]'):
    #         #small data
    #         datasave1 = href.extract()
    #         # urlbase
    #         urlbase = href.xpath("a/@href").extract_first()
    #         url = response.urljoin(urlbase)
    #         if not (dfcheck(self.df, url, self.tag)):
    #             yield scrapy.Request(url,  meta={'datasave1': datasave1}, callback=self.parse_car, cookies={'_Xdwuv': '5046671120584'})
    #     # next page
    #     next_page = response.xpath('//a[@class="page_down"]/@href').extract_first()
    #     if next_page:
    #         url_next = response.urljoin(next_page)
    #         yield scrapy.Request(url_next, self.parse_list, cookies={'_Xdwuv': '5046671120584'})


    def parse(self, response):
        pass


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