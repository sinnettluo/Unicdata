# #-*- coding: UTF-8 -*-
# #-*- coding: UTF-8 -*-
# import scrapy
# from ganji.items import GanjiItem
# import time
# import logging
# from hashlib import md5
# from scrapy.mail import MailSender
# from SpiderInit import spider_original_Init
# from SpiderInit import spider_new_Init
# from SpiderInit import spider_update_Init
# from SpiderInit import dfcheck
# from SpiderInit import dffile
# from Car_spider_update import update
#
#
# website ='zg2sc'
# spidername_new = 'zg2sc_new'
# spidername_update = 'zg2sc_update'
#
# #main
# class CarSpider(scrapy.Spider):
#
#     #basesetting
#     name = website
#     allowed_domains = ["zg2sc.cn"]
#     start_urls=['http://www.zg2sc.cn/allcars/1.html',]
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider, self).__init__(**kwargs)
#         #setting
#         self.tag='original'
#         self.counts=0
#         self.carnum=300000
#         self.dbname = 'usedcar'
#         # spider setting
#         spider_original_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         self.df='none'
#         self.fa='none'
#
#     # car list parse
#     def parse(self,response):
#         for i in range(1,20000):
#             url ="http://www.zg2sc.cn/allcars/"+str(i)+".html"
#             yield scrapy.Request(url,callback=self.parse_list)
#
#     # car list parse
#     def parse_list(self, response):
#         for href in response.xpath('//div[@class="search_car_lb"]/dl'):
#             urlbase = href.xpath('dt/a/@href').extract_first()
#             datasave1 = href.extract()
#             url = response.urljoin(urlbase)
#             if not (dfcheck(self.df, url, self.tag)):
#                 yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
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
#
#         # base infor
#         # count
#         self.counts += 1
#         logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
#         # dffile
#         dffile(self.fa, response.url, self.tag)
#         # datasave
#         if response.meta.has_key('datasave1'):
#             datasave1 = response.meta['datasave1']
#         else:
#             datasave1 = 'zero'
#         #key and status (sold or sale, price,time)
#         status = response.xpath(u'//p[contains(text(),"在售")]')
#         status = "sale" if status else "sold"
#         price = response.xpath('//input[@id="price"]/@value')
#         price = str(price.extract_first()) if price else "zero"
#         datetime =response.xpath('//div[@class="carfile_xinxi_text_right"]/dl/dd[2]/text()')
#         datetime =datetime.extract_first() if datetime else "zero"
#         if price !="zero":
#             # count
#             self.counts += 1
#             logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
#             #item loader
#             item = GanjiItem()
#             item['url'] = response.url
#             item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#             item['website'] = website
#             item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
#             item['pagetime'] = datetime
#             item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
#             yield item
#         else:
#             pass
#             #self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=website, body="Scrapy Error!",
#                              #cc=["hzhy_1@163.com"])
#
# # new
# class CarSpider_new(CarSpider):
#
#     # basesetting
#     name = spidername_new
#
#     def __init__(self, **kwargs):
#         # args
#         super(CarSpider_new, self).__init__(**kwargs)
#         # tag
#         self.tag = 'new'
#         # spider setting
#         self.df = spider_new_Init(
#             spidername=spidername_new,
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum)
#         filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
#         self.fa = open(filename, "a")
#
# # update
# class CarSpider_update(CarSpider, update):
#
#     # basesetting
#     name = spidername_update
#
#     def __init__(self, **kwargs):
#         # load
#         super(CarSpider_update, self).__init__(**kwargs)
#         # settings
#         self.urllist = spider_update_Init(
#             dbname=self.dbname,
#             website=website,
#             carnum=self.carnum
#         )
#         self.carnum = len(self.urllist)
#         self.tag = 'update'
#         # do
#         super(update, self).start_requests()

#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
import logging
from hashlib import md5
from scrapy.mail import MailSender
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
from ganji.redial import Redial
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


website ='zg2sc'
spidername_new = 'zg2sc_new'
spidername_update = 'zg2sc_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["zg2sc.cn"]
    start_urls=['http://www.zg2sc.cn/usedcar/search_result.do?sr=%C7%EB%CA%E4%C8%EB%C4%FA%D2%AA%CB%D1%CB%F7%B5%C4%B3%B5%C1%BE%C6%B7%C5%C6',]
    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=300000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

        # rd = Redial()
        # rd.connect()
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()


    def parse(self, response):
        # print(response.body.decode('gbk'))
        for href in response.xpath('//div[@class="search_car_lb"]/dl'):
            urlbase = href.xpath('dt/a/@href').extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
        next_page= response.xpath(u'//a[contains(text()," >> ")]')
        if next_page:
            nexturl = next_page.xpath('@href').extract_first()
            url = response.urljoin(nexturl)
            yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse)

    # car list parse
    # def parse(self,response):
    #     for i in range(1,20000):
    #         url ="http://www.zg2sc.cn/allcars/"+str(i)+".html"
    #         yield scrapy.Request(url,callback=self.parse_list)

    # # car list parse
    # def parse_list(self, response):
    #     for href in response.xpath('//div[@class="search_car_lb"]/dl'):
    #         urlbase = href.xpath('dt/a/@href').extract_first()
    #         datasave1 = href.extract()
    #         url = response.urljoin(urlbase)
    #         if not (dfcheck(self.df, url, self.tag)):
    #             yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
    #
    # # get car infor
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
        status = response.xpath(u'//p[contains(text(),"在售")]')
        status = "sale" if status else "sold"
        price = response.xpath('//input[@id="price"]/@value')
        price = str(price.extract_first()) if price else "zero"
        datetime =response.xpath('//div[@class="carfile_xinxi_text_right"]/dl/dd[2]/text()')
        datetime =datetime.extract_first() if datetime else "zero"
        if price !="zero":
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-"+datetime
            item['pagetime'] = datetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]
            yield item
        else:
            pass
            #self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=website, body="Scrapy Error!",
                             #cc=["hzhy_1@163.com"])

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