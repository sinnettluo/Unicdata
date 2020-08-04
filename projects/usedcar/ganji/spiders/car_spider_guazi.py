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
import math
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy import signals
from scrapy.conf import settings


website ='guazi'
spidername_new = 'guazi_new'
spidername_update = 'guazi_update'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["guazi.com"]
    # start_urls = [ "http://m.guazi.com/www/buy/?act=changeCity",]
    start_urls = ["https://www.guazi.com/qg/buy",]
    custom_settings = {
        'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    # settings.set('DOWNLOAD_DELAY', 2.5, priority='cmdline')
    # settings.set('RANDOMIZE_DOWNLOAD_DELAY', True, priority='cmdline')

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 1500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'

        # options = webdriver.ChromeOptions()
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        # print('opening browser')
        # # options.add_argument('--proxy-server=http://%s' % "121.225.24.3:18888")
        # self.browser = webdriver.Chrome(
        #     executable_path=settings['CHROME_PATH'],
        #     chrome_options=options)




        self.desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        self.desired_capabilities["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs", desired_capabilities=self.desired_capabilities)
        # self.browser = webdriver.PhantomJS(executable_path="/home/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=self.desired_capabilities)

        # self.browser.start_session(self.desired_capabilities)
        # self.browser.set_page_load_timeout(300)

        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        print(response.body)
        lis = response.xpath("//ul[@class='carlist clearfix js-top']/li")
        print(lis)
        for li in lis:
            yield scrapy.Request(response.urljoin(li.xpath("./a/@href").extract_first()), callback=self.parse_car)

        next = response.xpath("//a[@class='next']/@href")
        print(next)
        if next:
            yield scrapy.Request(url=response.urljoin(next.extract_first()), callback=self.parse)
    # region select
    # def parse(self, response):
    #     if response.xpath('//li[@class=" js-change-city"]/@data-citydomain'):
    #         for href in response.xpath('//li[@class=" js-change-city"]/@data-citydomain'):
    #             region = href.extract()
    #             url = 'https://m.guazi.com/'+href.extract()+'/buy/'
    #             yield scrapy.Request(url,meta={"region":region,"page":"1"},callback=self.select1_parse)
    #     else:
    #         yield scrapy.Request(url="http://m.guazi.com/www/buy/?act=changeCity", dont_filter=True)
    # brand select
    # def select1_parse(self, response):
    #     page300 = int(response.xpath('//div[@class="find-num bg-shadow active"]/text()').re('\d+')[0]) \
    #         if response.xpath('//div[@class="find-num bg-shadow active"]/text()').re('\d+') else 0
    #     if page300 >1500 and not(response.meta.has_key("brand")):
    #         url =response.url+"?act=changeBrand"
    #         yield scrapy.Request(url,meta={"region":response.meta["region"]}, callback=self.select2_parse)
    #     else:
    #         # if no page300, car select
    #         for href in response.xpath('//li[@class="list-item"]'):
    #             urlbase = href.xpath("a/@href").extract_first()
    #             datasave1 = href.extract()
    #             if urlbase:
    #                 url = "https://www.guazi.com"+urlbase.split('?')[0]+".htm"
    #                 if not (dfcheck(self.df, url, self.tag)):
    #                     yield scrapy.Request(url,meta={"datasave1":datasave1}, callback=self.parse_car)
    #         # next page
    #         total_page = math.ceil(float(page300)/float(30))
    #         next_page=int(response.meta["page"])+1
    #         if next_page <= total_page:
    #             href ="/o"+str(next_page)+"/"
    #             url_next = response.urljoin(href)
    #             yield scrapy.Request(url_next,meta={"region":response.meta["region"],"page":str(next_page)}, callback=self.select1_parse)

    # brand select
    # def select2_parse(self, response):
    #     for href in response.xpath('//li[@class=" js-change-brand"]/@data-brandurl'):
    #         urlbase = "https://m.guazi.com/"+response.meta["region"]+"/"+href.extract()+"/"
    #         yield scrapy.Request(urlbase, meta={"region":response.meta["region"],"page":"1","brand":"brand"},callback=self.select1_parse)

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

        # status check
        if response.status==200:
            # count
            self.counts += 1
            logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
            # dffile
            dffile(self.fa, response.url, self.tag)
            #base infor
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'
            #key and status (sold or sale, price,time)
            status = response.xpath('//*[@class="graybtn"]')
            status = "sold" if status else "sale"
            price = response.xpath('//b[@class="f30 numtype"]/text()')
            price = price.extract_first()[1:] if price else "zero"
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