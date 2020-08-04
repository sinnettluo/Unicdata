#-*- coding: UTF-8 -*-
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



website ='cn2che'
spidername_new = 'cn2che_new'
spidername_update = 'cn2che_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["cn2che.com"]
    start_urls = [
        "http://www.cn2che.com/serial.html",
    ]
    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=800000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    # get family list
    def parse(self, response):
        # car_item
        for href in response.xpath(u'//div[@class="msglist12"]/dl/dd/a[contains(text(),"二手车")]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_list)

    # get car list
    def parse_list(self, response):
        # car_item
        for href in response.xpath('//div[contains(@class,"cheyuan")]/ul/li'):
            urlbase = href.xpath("span/a/@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.parse_list)

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
        logging.log(msg="download              " + str(self.counts) + "                  items",
                    level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        # base infor
        # datasave
        if response.meta.has_key('datasave1'):
            datasave1 = response.meta['datasave1']
        else:
            datasave1 = 'zero'
        # key and status (sold or sale, price,time)
        status = response.xpath('//li[@id="car_state_text"]/@val')
        if status:
            if int(status.extract_first()) == 1:
                status = "sale"
            else:
                status = "sold"
        else:
            status = "sale"
        price = response.xpath('//strong[@id="price"]/text()')
        price = ".".join(price.re('\d+')) if price else "zero"
        pagetime = response.xpath('//li[@class="sendtime"]/text()')
        pagetime = "-".join(pagetime.re('\d+')) if pagetime else "zero"
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + str(price) + "-" + str(status) + "-" + pagetime
        item['pagetime'] = pagetime
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