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

website ='aokangda'
spidername_new = 'aokangda_new'
spidername_update = 'aokangda_update'

#main
class CarSpider(scrapy.Spider):
    # basesetting
    name = website
    allowed_domains = ["akd.cn"]
    start_urls=['http://www.akd.cn',]
    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 250000
        self.start = 1
        self.num = 250000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    def parse(self,response):
        for i in range(150000, 250000):
        #         print(i)
        # for i in range(self.start, self.start+self.num):
                url = "http://www.akd.cn/car/" + str(i) + "/"
                if not (dfcheck(self.df, str(i), self.tag)):
                    yield scrapy.Request(url,callback=self.parse_car)
        # yield scrapy.Request('http://www.akd.cn/car/159118/', callback=self.parse_car)

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
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag, urltag='num')
        #key and status (sold or sale, price,time)
        status = response.xpath('//a[@class="subscribe-btn"]')
        if status:
            status= "sold"
            # price = response.xpath('//p[@style="text-align: center;color: #EF4C07;font-weight:bold;margin-bottom:12px;"]/text()')
            # price = round(float(".".join(price.re('\d+')[:2]))/0.3,2)
        else:
            status = "sale"
            # price = response.xpath('//div[@class="grid-c-l car-price"]/strong/text()')
            # price = ".".join(price.re('\d+'))
        datetime = "zero"

        price =response.xpath('//*[@id="akd_content"]/div[1]/div[2]/div[2]/p[1]/span/text()').extract_first()       #item loader
        if not price:
            price = "no price"
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(status)+"-"+price
        print(item['status'])
        item['pagetime'] = datetime
        item['datasave'] = [response.xpath('//html').extract_first()]
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
                carnum=self.carnum,
                urltag='num'
        )
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