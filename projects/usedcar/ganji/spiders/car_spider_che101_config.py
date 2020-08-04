#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
from scrapy.conf import settings
from hashlib import md5
carnum = 300000
website ='che101_config'

#main
class CarSpider(scrapy.Spider):
    #basesetting
    name = website
    allowed_domains = ["che101.com"]
    start_urls = [
        "http://www.che101.com/buycar/",
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        settings.set('CrawlCar_Num', carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    # get car list
    def parse(self, response):
        # car_item
        for href in response.xpath('//ul[@class="carList_286 cf"]/li'):
            carid = str(href.xpath('a/@href').re('\d+')[0])
            urlbase="http://www.che101.com/buycar/cartypeconfig/"+carid+".html"
            url = response.urljoin(urlbase)
            yield scrapy.Request(url,callback= self.parse_car)
            # next page
            next_page = response.xpath('//a[@class="next"]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.parse)

    # get car infor
    def parse_car(self, response):
        # key and status (sold or sale, price,time)
        # item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['pagetime'] = "zero"
        item['datasave'] = response.xpath('//html').extract_first()
        yield item