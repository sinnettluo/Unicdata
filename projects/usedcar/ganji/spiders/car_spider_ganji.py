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


# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

website ='ganji'
spidername_new = 'ganji_new'
spidername_update = 'ganji_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["ganji.com"]
    start_urls = [
        "http://www.ganji.com/index.htm",]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 50000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

    # region select
    def parse(self, response):
        if response.xpath('//div[@class="all-city"]/dl/dd/a/@href'):
            for href in response.xpath('//div[@class="all-city"]/dl/dd/a/@href'):
                url = response.urljoin(href.extract() + "ershouche/")
                yield scrapy.Request(url, self.select2_parse)
        else:
            yield scrapy.Request(url="http://www.ganji.com/index.htm", dont_filter=True)

    # more brand select, region parse
    def select2_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        if not (dfcheck(self.df, url, self.tag)):
                            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select2_parse)
                else:
                    for href in response.xpath('//a[@class="more songti"]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select3_parse)

    # brand select
    def select3_parse(self, response):
            for href in response.xpath('//p[@class="mt5"]/span[@class="hb-genre"]/a[1]/@href'):
                urlbase = href.extract()
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, self.select4_parse)

    # price select,brand parse
    def select4_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        if not (dfcheck(self.df, url, self.tag)):
                            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select4_parse)
                else:
                    for href in response.xpath('//dd[@class="ddmyprice"]/a[not(@class="cur")]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select5_parse)

    # mileage select, price parse
    def select5_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select5_parse)
                else:
                    for href in response.xpath(u'//dl/dt[contains(text(),"\u91cc\u7a0b:")]/../dd/a[not(@class="cur")]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select6_parse)

    # output select,mileage parse
    def select6_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        if not (dfcheck(self.df, url, self.tag)):
                            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select6_parse)
                else:
                    for href in response.xpath(u'//dl/dt[contains(text(),"\u6392\u91cf:")]/../dd/a[not(@class="cur")]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select7_parse)

    # geartype select,output parse
    def select7_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        if not (dfcheck(self.df, url, self.tag)):
                            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select7_parse)
                else:
                    for href in response.xpath(u'//dl/dt[contains(text(),"\u53d8\u901f\u7bb1:")]/../dd/a[not(@class="cur")]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select8_parse)

    # emission select,geartype parse
    def select8_parse(self, response):
            counts = response.xpath('//strong[@class="fc-org"]/text()').extract_first()
            if counts:
                counts = float(counts[0:-1])
                if counts <= 3000:
                    for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                        urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                        datasave1 = href.extract()
                        url = response.urljoin(urlbase)
                        if not (dfcheck(self.df, url, self.tag)):
                            yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
                    # next page
                    next_page = response.xpath('//a[@class="next"]/@href')
                    if next_page:
                        url = response.urljoin(next_page.extract_first())
                        yield scrapy.Request(url, self.select8_parse)
                else:
                    for href in response.xpath(u'//dl/dt[contains(text(),"\u6392\u653e\u6807\u51c6:")]/../dd/a[not(@class="cur")]/@href'):
                        url = response.urljoin(href.extract())
                        yield scrapy.Request(url, self.select9_parse)

    # emission parse
    def select9_parse(self, response):
            for href in response.xpath('//dl[contains(@class,"list-pic clearfix cursor_pointer")]'):
                urlbase = href.xpath('dt/div[2]/div/a/@href').extract_first()
                datasave1 = href.extract()
                url = response.urljoin(urlbase)
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select9_parse)

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

        if response.status == 200 and response.url.find('confirm.php') == -1:
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            #base infor
            # datasave
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'
            #key and status (sold or sale, price,time)
            status = "sale"
            price = response.xpath('//i[@class="arial fc-org f20"]/text()')
            price = str(price.extract_first()) if price else "zero"
            datetime =response.xpath('//i[@class="f10 pr-5"]/text()')
            datetime = str(datetime.extract_first()) if datetime else "zero"
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