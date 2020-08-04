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
from scrapy.conf import settings
import random

website='baixing'
spidername_new='baixing_new'
spidername_update='baixing_update'

class CarSpider(scrapy.Spider):
    #basesetting
    name=website
    allowed_domains=["baixing.com"]
    start_urls=["http://china.baixing.com/ershouqiche/"]
    # settings.set('DOWNLOAD_DELAY', 1, priority='cmdline')

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=5000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    # region select
    def parse(self,response):
        x=response.xpath('//div[@class="area links"]/a')
        for temp in x[1:31]:
            url=str(temp.xpath('@href').extract_first())
            yield scrapy.Request(url,self.select2_parse)

    # price select,region parse
    def select2_parse(self,response):
        page100=bool(response.xpath('//ul[@class="list-pagination"]/li/a[contains(text(),"100")]'))
        if page100:
            x=response.xpath(u'//span[contains(text(),"价格")]/../div/a')
            for temp in x[1:6]:
                href=temp.xpath('@href').extract_first()
                url=response.urljoin(href)
                yield scrapy.Request(url,self.select3_parse)
        else:
            x=response.xpath('//ul[@class="list-ad-items"]/li')
            for temp in x:
                datasave1=temp.extract()
                url = str(temp.xpath('a/@href').extract_first())
                if not (dfcheck(self.df,url,self.tag)):
                    yield scrapy.Request(url, meta={"datasave1":datasave1},callback=self.parse_car)
            next_page=response.xpath(u'//a[contains(text(),"下一页")]/@href')
            if next_page:
                url=response.urljoin(next_page.extract_first())
                yield scrapy.Request(url,self.select2_parse)



    # price parse level select
    def select3_parse(self,response):
        page100 = bool(response.xpath('//ul[@class="list-pagination"]/li/a[contains(text(),"100")]'))
        if page100:
            x=response.xpath(u'//span[contains(text(),"车级别")]/../div/a')
            for temp in x[1:8]:
                url=response.urljoin(temp.xpath('@href').extract_first())
                yield scrapy.Request(url,self.select4_parse)
        else:
            x=response.xpath('//ul[@class="list-ad-items"]/li')
            for temp in x:
                datasave1 = temp.extract()
                url = str(temp.xpath('a/@href').extract_first())
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select3_parse)

    # level parse
    def select4_parse(self,response):
        x=response.xpath('//ul[@class="list-ad-items"]/li')
        for temp in x:
            datasave1 = temp.extract()
            url = str(temp.xpath('a/@href').extract_first())
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.select4_parse)


    def parse_car(self, response):
        # requests count
        if self.tag == 'update':
            addcounts = self.request_next()
            if addcounts:
                self.size=min(self.size, self.carnum - self.reqcounts)
                for i in range(self.reqcounts, self.reqcounts + self.size):
                    url = self.urllist[i]
                    if url:
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
        #count
        self.counts += 1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        # base infor
        if response.meta.has_key('datasave1'):
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'
        # key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="viewad-content out-of-time"]')
        status = "sold" if status else "sale"
        if status == "sold":
            price = "zero"
        else:
            price = response.xpath('//span[@class="price"]/text()').re('\d+\.\d+')[0] \
                if response.xpath('//span[@class="price"]/text()').re('\d+\.\d+') else "zero"
        datetime = response.xpath('//span[@data-toggle="tooltip"]/text()')
        datetime = datetime.extract_first() if datetime else "zero"
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + str(datetime)
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

