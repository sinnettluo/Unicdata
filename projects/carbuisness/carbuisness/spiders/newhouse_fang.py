# -*- coding: utf-8 -*-
"""

C2017-27-2
二手房和新房分成两个程序，这是新房

"""
import scrapy
from carbuisness.items import NewhouseFangItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5

website='newhouse_fang_2018'

class CarSpider(scrapy.Spider):

    name=website
    start_urls=['http://newhouse.fang.com/house/s/']

    def __init__(self,**kwargs):
        #print "do init"
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=80000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self, response):
        print "do parse"
        cityurls_lists = response.xpath('//div[@class="city20141104nr"]/a')
        cityurls_list = cityurls_lists[1:]
        #print cityurls
        for cityurl in cityurls_list:
            url = cityurl.xpath('@href').extract_first()
            city = cityurl.xpath('text()').extract_first()
            print city + url
            # print "***************************************"
            metadata = {"city": city}

            #print url
            # yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle1, dont_filter=True)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)

    # def parse_middle1(self, response):
    #     #print "do parse_middle1"
    #     metadata = response.meta['metadata']
    #     if response.xpath('//li[@id="quyu_name"]//a'):
    #         areas = response.xpath('//li[@id="quyu_name"]//a')
    #         flag = 0    #第一个对应网页上的“不限”
    #         for area in areas:
    #             if flag:
    #                 districts = area.xpath('text()').extract()
    #                 x = 0
    #                 district = None
    #                 for dis in districts:
    #                     if x == 0:
    #                         x = 1
    #                         district = dis
    #                     else:
    #                         district += " " + dis
    #                 addmeta = {"district": district}
    #                 metadata = dict(metadata, **addmeta)
    #                 urlbase = area.xpath('@href').extract_first()
    #                 url = response.urljoin(urlbase)
    #                 yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle2, dont_filter=True)
    #             else:
    #                 flag = 1
    #     else:
    #         yield scrapy.Request(response.url, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)
    #
    # def parse_middle2(self, response):
    #     #print "do parse_middle2"
    #     metadata = response.meta['metadata']
    #     coutys = response.xpath('//div[@class="quyu"]//li/a')
    #     #flag = 0    #这第一个元素对应于页面上的“不限”
    #     for county_temp in coutys:
    #         #if flag:
    #         county = county_temp.xpath('text()').extract_first()
    #         addmeta = {"county": county}
    #         metadata = dict(metadata, **addmeta)
    #         countyurlbase = county_temp.xpath('@href').extract_first()
    #         countyurl = response.urljoin(countyurlbase)
    #         #print countyurl
    #         yield scrapy.Request(countyurl, meta={"metadata":metadata}, callback=self.parse_middle3, dont_filter=True)
    #         #else:
    #         #    flag = 1

    def parse_middle3(self, response):
        #print "do parse_middle3"
        metadata = response.meta['metadata']
        # http://newhouse.fang.com/house/s/
        if response.xpath('//div[@id="newhouse_loupai_list"]/ul/li'):
            newhouselist = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')
            for newhouse in newhouselist:
                if newhouse.xpath('.//div[@class="nlcd_name"]/a/@href'):
                    url = newhouse.xpath('.//div[@class="nlcd_name"]/a/@href').extract_first()
                    yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle4, dont_filter=True)
            next_page = response.xpath(u'//a[contains(text(),"下一页")]')
            if next_page:
                next = next_page.xpath('@href').extract_first()
                url = response.urljoin(next)
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)
        # http://newhouse.cq.fang.com/house/s/
        elif response.xpath('//div[@class="nhouse_list"]//ul/li//div[@class="clearfix"]//div[@class="nlcd_name"]/a'):
            newhouselist = response.xpath('//div[@class="nhouse_list"]//ul/li//div[@class="clearfix"]//div[@class="nlcd_name"]/a')
            for newhouse in newhouselist:
                url = newhouse.xpath('@href').extract_first()
                test = re.findall("http", url)
                if test:
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle4, dont_filter=True)
                else:
                    join_url = response.urljoin(url)
                    yield scrapy.Request(join_url, meta={"metadata": metadata}, callback=self.parse_middle4,dont_filter=True)
            next_page = response.xpath(u'//a[contains(text(),"下一页")]')
            if next_page:
                next = next_page.xpath('@href').extract_first()
                url = response.urljoin(next)
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)
        else:
            newhouselist = response.xpath('//div[@class="sslist"]/div/ul/li/strong/a')
            for newhouse in newhouselist:
                if newhouse.xpath('@href'):
                    url = newhouse.xpath('@href').extract_first()
                    yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle4,dont_filter=True)
            next_page = response.xpath('//li[@class="pagearrowright"]/a')
            if next_page:
                next = next_page.xpath('@href').extract_first()
                url = response.urljoin(next)
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_middle3, dont_filter=True)

    def parse_middle4(self, response):
        #print "do parse_middle4"
        #print response.url
        metadata = response.meta['metadata']

        #   这里会得到两种不同页面，例如下面两个：
        #   http://wandaguangchangfh.fang.com/
        #   http://yunshanlichi.fang.com/
        #   但是可以统一解析
        url = response.xpath(u'//a[contains(text(),"更多详细信息")]/@href').extract_first()
        if url:
            test = re.findall("http", url)
            if test:
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
            else:
                join_url = response.urljoin(url)
                yield scrapy.Request(join_url, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)
        # http://xindongfanghz2.fang.com/?ctm=1.anshan.xf_search.lplist.17
        elif response.xpath(u'//div[@class="xqnavN"]//li/a[contains(text(),"小区详情")]/@href'):
            url_village = response.xpath(u'//div[@class="xqnavN"]//li/a[contains(text(),"小区详情")]/@href').extract_first()
            yield scrapy.Request(url_village, meta={"metadata": metadata}, callback=self.parse_info, dont_filter=True)



    def parse_info(self, response):
        #print "parse_info"
        item = NewhouseFangItem()
        metadata = response.meta['metadata']
        #item['province'] = metadata['province']
        city_district = response.xpath("//div[@class='header_mnav']/p/a/text()").extract()
        item['city_district'] = '>'.join(city_district)

        item['city'] = metadata['city']
        try:
            item['district'] = metadata['district']
        except:
            item['district'] = "-"

        try:
            item['county'] = metadata['county']
        except:
            item['county'] = "-"
        item['url'] = response.url
        item['website'] = website
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        lis = response.xpath("//li")
        print(lis)
        for li in lis:
            if(li.xpath("./div[contains(@class, 'list-left')]")):
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"楼盘地址") >= 0:
                    item['location'] = li.xpath('./div[2]/text()').extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"总") >= 0:
                    item['housenum'] = li.xpath('./div[2]/text()').extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"交房时间") >= 0:
                    item['completetime'] = li.xpath('./div[2]/text()').extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"开盘时间") >= 0:
                    item['opening_quotation'] = li.xpath('./div[2]/text()').extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"建筑面积") >= 0:
                    item['area'] = li.xpath('./div[2]/text()').extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"停") >= 0:
                    item['parkingnum'] = li.xpath('./div[2]/text()').extract_first()
                item['price'] = response.xpath("//div[@class='main-info-price']/em/text()").extract_first()
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"物业类别") >= 0:
                    item['buildtype'] = li.xpath('./div[2]/text()').extract_first()

                # print(li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first() + str(len(li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first())))
                if li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first().find(u"开") >= 0 and len(li.xpath("./div[contains(@class, 'list-left')]/text()").extract_first()) == 1:
                    item['factoryname'] = li.xpath('./div[2]/a/text()').extract_first()
        # print(item)
        yield item





        #   几种不一样的页面解析方式不一样，例如：
        #   http://832895.fang.com//house/1110832895/housedetail.htm
        #   http://wanlinfang.fang.com/house/2110175658/housedetail.htm
        #
        # if response.xpath(u'//div[contains(text(),"楼盘地址")]/../div[2]/text()'):
        #     item['location'] = response.xpath(u'//div[contains(text(),"楼盘地址")]/../div[2]/text()').extract_first()
        # elif response.xpath(u'//strong[contains(text(),"小区地址")]/../@title'):
        #     item['location'] = response.xpath(u'//strong[contains(text(),"小区地址")]/../@title').extract_first()
        #     item['buildingname'] = response.xpath('//h1/a/text()').extract_first()
        #
        #     if response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()'):
        #         housenumbase = response.xpath(u'//strong[contains(text(),"总 户 数：")]/../text()').extract_first()
        #         item['housenum'] = re.findall("\d+", housenumbase)[0]
        #     else:
        #         item['housenum'] = "-"
        #
        #     item['handover_time'] = ""
        #     item['completetime'] = response.xpath(u'//strong[contains(text(),"竣工时间：")]/../text()').extract_first()
        #     # item['opening_quotation'] = response.xpath(u'//strong[contains(text(),"开盘时间")]/../text()').extract_first()
        #     item['area'] = response.xpath(u'//strong[contains(text(),"建筑面积：")]/../text()').extract_first()
        #     item['parkingnum'] = response.xpath(u'//strong[contains(text(),"停 车 位：")]/../text()').extract_first()
        #     item['price'] = response.xpath(u'//dt[contains(text(),"本月均价")]/../dd/span/text()').extract_first()
        #     item['buildtype'] = response.xpath(u'//strong[contains(text(),"物业类别：")]/../text()').extract_first()
        #     item['factoryname'] = response.xpath(u'//strong[contains(text(),"开 发 商：")]/../text()').extract_first()
        #
        # else:
        #     item['location'] = "-"
        #
        # if response.xpath('//h1/a/text()'):
        #     item['buildingname'] = response.xpath('//h1/a/text()').extract_first()
        # else:
        #     item['buildingname'] = "-"
        #
        # if response.xpath(u'//ul[@class="clearfix list"]/li/div[contains(text(),"总")]/i/../../div[2]/text()'):
        #     item['housenum'] = response.xpath(u'//ul[@class="clearfix list"]/li/div[contains(text(),"总")]/i/../../div[2]/text()').extract_first()
        # else:
        #     item['housenum'] = "-"
        #
        # if response.xpath(u'//div[contains(text(),"开盘时间")]/../div[2]/text()'):
        #     item['completetime'] = response.xpath(u'//div[contains(text(),"开盘时间")]/../div[2]/text()').extract_first()
        # else:
        #     item['completetime'] = "-"
        #
        # if response.xpath(u'//div[contains(text(),"建筑面积：")]/../div[2]/text()'):
        #     item['area'] = response.xpath(u'//div[contains(text(),"建筑面积：")]/../div[2]/text()').extract_first()
        # else:
        #     item['area'] = "-"
        #
        # if response.xpath(u'//ul[@class="clearfix list"]/li/div[contains(text(),"停")]/../div[@class="list-right"]/text()'):
        #     item['parkingnum'] = response.xpath(u'//ul[@class="clearfix list"]/li/div[contains(text(),"停")]/../div[@class="list-right"]/text()').extract_first()
        # elif response.xpath(u'//div[contains(text(),"停车位")]/../div[2]/text()'):
        #     item['parkingnum'] = response.xpath(u'//div[contains(text(),"停车位")]/../div[2]/text()').extract_first().strip()
        # else:
        #     item['parkingnum'] = "-"
        #
        # if response.xpath('//div[@class="main-info-price"]/em/text()'):
        #     item['price'] = response.xpath('//div[@class="main-info-price"]/em/text()').extract_first().strip()
        # else:
        #     item['price'] = "-"
        #
        # if response.xpath(u'//div[contains(text(),"物业类别：")]/../div[2]/text()'):
        #     item['buildtype'] = response.xpath(u'//div[contains(text(),"物业类别：")]/../div[2]/text()').extract_first().strip()
        # else:
        #     item['buildtype'] = "-"
        #
        # if response.xpath(u'//div[contains(text(),"开")]/i/../../div[2]/a[1]/text()'):
        #     item['factoryname'] = response.xpath(u'//div[contains(text(),"开")]/i/../../div[2]/a[1]/text()').extract_first()
        # else:
        #     item['factoryname'] = "-"

        # yield item

