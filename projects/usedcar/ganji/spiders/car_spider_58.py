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
from scrapy.conf import settings
import random
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy import signals
# from pyvirtualdisplay import Display

website ='che58'
spidername_new = 'che58_new'
spidername_update = 'che58_update'

#original
class CarSpider(scrapy.Spider):

    #basesetting
    # Delay=random.uniform(2.5,3.5)
    name = website
    allowed_domains = ["58.com"]
    start_urls = [
        "http://www.58.com/ershouche/changecity/"
    ]
    # settings.set('DOWNLOAD_DELAY', Delay, priority='cmdline')

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting
        self.tag='original'
        self.counts=0
        self.carnum=5000000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        # self.browser = webdriver.Chrome(executable_path=settings['CHROME_PATH'])
        # self.browser = webdriver.Chrome(
        #     executable_path="/root/chromedriver.exe")
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities[
            "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'], desired_capabilities=desired_capabilities)
        self.browser.set_page_load_timeout(20)
        self.browser.implicitly_wait(100)
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()
        # self.display.stop()

    # region select
    def parse(self, response):
        urllist=[]
        sblist=['http://hk.58.com/ershouche/','http://am.58.com/ershouche/','http://tw.58.com/ershouche/','http://diaoyudao.58.com/','http://cn.58.com/ershouche/']
        for href in response.xpath('//dl[@id="clist"]/dd/a/@href'):
            url = str(response.urljoin(href.extract()))
            urllist.append(url)
        for urlbase in urllist:
            urlc=urlbase
            if urlc not in sblist:
                yield scrapy.Request(urlc,self.select2_parse)
            # yield scrapy.Request(url, self.select2_parse)

    # type select,region parse
    def select2_parse(self, response):
        # logging.log(msg="do this step2",level=logging.INFO)
        # print(response.body)
        counts = response.xpath('//div[@class="info_funcs_right"]/span/i/text()')
        listok = True
        if counts:
            counts = float(counts.extract_first())
            if counts > 3500:
                listok =False
        if listok:
            for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
                url = str(href.xpath('a/@href').extract_first())
                datasave1 = href.extract()
                # url = response.urljoin(urlbase)
                # print urlbase
                # print url
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select2_parse)
        else:
            for href in response.xpath(u'//dt[contains(text(),"类型：")]/../dd/a/@href')[1:14]:
                url = str(href.extract())
                yield scrapy.Request(url, self.select3_parse)

    # brand select,type parse
    def select3_parse(self, response):
        # logging.log(msg="do this step3", level=logging.INFO)
        counts = response.xpath('//div[@class="info_funcs_right"]/span/i/text()')
        listok = True
        if counts:
            counts = float(counts.extract_first())
            if counts > 3500:
                listok = False
        if listok:
            for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
                url = str(href.xpath('a/@href').extract_first())
                datasave1 = href.extract()
                # urlbase = href.xpath('td[@class="t"]/a/@href').extract_first()
                # datasave1 = href.extract()
                # url = response.urljoin(urlbase)
                # print urlbase
                # print url
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select2_parse)
        else:
            hreflist = response.xpath('//input[@id="data1"]/@value').extract_first().split('},{')
            for href in hreflist:
                urlbase = href.split("','")[0].split("':'")[1]
                url = response.urljoin(urlbase)
                yield scrapy.Request(url, self.select4_parse)

    # years select,brand parse
    def select4_parse(self, response):
        # logging.log(msg="do this step4", level=logging.INFO)
        counts = response.xpath('//div[@class="info_funcs_right"]/span/i/text()')
        listok = True
        if counts:
            counts = float(counts.extract_first())
            if counts > 3500:
                listok = False
        if listok:
            for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
                url = str(href.xpath('a/@href').extract_first())
                datasave1 = href.extract()
                # urlbase = href.xpath('td[@class="t"]/a/@href').extract_first()
                #
                # datasave1 = href.extract()
                # url = response.urljoin(urlbase)
                # print urlbase
                # print url
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select2_parse)
        else:
            for href in response.xpath(u'//span[contains(text(),"车龄")]/../../ul/li')[1:7]:
                url = str(href.xpath('a/@href').extract_first())
                yield scrapy.Request(url, self.select5_parse)

    # output select,years parse
    def select5_parse(self, response):
        # logging.log(msg="do this step5", level=logging.INFO)
        counts = response.xpath('//div[@class="info_funcs_right"]/span/i/text()')
        listok = True
        if counts:
            counts = float(counts.extract_first())
            if counts > 3500:
                listok = False
        if listok:
            for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
                url = str(href.xpath('a/@href').extract_first())
                datasave1 = href.extract()
                # urlbase = href.xpath('td[@class="t"]/a/@href').extract_first()
                # datasave1 = href.extract()
                # url = response.urljoin(urlbase)
                # print urlbase
                # print url
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select2_parse)
        else:
            for href in response.xpath(u'//span[contains(text(),"排量")]/../../ul/li')[1:8]:
                url = str(href.xpath('a/@href').extract_first())
                yield scrapy.Request(url, self.select6_parse)

    # geartype select,output parse
    def select6_parse(self, response):
        # logging.log(msg="do this step6", level=logging.INFO)
        counts = response.xpath('//div[@class="info_funcs_right"]/span/i/text()')
        listok = True
        if counts:
            counts = float(counts.extract_first())
            if counts > 3500:
                listok = False
        if listok:
            for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
                url = str(href.xpath('a/@href').extract_first())
                datasave1 = href.extract()
                # urlbase = href.xpath('td[@class="t"]/a/@href').extract_first()
                # datasave1 = href.extract()
                # url = response.urljoin(urlbase)
                # print urlbase
                # print url
                if not (dfcheck(self.df, url, self.tag)):
                    yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
            # next page
            next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.select2_parse)
        else:
            for href in response.xpath(u'//span[contains(text(),"变速箱")]/../../ul/li')[1:3]:
                url = str(href.xpath('a/@href').extract_first())
                yield scrapy.Request(url, self.select7_parse)

    # geartype parse
    def select7_parse(self, response):
        # logging.log(msg="do this step7", level=logging.INFO)
        for href in response.xpath('//ul[@class="car_list ac_container"]/li/div[@class="col col2"]'):
            url = str(href.xpath('a/@href').extract_first())
            datasave1 = href.extract()
            # urlbase = href.xpath('td[@class="t"]/a/@href').extract_first()
            # datasave1 = href.extract()
            # url = response.urljoin(urlbase)
            # print urlbase
            # print url
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url, meta={"datasave1": datasave1}, callback=self.parse_car)
        # next page
        next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.select7_parse)

    # get car infor
    def parse_car(self, response):
        # logging.log(msg="do parse car", level=logging.INFO)
        # requests count
        if self.tag=='update':
            addcounts = self.request_next()
            if addcounts:
                self.size = min(self.size, self.carnum - self.reqcounts)
                for i in range(self.reqcounts, self.reqcounts + self.size):
                    url = self.urllist[i]
                    if url:
                        yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)
        #count
        self.counts +=1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        #error check
        if not("callback.58.com" in response.url):
            #dffile
            dffile(self.fa,response.url,self.tag)
            #base infor
            if response.meta.has_key('datasave1'):
                datasave1 = response.meta['datasave1']
            else:
                datasave1='zero'
            #key and status (sold or sale, price,time)
            status = response.xpath('//a[@class="btn_3"]')
            status = "sold" if status else "sale"
            price = response.xpath('//span[@class="jiage"]/text()')
            price = str(price.extract_first()) if price else "zero"
            datetime =response.xpath('//div[@class="posttime"]/span/text()')
            datetime ="-".join(datetime.re('\d+')) if datetime else "zero"
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
            logging.log(msg="Response.url:" + response.url +"-"+"Error" , level=logging.INFO)

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





