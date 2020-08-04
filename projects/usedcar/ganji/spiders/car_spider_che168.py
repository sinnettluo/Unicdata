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



website ='che168'
spidername_new = 'che168_new'
spidername_update = 'che168_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["che168.com"]
    start_urls = [ "http://m.che168.com/carlist/FilterBrand.aspx", ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=1500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    # brand select
    def parse(self, response):
        # yield scrapy.Request("https://www.che168.com/dealer/277155/21378007.html?pvareaid=100519", callback=self.parse_car)
        for href in response.xpath('//li[@class="carbrand"]/@data-pinyin').extract():
            brand =href
            href = "http://www.che168.com/china/" + brand + "/"
            url = response.urljoin(href)
            yield scrapy.Request(url,callback=self.select1_parse)
        # yield scrapy.Request(url='http://www.che168.com/china/aodi/', callback=self.parse_family)

    # def parse_family(self, response):
    #     labels = response.xpath('//label')
    #     for label in labels:
    #         family_name = label.xpath("./input/@pinyin").extract_first()
    #         if family_name:
    #             url = response.url + family_name + "/"
    #             yield scrapy.Request(url, callback=self.select1_parse)


    # region select
    def select1_parse(self, response):
        citys = response.xpath("//*[@class='city']")
        for city in citys:
            hrefs = city.xpath('./a')
            for href in hrefs:
                url = href.xpath("./@href").extract_first()
                city_name = url.split('/')[1]
                url = response.urljoin(response.url.replace('china',city_name))
                print(url)
                yield scrapy.Request(url, callback=self.select2_parse)

        # page300 = bool(response.xpath('//div[@id="listpagination"]/a[contains(text(),"300")]'))
        # if page300:
        #     for href in response.xpath('//span[@class="capital"]/a/@href'):
        #         family = response.meta['family']
        #         url = response.urljoin(href.extract()+family+"/")
        #         print(url)
        #         yield scrapy.Request(url, self.select2_parse)
        # else:
        #     # if no page300, car select
        #     for href in response.xpath('//ul[@class="fn-clear"]/li'):
        #         urlbase = href.xpath("a/@href").extract_first()
        #         datasave1 = href.extract()
        #         url = response.urljoin(urlbase)
        #         if not (dfcheck(self.df, url, self.tag)):
        #             yield scrapy.Request(url,meta={"datasave1":datasave1}, callback=self.parse_car)
        #     # next page
        #     next_page = response.xpath('//a[@class="page-item-next"]/@href')
        #     if next_page:
        #         url_next = response.urljoin(next_page.extract_first())
        #         yield scrapy.Request(url_next, self.select1_parse)

    # car select
    def select2_parse(self, response):
        # car select
        print(response.xpath('//ul[@class="fn-clear certification-list"]/li'))
        for href in response.xpath('//ul[@class="fn-clear certification-list"]/li'):
            urlbase = href.xpath("a/@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1":datasave1}, callback=self.parse_car)
        # next page
        next_page = response.xpath('//a[@class="page-item-next"]/@href')
        print(next_page)
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.select2_parse)

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
        if response.status==200 and len(response.xpath('//html').extract_first()) >=8000:
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            #key and status (sold or sale, price,time)
            status= response.xpath('//span[@class="be-scheduled" or @class="tag tag-sale"]')
            print(status)
            if status:
                status='sold'
            else:
                status='sale'
            price = ".".join(response.xpath('//div[@class="car-price"]/ins/text()').re('\d+'))
            price = price if price else "zero"
            pagetime = "zero"
            #datasave
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-" + pagetime
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