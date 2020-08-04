#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
from scrapy.conf import settings
carnum = 3000000
website ='chemao_config'

#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["chemao.com"]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        settings.set('CrawlCar_Num',carnum,priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        #global carnum
        cars = []
        for i in range(1, carnum):
                url = "http://www.chemao.com/index.php?app=show&act=show_more&id=" + str(i)
                car = scrapy.Request(url,headers={'User-Agent': " Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3"})
                cars.append(car)
        return cars

    # get car infor
    def parse(self, response):
        #item loader
        item = GanjiItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['datasave'] = response.xpath('//html').extract_first()
        yield item