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

website ='ttpai'
spidername_new = 'ttpai_new'
spidername_update = 'ttpai_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["ttpai.cn"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=600000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    def start_requests(self):
        pages = []
        for i in range(1, 20000):
                url = 'http://www.ttpai.cn/quanguo/list-p' + str(i)
                page = scrapy.Request(url)
                pages.append(page)
        return pages

    #get car list
    def parse(self, response):
        datacheck = len(response.xpath("//html").extract_first())
        if datacheck > 20000:
            # as list
            for href in response.xpath('//li[@class="item"]'):
                urlbase = href.xpath("a/@href").extract_first()
                datasave1 = href.extract()
                url = response.urljoin(urlbase)
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)

    # get car infor
    def parse_car(self, response):
        if response.status==200:
            #base infor
            # count
            self.counts += 1
            #logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            # datasave
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'
            #key and status (sold or sale, price,time)
            status = "sold"
            price = response.xpath('//strong[@class="s-orange"]/text()')
            price = ".".join(price.re('\d+')) if price else "zero"
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