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
from ganji.redial import Redial

website ='kaixin'
spidername_new = 'kaixin_new'
spidername_update = 'kaixin_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["kx.cn"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'
        self.wrong=0

        rd = Redial()
        rd.connect()

    def start_requests(self):
        cars=[]
        for i in range(40000, self.carnum):
            urlbase = 'http://www.kx.cn/chejia/' + str(i)
            if not (dfcheck(self.df, urlbase, self.tag)):
                car = scrapy.Request(urlbase, meta={'datasave1': 'zero'})
                cars.append(car)
        return cars

    # get car infor
    def parse(self, response):
        if self.wrong <=10000:
            if response.status==200 and response.xpath('//span[@class="date"]/text()') and not(response.xpath(u'//div[contains(text(),"非常抱歉")]/text()')):
                self.wrong=0
                #base infor
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
                #key and status (sold or sale, price,time)
                status = "sold"
                price = response.xpath('//span[@class="l"]/b/text()')
                price = price.extract_first() if price else "zero"
                datetime =response.xpath('//span[@class="date"]/text()')
                datetime = datetime.extract_first() if datetime else "zero"
                #item loader
                item = GanjiItem()
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['website'] = website
                item['status'] = response.url
                item['pagetime'] = datetime
                item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
                yield item
            else:
                self.wrong = self.wrong + 1
                logging.log(msg= response.url+':wrong'+str(response.status)+'-'+str(len(response.xpath('//html').extract_first()))\
                      +"-"+response.xpath(u'//div[contains(text(),"非常抱歉")]/text()').extract_first(),level=logging.INFO)

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