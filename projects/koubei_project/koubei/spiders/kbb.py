# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import KBBItem
from scrapy.conf import settings
import pymongo

# 修改了过滤规则
website ='kbb'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://www.kbb.com/cars-for-sale/cars/used-cars/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        # settings.set('DOWNLOAD_DELAY', 5, priority='cmdline')


    def start_requests(self):

        return [scrapy.Request(url="https://www.kbb.com/cars-for-sale/cars/used-cars/", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})]


    def parse(self, response):
        # print(response.text)
        cars = response.xpath("//*[@id='listingsContainer']//*[@class='listing js-used-listing']")
        for car in cars:
            url = car.xpath(".//*[@class='js-vehicle-name']/@href").extract_first()
            yield response.follow(url=url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}, callback=self.parse_car,)

        next = response.xpath("//*[@class='nav-control js-nav-next js-pagination-link']")
        if next:
            url = next.xpath("@href").extract_first()
            yield response.follow(url=url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}, callback=self.parse,)



    def parse_car(self, response):
        item = KBBItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['title'] = response.xpath("//*[@class='primary-vehicle-title title-two ']/text()").extract_first().strip()
        item['level'] = response.xpath("//*[@class='breadcrumbs']/ul/li[7]/a/text()").extract_first()
        item['brandname'] = response.xpath("//*[@class='breadcrumbs']/ul/li[9]/a/text()").extract_first()
        item['familyname'] = response.xpath("//*[@class='breadcrumbs']/ul/li[11]/a/text()").extract_first()
        item['price'] = response.xpath("//*[@class='price js-price']/text()").extract_first().strip()
        item['vin'] = response.xpath("//*[@class='paragraph-one vin']/text()").extract_first().replace("VIN: ", "")
        item['stockNo'] = response.xpath("//*[@class='paragraph-one js-stock']/text()").extract_first().replace("Stock No: ", "")
        item['status'] = item['stockNo']

        details = response.xpath("//*[@class='details-list']/ul/li")
        for detail in details:
            if detail.xpath("text()").extract_first().find("Mileage: ") >= 0:
                item['mileage'] = detail.xpath("text()").extract_first().replace("Mileage: ", "")
            if detail.xpath("text()").extract_first().find("Body Style: ") >= 0:
                item['bodyStyle'] = detail.xpath("text()").extract_first().replace("Body Style: ", "")
            if detail.xpath("text()").extract_first().find("Exterior Color: ") >= 0:
                item['exterior'] = detail.xpath("text()").extract_first().replace("Exterior Color: ", "")
            if detail.xpath("text()").extract_first().find("Interior Color: ") >= 0:
                item['interior'] = detail.xpath("text()").extract_first().replace("Interior Color: ", "")
            if detail.xpath("text()").extract_first().find("Fuel Economy: ") >= 0:
                item['fuel'] = detail.xpath("text()").extract_first().replace("Fuel Economy: ", "")
            if detail.xpath("text()").extract_first().find("Engine: ") >= 0:
                item['engine'] = detail.xpath("text()").extract_first().replace("Engine: ", "")
            if detail.xpath("text()").extract_first().find("Fuel Type: ") >= 0:
                item['fuelType'] = detail.xpath("text()").extract_first().replace("Fuel Type: ", "")
            if detail.xpath("text()").extract_first().find("Transmission: ") >= 0:
                item['transmission'] = detail.xpath("text()").extract_first().replace("Transmission: ", "")
            if detail.xpath("text()").extract_first().find("Drive Type: ") >= 0:
                item['driveType'] = detail.xpath("text()").extract_first().replace("Drive Type: ", "")
            if detail.xpath("text()").extract_first().find("Doors: ") >= 0:
                item['doors'] = detail.xpath("text()").extract_first().replace("Doors: ", "")

            # print(item)
            yield item