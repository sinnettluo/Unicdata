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



website ='che101'
spidername_new = 'che101_new'
spidername_update = 'che101_update'

#main
class CarSpider(scrapy.Spider):
    #basesetting
    name = website
    allowed_domains = ["che101.com"]
    start_urls = [
        "http://www.che101.com/buycar/",
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

    # get car list
    def parse(self, response):

        # next page
        next_page = response.xpath('//a[@class="next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.parse, priority=1)

        # car_item
        for href in response.xpath('//ul[@class="carList_286 cf"]/li'):
            urlbase=href.xpath('a/@href').extract_first()
            pagetime= href.xpath('a/span[@class="lastest"]/text()').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url,meta={'datasave1':datasave1,
                                               'pagetime':pagetime},
                                                callback= self.parse_car)


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
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse_original)
        # count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        # base infor
        if response.meta.has_key('datasave1'):
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'
        if response.meta.has_key('pagetime'):
            pagetime = response.meta['pagetime']
        else:
            pagetime = 'zero'
        # key and status (sold or sale, price,time)
        status = "sale"
        price = response.xpath('//span[@id="total_price"]/text()')
        price = str(price.extract_first()) if price else "zero"
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + md5(pagetime.encode("utf-8")).hexdigest()
        item['pagetime'] = pagetime
        item['datasave'] = [datasave1,response.xpath('//html').extract_first()]
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