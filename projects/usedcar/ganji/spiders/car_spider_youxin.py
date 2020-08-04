# #-*- coding: UTF-8 -*-
# import scrapy
# from scrapy.spiders import SitemapSpider
# from ganji.items import GanjiItem
# import time
# import logging
# from hashlib import md5
# from SpiderInit import spider_original_Init
# from SpiderInit import spider_new_Init
# from SpiderInit import spider_update_Init
# from SpiderInit import dfcheck
# from SpiderInit import dffile
# from Car_spider_update import update
# from scrapy.conf import settings
# import re
#
#
#
# website ='youxin'
# spidername_new = 'youxin_new'
# spidername_update = 'youxin_update'
# carnum=20000000
#
# #main
# class CarSpider(scrapy.Spider):
#     #basesetting
#     name = website
#     allowed_domains = ["xin.com"]
#     #sitemap_urls = ['http://www.xin.com/sitemap/sitemapIndex_02.xml']
#     #sitemap_follow = ['http://www.xin.com/sitemap/day_car_detail_']
#     #sitemap_rules = [
#         #('www.xin.com/sitemap/day_car_detail_', 'parse_list'),
#     #]
#     start_urls=['https://www.xin.com/quanguo/',]
#
#     settings.set('CrawlCar_Num', carnum, priority='cmdline')
#     settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
#     settings.set('MONGODB_COLLECTION', website, priority='cmdline')
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider, self).__init__(**kwargs)
#         #setting
#         self.tag='original'
#         self.counts=0
#         self.carnum=15000000
#         self.dbname = 'usedcar'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df='none'
#         self.fa='none'
#
#     #brand select
#     def parse(self,response):
#         print response.url
#         Alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
#         for i in Alphabet:
#             strtemp = '//dt[contains(text(),"' + i + '")]/../dd/a/@href'
#             for href in response.xpath(strtemp):
#                 urlbase=str(href.extract())
#                 url="https://www.xin.com"+urlbase
#                 yield scrapy.Request(url, callback=self.select2_parse)
        #for href in response.xpath('//loc/text()'):
            #url= href.extract()
            #if not (dfcheck(self.df, url, self.tag)):
                #yield scrapy.Request(url,callback=self.parse_car)
#
#
#
#
#     #price select brand parse
#     def select2_parse(self,response):
#         counts=response.xpath('//a[@name="view_v"]/h4/text()').re('\d+')[0] \
#             if response.xpath('//a[@name="view_v"]/h4/text()').re('\d+') else "0"
#         if counts:
#             counts=float(counts)
#             if counts<=4000:
#                 temp=response.xpath('//li[@class="con caritem"]')
#                 for x in temp:
#                     print x
#                     datasave1=x.extract()
#                     urlbase=str(x.xpath('//a[@class="aimg"]/@href').extract_first())
#                     #print urlbase
#                     #print len(urlbase)
#                     url="http://www.xin.com"+urlbase
#                     # print url
#                     # print type(url)
#                     if not (dfcheck(self.df,url,self.tag)):
#                         yield scrapy.Request(url,meta={"datasave1":datasave1},callback=self.parse_car)
#                 next_page= response.xpath(u'//a[contains(text(),"下一页")]/@href')
#                 if next_page:
#                     urlbase=str(next_page.extract()[0])
#                     url="http://www.xin.com"+urlbase
#                     yield scrapy.Request(url,self.select2_parse)
#             else:
#                 for href in response.xpath('//div[@class="select-con"][3]/dl/dd/a/@href'):
#                     urlbase=str(href.extract())
#                     url="http://www.xin.com"+urlbase
#                     yield scrapy.Request(url,self.select3_parse)
#
#
#     #price parse output select
#     def select3_parse(self,response):
#         counts = response.xpath('//a[@name="view_v"]/h4/text()').re('\d+')[0] \
#             if response.xpath('//a[@name="view_v"]/h4/text()').re('\d+') else "0"
#         if counts:
#             counts = float(counts)
#             if counts<=4000:
#                 temp = response.xpath('//li[@class="con caritem"]')
#                 for x in temp:
#                     print x
#                     datasave1 = x.extract()
#                     urlbase = str(x.xpath('//a[@class="aimg"]/@href').extract_first())
#                     print urlbase
#                     print len(urlbase)
#                     url = "http://www.xin.com" + urlbase
#                     print url
#                     print "parse3"
#                     print type(url)
#                     if not (dfcheck(self.df, url, self.tag)):
#                         yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
#                 next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
#                 if next_page:
#                     urlbase = str(next_page.extract()[0])
#                     url = "http://www.xin.com" + urlbase
#                     yield scrapy.Request(url, self.select3_parse)
#                 else:
#                     for href in response.xpath('//div[@class="select-menu"]/div[@class="menu menu6"]/dd/a/@href'):
#                         urlbase = str(href.extract())
#                         url = "http://www.xin.com" + urlbase
#                         yield scrapy.Request(url, self.select4_parse)
#
#
#
#
#     #parse output
#     def select4_parse(self,response):
#         temp = response.xpath('//li[@class="con caritem"]')
#         for x in temp:
#             datasave1 = x.extract()
#             urlbase = str(x.xpath('//a[@class="aimg"]/@href').extract_first())
#             url = "http://www.xin.com" + urlbase
#             if not (dfcheck(self.df, url, self.tag)):
#                 yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
#         next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href')
#         if next_page:
#             urlbase = str(next_page.extract()[0])
#             url = "http://www.xin.com" + urlbase
#             yield scrapy.Request(url, self.select4_parse)
#
#     # get car infor
#     def parse_car(self, response):
#         # requests count
#         if self.tag == 'update':
#             addcounts = self.request_next()
#             if addcounts:
#                 self.size = min(self.size, self.carnum - self.reqcounts)
#                 for i in range(self.reqcounts, self.reqcounts + self.size):
#                     url = self.urllist[i]
#                     if url:
#                         yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
#         # count
#         self.counts += 1
#         logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
#         # dffile
#         dffile(self.fa, response.url, self.tag)
#         #base infor
#         datasave1 = "zero"
#         #key and status (sold or sale, price,time)
#         status = response.xpath('//div[@class="d-photo img-album"]/em')
#         status = "sold" if status else "sale"
#         price = response.xpath('//div[@class="jiage"]/p/text()')
#         price = price.extract_first()[1:-1] if price else "zero"
#         datetime =response.xpath('//li[@class="br"]/em/text()')
#         datetime = datetime.extract_first() if datetime else "zero"
#         #item loader
#         item = GanjiItem()
#         item['url'] = response.url
#         item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#         item['website'] = website
#         item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+str(datetime)
#         item['pagetime'] = datetime
#         item['datasave'] = [datasave1, re.sub(r'\s+', ' ', response.xpath('//html').extract_first())]
#         yield item
#
# #new
# class CarSpider_new(CarSpider):
#
#     #basesetting
#     name = spidername_new
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider_new, self).__init__(**kwargs)
#         #tag
#         self.tag='new'
#         # spider setting
#         self.df =spider_new_Init(
#                 spidername=spidername_new,
#                 dbname=self.dbname,
#                 website=website,
#                 carnum=self.carnum)
#         filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
#         self.fa = open(filename, "a")
#
# #update
# class CarSpider_update(CarSpider,update):
#
#     #basesetting
#     name = spidername_update
#
#     def __init__(self, **kwargs):
#         # load
#         super(CarSpider_update, self).__init__(**kwargs)
#         #settings
#         self.urllist = spider_update_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum
#         )
#         self.carnum = len(self.urllist)
#         self.tag='update'
#         #do
#         super(update, self).start_requests()

