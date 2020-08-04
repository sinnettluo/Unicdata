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

website ='youxinpaicheck'
spidername_new = 'youxinpaicheck_new'
spidername_update = 'youxinpaicheck_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["youxinpaicheck"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting-
        self.tag='original'
        self.counts=0
        self.carnum=2000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website='youxinpai',
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.df='none'
        self.fa='none'


    # car list parse
    def parse(self):
        for i in range(1220000,1,-1):
            url ="http://i.youxinpaicheck.com/auctionhall/Detailforop.aspx?id="+str(i)
            yield scrapy.Request(url,callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        #count
        self.counts +=1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        #base infor
        datasave1 = "zero"
        #key and status (sold or sale, price,time)
        status = "sold"
        price =  "zero"
        datetime =response.xpath('//div[@class="bidding_title"]/p/strong/text()')
        datetime ="-".join(datetime.re('\d+')) if datetime else "zero"
        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
        item['pagetime'] = datetime
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
                carnum=self.carnum,
                urltag='url',
                keycol='status')
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