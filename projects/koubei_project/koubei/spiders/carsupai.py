# -*- coding: utf-8 -*-
import re
import time
from copy import deepcopy

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.mail import MailSender
import logging
import json

from koubei.items import chesupaiItem

settings = get_project_settings()

website = 'carsupai'


class CarsupaiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['carsupai.cn']
    start_urls = ['http://chesupai.cn/']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 16,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(CarsupaiSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 800000
        self.city = settings['CITY']

        self.cityDomain = ""

        self.UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        self.cookies = {
            'cityDomain': '{}'.format(self.cityDomain),
        }
        self.headers = {
            'User-agent': "{}".format(self.UserAgent),
            'cookies': "cityDomain={}".format(self.cityDomain),
        }

    def start_requests(self):
        url = "http://www.chesupai.cn/index/"
        return [scrapy.Request(url=url)]

    def parse(self, response):
        for href in response.xpath('//div[@class="city-all"]/dl[not(@class="c-fore1")]/dd/a/@href').extract():
            city = re.findall(r'domain=(.*?)&', href)[0]
            url = "https://www.chesupai.cn/list/" + city + "/"
            yield scrapy.Request(
                url=url,
                callback=self.parse_brand_url,
            )

    def parse_brand_url(self, response):
        item = chesupaiItem()
        li_list = response.xpath("//ul[@class='gzp-list clearfix']/li")
        for li in li_list:
            item["shortdesc"] = li.xpath("./p[@class='l-name']/a/text()").get()
            item["brand"] = item["shortdesc"].split()[0]
            brand_url = li.xpath("./p[@class='l-name']/a/@href").get()
            item["carid"] = re.findall("/\w{2}/(.*?)x.", brand_url)[0] if re.findall("/\w{2}/(.*?)x.",
                                                                                     brand_url) else None
            # is_offsite = li.xpath(".//pan[@class='icon-source2']/text()").get()
            city = li.xpath("./p[@class='l-name']/span/text()").get()
            detail_url = "https://www.chesupai.cn" + brand_url
            item["url"] = detail_url
            # if is_offsite is None:
            for k, v in self.city.items():
                if k in city:
                    self.cityDomain = v
                    self.cookies = {
                        'cityDomain': '{}'.format(self.cityDomain),
                    }
                    self.headers = {
                        'User-agent': "{}".format(self.UserAgent),
                        'cookies': "cityDomain={}".format(self.cityDomain),
                    }
                    break
            # print(self.cityDomain)
            # print(detail_url)
            # print("*"*100)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail_url,
                meta={"item": deepcopy(item)},
                cookies=self.cookies,
                headers=self.headers,
                dont_filter=True
            )
        # 翻页
        next_url_list = response.xpath("//div[@class='pager']/a[@class='']/@href").getall()
        for next_url in next_url_list:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_brand_url,
                meta={"item": deepcopy(item)},
                # cookies=self.cookies,
                # headers=self.headers,
                dont_filter=True
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        item["emission"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[2]/td[4]/text()").get()
        item["mileage"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[1]/td[4]/text()").get()
        item["registerdate"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[1]/td[2]/text()").get()
        item["car_source"] = "carsupai"
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["pagetime"] = "zero"
        item["pagetitle"] = item["shortdesc"]
        item["series"] = item["brand"]
        item["makeyear"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[11]/td[4]/text()").get()
        item["produceyear"] = item["makeyear"]
        item["level"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[12]/td[4]/text()").get()
        try:
            item["bodystyle"] = re.findall('(.*?)厢', item["level"])[0] + "厢" if len(
                re.findall('(.*?)厢', item["level"])) != 0 else None
        except:
            item["bodystyle"] = None
        item["fueltype"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[5]/td[4]/text()").get()
        item["body"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[10]/td[4]/text()").get()

        count = 0
        for k, v in enumerate(item["pagetitle"].split()):
            if '.' in v:
                count += 1
                item["output"] = v
            elif 'TFSI' in v:
                item["output"] = item["pagetitle"].split()[k - 1] + "TFSI"
            if count == 0:
                item["output"] = None
        try:
            item["doors"] = re.findall('(.*?)门', item["body"])[0] if len(
                re.findall('(.*?)门', item["body"])) != 0 else None
        except:
            item["doors"] = None
        item["geartype"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[9]/td[2]/text()").get()
        item["generation"] = item["makeyear"]
        item["usage"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[4]/td[4]/text()").get()
        item["color"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[9]/td[4]/text()").get()
        item["city"] = response.xpath("//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[4]/td[2]/text()").get()
        item["totalcheck_desc"] = response.xpath("//*[@id='base']/div/div[2]/span[1]/text()").get()
        item["totalgrade"] = response.xpath("//*[@id='base']/div/div[1]/p[1]/text()").get()
        item["contact_type"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[5]/td[2]/text()").get()
        item["change_date"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[12]/td[2]/text()").get()
        item["change_times"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[3]/td[2]/text()").get()
        item["insurance1_date"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[7]/td[2]/text()").get()
        item["yearchecktime"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[8]/td[2]/text()").get()

        accident_desc = ''
        name1 = response.xpath(
            '//div[@class="detectBox clearfix"][1]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').getall()
        desc1 = response.xpath(
            '//div[@class="detectBox clearfix"][1]//td/span[contains(@class, "fc-orange")]/text()').getall()
        relt1 = zip(name1, desc1)
        for relt in relt1:
            accident_desc += ''.join(relt) + '/'

        outer_desc = ''
        points = response.xpath('//div[@class="outward fl"]//div[@class="appearance-det"]')
        temp = ['hood', 'fender_fr', 'door_fr', 'door_rr', 'fender_rr', 'trunk_lid',
                'fender_rl', 'door_rl', 'foot_save', 'door_fl', 'head_save', 'fender_fl', 'roof']
        for point in points:
            position_num = int(point.xpath('./i/text()').extract_first())
            position = temp[position_num]
            desc2 = point.xpath('.//p/text()').extract_first()
            outer_desc += position + ': ' + desc2.strip() + ';'

        safe_desc = ''
        name3 = response.xpath(
            '//div[@class="detectBox clearfix"][4]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').getall()
        desc3 = response.xpath(
            '//div[@class="detectBox clearfix"][4]//td/span[contains(@class, "fc-orange")]/text()').getall()
        relt3 = zip(name3, desc3)
        for relt in relt3:
            safe_desc += ''.join(relt) + '/'

        road_desc = ''
        name4 = response.xpath(
            '//div[@class="detectBox clearfix"][position()>4]//td/span[contains(@class, "fc-orange")]/../preceding-sibling::td[1]/text()').getall()
        desc4 = response.xpath(
            '//div[@class="detectBox clearfix"][position()>4]//td/span[contains(@class, "fc-orange")]/text()').getall()
        relt4 = zip(name4, desc4)
        for relt in relt4:
            road_desc += ''.join(relt) + '/'

        item["accident_desc"] = accident_desc
        item["outer_desc"] = outer_desc
        item["safe_desc"] = safe_desc
        item["road_desc"] = road_desc
        item["img_url"] = response.xpath("//ul[@class='slider-pics']/li[1]/img/@src").get()
        item["carno"] = response.xpath(
            "//*[@id='documents_and_procedures']/div[2]/table/tbody/tr[3]/td[4]/text()").get()
        item["desc"] = response.xpath("//*[@id='base']/div/div[1]/p[2]/text()").get()

        carid = item["carid"]
        url = f"http://www.chesupai.cn/ajax/?act=getBidInfo&source_id={carid}"
        yield scrapy.Request(
            url=url,
            callback=self.parse_price,
            meta={"item": deepcopy(item)},
            # cookies=self.cookies,
            # headers=self.headers,
        )

    def parse_price(self, response):
        item = response.meta["item"]
        data = json.loads(response.body)
        try:
            # 当前投标价格
            item["price1"] = data["last_bid"]["amount"]
        except:
            item["price1"] = None
        try:
            # 最后一次投标时间
            item["post_time"] = data["last_bid"]["timeFormat"]
        except:
            item["post_time"] = None
        # yield item
        print(item)
