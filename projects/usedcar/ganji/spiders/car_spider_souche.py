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

website ='souche'
spidername_new = 'souche_new'
spidername_update = 'souche_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["souche.com"]
    start_urls = [ "http://www.souche.com/shanghai/list", ]

    #init
    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=1000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    # region select
    def parse(self, response):
        for href in response.xpath('//a[contains(@class,"province-item")]/@data-pinyin'):
            urlbase1= "http://www.souche.com/"+href.extract()+"/list-stzaishou"
            urlbase2= "http://www.souche.com/"+href.extract()+"/list-styishou"
            url = response.urljoin(urlbase1)
            url = response.urljoin(urlbase2)
            yield scrapy.Request(url, self.select2_parse)

    # brand select, region parse
    def select2_parse(self, response):
        #数量
        counts = response.xpath('//h1[@class="historyRecord_title"]/text()').re('\d+')
        print counts
        if counts:
            counts = int(counts[0])
            if counts <= 6000:
                for href in response.xpath('//div[@class="carsItem carItem"]'):
                    urlbase = href.xpath('a/@href').extract_first()
                    datasave1 = href.extract()
                    url = response.urljoin(urlbase)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                # next page
                next_page = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_page:
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.select2_parse)
            else:
                for href in response.xpath('//dl[@class="clearfix"]/dd/a/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, self.select4_parse)

    # geartype select,brand parse
    def select4_parse(self, response):
        counts = response.xpath('//h1[@class="historyRecord_title"]/text()').re('\d+')
        if counts:
            counts = int(counts[0])
            if counts <= 6000:
                for href in response.xpath('//div[@class="carsItem carItem"]'):
                    urlbase = href.xpath('a/@href').extract_first()
                    datasave1 = href.extract()
                    url = response.urljoin(urlbase)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                # next page
                next_page = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_page:
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.select4_parse)
            else:
                for href in response.xpath(u'//dd[@click_type="sale-transmissions"]/div/ul/li/a[not(contains(text(),"不限"))]/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, self.select5_parse)

                    # output select, geartype parse
    def select5_parse(self, response):
        counts = response.xpath('//h1[@class="historyRecord_title"]/text()').re('\d+')
        if counts:
            counts = int(counts[0])
            if counts <= 6000:
                for href in response.xpath('//div[@class="carsItem carItem"]'):
                    urlbase = href.xpath('a/@href').extract_first()
                    datasave1 = href.extract()
                    url = response.urljoin(urlbase)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                # next page
                next_page = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_page:
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.select5_parse)
            else:
                for href in response.xpath(u'//dd[@click_type="sale-engines"]/div/ul/li/a[not(contains(text(),"不限"))]/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, self.select6_parse)

    # emission select,output parse
    def select6_parse(self, response):
        counts = response.xpath('//h1[@class="historyRecord_title"]/text()').re('\d+')
        if counts:
            counts = int(counts[0])
            if counts <= 6000:
                for href in response.xpath('//div[@class="carsItem carItem"]'):
                    urlbase = href.xpath('a/@href').extract_first()
                    datasave1 = href.extract()
                    url = response.urljoin(urlbase)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                # next page
                next_page = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_page:
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.select6_parse)
            else:
                for href in response.xpath(
                        u'//dd[@click_type="sale-standard"]/div/ul/li/a[not(contains(text(),"不限"))]/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, self.select7_parse)

                    # country select,emission parse
    def select7_parse(self, response):
        counts = response.xpath('//h1[@class="historyRecord_title"]/text()').re('\d+')
        if counts:
            counts = int(counts[0])
            if counts <= 6000:
                for href in response.xpath('//div[@class="carsItem carItem"]'):
                    urlbase = href.xpath('a/@href').extract_first()
                    datasave1 = href.extract()
                    url = response.urljoin(urlbase)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                # next page
                next_page = response.xpath('//a[@class="next"]/@href').extract_first()
                if next_page:
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.select7_parse)
            else:
                for href in response.xpath(u'//dd[@click_type="sale-country"]/div/ul/li/a[not(contains(text(),"不限"))]/@href'):
                    url = response.urljoin(href.extract())
                    yield scrapy.Request(url, self.select8_parse)

    # country parse
    def select8_parse(self, response):
        for href in response.xpath('//div[@class="carsItem carItem"]'):
            urlbase = href.xpath('a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
        # next page
        next_page = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.select8_parse)


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

        if response.status == 200:
            # base infor
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            # datasave
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'
            #key and status (sold or sale, price,time)
            status = response.xpath('//ins[@class="detail-no hook-work-off"]')
            if status:
                status= "sold"
            else:
                status = "sale"
            price = ".".join(response.xpath('//div[@class="detail_price_left clearfix"]/em/text()').re('\d+'))
            price = price if price else "zero"
            pagetime = response.xpath('//div[@class="push-time"]/text()').extract_first()
            pagetime = pagetime[:-2] if pagetime else "zero"
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-" + md5(pagetime.encode("utf-8")).hexdigest()
            item['pagetime'] = pagetime
            item['datasave'] = [datasave1 ,response.xpath('//html').extract_first()]
            yield item
#
#  new
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