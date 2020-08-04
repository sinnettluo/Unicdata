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



website ='chewang'
spidername_new = 'chewang_new'
spidername_update = 'chewang_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["carking001.com"]
    start_urls = [
        "http://www.carking001.com/ershouche"
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

    #get car list
    def parse(self, response):
        for href in response.xpath('//ul[@class="carList"]/li'):
            urlbase = href.xpath("a/@href").extract_first()
            url = response.urljoin(urlbase)
            datasave1 = href.extract()
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url,meta={"datasave1":datasave1},callback= self.parse_car)
        next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.parse)
        else:
            # as list
            for id in range(1, 290000):
                urlbase = 'http://www.carking001.com/ershouche/detail/' + str(id) + '.html'
                url = response.urljoin(urlbase)
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url,meta={"datasave1":"zero"} ,callback=self.parse_car)

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
        if response.status==200 and len(response.xpath('//html').extract_first())>=20000:
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
            status = response.xpath('//a[@class="btn_3"]')
            status = "sold" if status else "sale"
            # price = response.xpath('//strong/span/text()')
            # price = str(price.extract_first()) if price else "zero"
            price = response.xpath('//div[@class="car_details_con_2017"]/span/strong/text()').re('\d+.\d+')[0] \
                if response.xpath('//div[@class="car_details_con_2017"]/span/strong/text()').re('\d+.\d+') else "zero"
            # price = re.findall("\d+.\d+",str(price.extract_first()))[0] if price else "zero"
            datetime ="zero"
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