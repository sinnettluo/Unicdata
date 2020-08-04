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
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings

website ='renrenche_sold'
spidername_new = 'renrenche_new'
spidername_update = 'renrenche_update'
antispamWallToken = ''
#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["renrenche.com"]
    start_urls = [
        "https://www.renrenche.com/sh/ershouche"
    ]

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
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        self.cookies_for_request = {}
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        self.browser.set_page_load_timeout(30)
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies_for_request, headers=self.headers, dont_filter=True)

    # region select
    def parse(self, response):
        print(response.body)
        for href in response.xpath('//a[@class="province-item "]/@href'):
            url = response.urljoin(href.extract() + "/ershouche?sort=publish_time&seq=desc")
            print(url)
            yield scrapy.Request(url, cookies=self.cookies_for_request, headers=self.headers, callback=self.list_parse)

    # get car list
    def list_parse(self, response):
        print(response)
        for href in response.xpath('//li[@class="span6 list-item car-item"]'):
            datasave1= href.extract()
            urlbase = href.xpath('a/@href').extract_first()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, cookies=self.cookies_for_request, headers=self.headers, meta={'datasave1': datasave1}, callback=self.parse_car)
        next_page = response.xpath('//a[@rrc-event-name="switchright"]/@href').extract_first()
        if not(next_page):
            time.sleep(0.5)
            try:
                page = int(response.xpath('//li[@class="active"]/a[@href="javascript:void(0);"]/text()').extract_first())+1
            except Exception as e:
                print(e)
                yield scrapy.Request(url=response.url, dont_filter=True)
                return
            location=response.url.find("ershouche")+9
            newpage = response.url[0:location]+"/p"+str(page)
            print newpage
            url = response.urljoin(newpage)
        else:
            url = response.urljoin(next_page)
        yield scrapy.Request(url, self.list_parse, cookies=self.cookies_for_request, headers=self.headers)

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
                        yield scrapy.Request(url, cookies=self.cookies_for_request, headers=self.headers, callback=self.parse_car, errback=self.error_parse)

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
            if response.xpath("//*[@id='sold_button']"):
                status = "sold"
            else:
                status = "sale"
            price = response.xpath('//span[@class="price"]/text()').extract_first()
            datetime =time.strftime('%Y-%m-%d %X', time.localtime())
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)
            item['pagetime'] = datetime
            item['sold_date'] = status
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            if status == "sold":
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