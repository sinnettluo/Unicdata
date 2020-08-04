#-*- coding: UTF-8 -*-
from scrapy.spiders import SitemapSpider
import scrapy
from ganji.items import GanjiItem
from scrapy.conf import settings
import time
import logging
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update

website ='guazi'
spidername_new = 'guazimap_new'
spidername_update = 'guazimap_update'
carnum = 300000
#main
class CarSpider(SitemapSpider):
    #basesetting
    name = website+'map'
    allowed_domains = ["guazi.com"]
    sitemap_urls = ['http://seo.guazi.com/baidu/urlindex.xml']
    sitemap_follow = ['/seo.guazi.com']
    sitemap_rules = [
        ('/www.guazi.com/', 'parse_car'),
    ]
    settings.set('CrawlCar_Num', carnum, priority='cmdline')
    settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
    settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 300000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

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
        #status check
        if response.status==200 and not(dfcheck(self.df, response.url, self.tag)):
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            #base infor
            datasave1 = "zero"
            #key and status (sold or sale, price,time)
            status = response.xpath('//a[@class="stipul-btn stipul-btn-gray"]')
            status = "sold" if status else "sale"
            price = response.xpath('//b[@class="f30 numtype"]/text()')
            price = price.extract_first()[1:] if price else "zero"
            datetime ="zero"
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+str(datetime)
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