#-*- coding: UTF-8 -*-
import scrapy
from scrapy.spiders import SitemapSpider
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
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import re



website ='youxin'
spidername_new = 'youxin_new'
spidername_update = 'youxin_update'
carnum=20000000

#main
class CarSpider(scrapy.Spider):
    #basesetting
    name = website
    allowed_domains = ["xin.com"]
    #sitemap_urls = ['http://www.xin.com/sitemap/sitemapIndex_02.xml']
    #sitemap_follow = ['http://www.xin.com/sitemap/day_car_detail_']
    #sitemap_rules = [
        #('www.xin.com/sitemap/day_car_detail_', 'parse_list'),
    #]
    start_urls=['https://www.xin.com/quanguo/']
    # start_urls=['http://192.168.1.106/youxin/?date=detail20180206','http://192.168.1.106/youxin/?date=detail20180207','http://192.168.1.106/youxin/?date=detail20180202']

    settings.set('CrawlCar_Num', carnum, priority='cmdline')
    settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
    settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    custom_settings = {
        'COOKIES_ENABLED': False,
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=15000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # self.browser.set_page_load_timeout(100)
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    #brand select
    # def parse(self,response):
    #     print(response.body)
    #     # print response.url
    #     Alphabet=['A','B','C','D','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','W','X','Y','Z',]
    #     for i in Alphabet:
    #         strtemp = '//dt[contains(text(),"' + i + '")]/../dd/a/@href'
    #         for href in response.xpath(strtemp):
    #             urlbase=str(href.extract())
    #             url="https://www.xin.com"+urlbase
    #             yield scrapy.Request(url, callback=self.select2_parse)
        #for href in response.xpath('//loc/text()'):
            #url= href.extract()
            #if not (dfcheck(self.df, url, self.tag)):
                #yield scrapy.Request(url,callback=self.parse_car)

    # def parse(self, response):
    #     # print(response.xpath("//a"))
    #     for href in response.xpath("//a"):
    #         url = response.urljoin(href.xpath("@href").extract_first())
    #         yield scrapy.Request(url=url, callback=self.parse_car, dont_filter=True)


    def parse(self, response):
        with open("json_or_txt/brand.txt") as f:
            brand = f.read()
            brand_list = brand.split("\n")
            print(brand_list)
        with open("json_or_txt/city.txt") as f:
            city = f.read()
            city_list = city.split("\n")
            print(city_list)
        for brand in brand_list:
            if brand != "":
                for city in city_list:
                    if city != "":
                        yield scrapy.Request("https://www.xin.com/%s/%s/" % (city, brand), callback=self.select4_parse)


    #price select brand parse
    def select2_parse(self,response):
        counts = response.xpath('//a[@name="view_v"]/h4/text()').re('\d+')[0] \
            if response.xpath('//a[@name="view_v"]/h4/text()').re('\d+') else "0"
        if counts:
            counts=float(counts)
            if counts<=4000:
                # temp=response.xpath('//li[@class="con caritem"]')
                temp = response.xpath('//li[@class="con caritem conHeight"]')
                for x in temp:
                    # print x
                    datasave1=x.extract()
                    urlbase = x.xpath('//a[@class="aimg"]/@href').extract_first()
                    url = response.urljoin(urlbase)
                    # urlbase=str(x.xpath('//a[@class="aimg"]/@href').extract_first())
                    #print urlbase
                    #print len(urlbase)
                    # url="http://www.xin.com"+urlbase
                    # print url
                    # print type(url)
                    if not (dfcheck(self.df,url,self.tag)):
                        yield scrapy.Request(url,meta={"datasave1":datasave1},callback=self.parse_car)
                next_page= response.xpath(u'//a[contains(text(),"下一页")]')
                if next_page:
                    urlbase = response.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    # urlbase=str(next_page.extract()[0])
                    # url="http://www.xin.com"+urlbase
                    yield scrapy.Request(url,self.select2_parse)
            else:
                for href in response.xpath('//div[@class="select-con"][3]/dl/dd/a'):
                    urlbase = href.xpath('@href').extract_first()
                    url = response.urljoin(urlbase)
                    # urlbase=str(href.extract())
                    # url="http://www.xin.com"+urlbase
                    yield scrapy.Request(url,self.select3_parse)


    #price parse output select
    def select3_parse(self,response):
        counts = response.xpath('//a[@name="view_v"]/h4/text()').re('\d+')[0] \
            if response.xpath('//a[@name="view_v"]/h4/text()').re('\d+') else "0"
        if counts:
            counts = float(counts)
            if counts<=4000:
                temp = response.xpath('//li[@class="con caritem conHeight"]')
                for x in temp:
                    # print x
                    urlbase = x.xpath('//a[@class="aimg"]/@href').extract_first()
                    url = response.urljoin(urlbase)
                    datasave1 = x.extract()
                    # urlbase = str(x.xpath('//a[@class="aimg"]/@href').extract_first())
                    # print urlbase
                    # print len(urlbase)
                    # url = "http://www.xin.com" + urlbase
                    # print url
                    # print "parse3"
                    # print type(url)
                    if not (dfcheck(self.df, url, self.tag)):
                        yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
                next_page = response.xpath(u'//a[contains(text(),"下一页")]')
                if next_page:
                    urlbase = next_page.xpath('@href').extract_first()
                    # urlbase = str(next_page.extract()[0])
                    url = response.urljoin(urlbase)
                    # url = "http://www.xin.com" + urlbase
                    yield scrapy.Request(url, self.select3_parse)
                else:
                    for href in response.xpath('//div[@class="select-menu"]/div[@class="menu menu6"]/dd/a'):
                        urlbase = href.xpath('@href').extract_first()
                        # urlbase = str(href.extract())
                        url = response.urljoin(urlbase)
                        # url = "http://www.xin.com" + urlbase
                        yield scrapy.Request(url, self.select4_parse)




    #parse output
    def select4_parse(self,response):
        temp = response.xpath('//li[@class="con caritem conHeight"]')
        for x in temp:
            datasave1 = x.extract()
            urlbase = x.xpath('//a[@class="aimg"]/@href').extract_first()
            # urlbase = str(x.xpath('//a[@class="aimg"]/@href').extract_first())
            # url = "http://www.xin.com" + urlbase
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={'datasave1': datasave1}, callback=self.parse_car)
        next_page = response.xpath(u'//a[contains(text(),"下一页")]')
        if next_page:
            urlbase = next_page.xpath('@href').extract_first()
            # urlbase = str(next_page.extract()[0])
            # url = "http://www.xin.com" + urlbase
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, self.select4_parse)

    # get car infor
    def parse_car(self, response):
        # print(response.body)
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
        logging.log(msg="download              " + str(self.counts) + "                  items",level=logging.INFO)
        # dffile
        dffile(self.fa, response.url, self.tag)
        #base infor
        datasave1 = "zero"
        #key and status (sold or sale, price,time)
        status = response.xpath('//div[@class="d-photo img-album"]/em')
        status = "sold" if status else "sale"
        # price = response.xpath('//div[@class="jiage"]/p/text()')
        if response.xpath('//span[@class="cd_m_info_jg"]/b/text()'):
            price = response.xpath('//span[@class="cd_m_info_jg"]/b/text()').extract_first()
        else:
            price = "zero"
        # price = price.extract_first()[1:-1] if price else "zero"
        datetime =response.xpath('//li[@class="br"]/em/text()')
        datetime = datetime.extract_first() if datetime else "zero"
        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+str(datetime)
        print(item['status'])
        item['pagetime'] = datetime
        item['datasave'] = [datasave1, re.sub(r'\s+', ' ', response.xpath('//html').extract_first())]
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