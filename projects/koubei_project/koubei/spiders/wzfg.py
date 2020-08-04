# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import WzfgItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='wzfg'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
        # self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        # super(KoubeiSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def start_requests(self):
        urls = []
        for i in range(143):
            url = "http://www.wzfg.com/realweb/stat/ProjectSellingList.jsp?currPage=%d" % i
            urls.append(scrapy.Request(url=url))
        return urls

    def parse(self,response):
        trs = response.xpath("/html/body/table[1]/tr/td/table[3]/tr")[1:]
        for tr in trs:
            url = re.findall("window.open\(\'(.*?)\'\)", tr.xpath("@onclick").extract_first(), re.S)[0]
            yield scrapy.Request(url=response.urljoin("http://www.wzfg.com/realweb/stat/" + url), callback=self.parse_room)

    def parse_room(self, response):
        hrefs = response.xpath("//*[@class='G1']")
        for href in hrefs:
            url = "HouseInfoUser5.jsp?houseID=%s" % href.xpath("@id").extract_first().replace("R", "")
            yield scrapy.Request(url=response.urljoin("http://www.wzfg.com/realweb/stat/" + url), callback=self.parse_detail)

    def parse_detail(self, response):
        item = WzfgItem()
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['district'] = response.xpath("/html/body/form/table[2]/tr[1]/td[2]/text()").extract_first()
        item['example'] = response.xpath("/html/body/form/table[2]/tr[1]/td[4]/text()").extract_first()
        item['location'] = response.xpath("/html/body/form/table[2]/tr[2]/td[2]/text()").extract_first()
        item['houseId'] = response.url.split("=")[1]
        item['room'] = response.xpath("/html/body/form/table[2]/tr[3]/td[2]/text()").extract_first()
        item['zong_area'] = response.xpath("/html/body/form/table[2]/tr[3]/td[4]/text()").extract_first()
        item['taonei_area'] = response.xpath("/html/body/form/table[2]/tr[4]/td[2]/text()").extract_first()
        item['fentan_area'] = response.xpath("/html/body/form/table[2]/tr[4]/td[4]/text()").extract_first()
        item['type'] = response.xpath("/html/body/form/table[2]/tr[5]/td[2]/text()").extract_first()
        item['usage'] = response.xpath("/html/body/form/table[2]/tr[5]/td[4]/text()").extract_first()
        item['constructure'] = response.xpath("/html/body/form/table[2]/tr[6]/td[2]/text()").extract_first()
        item['unit'] = response.xpath("/html/body/form/table[2]/tr[6]/td[4]/text()").extract_first()
        item['projectId'] = response.xpath("/html/body/form/table[2]/tr[7]/td[2]/a/@onclick").re("\d+")[0]
        item['project_name'] = response.xpath("/html/body/form/table[2]/tr[7]/td[2]/a/text()").extract_first()
        item['kaifashang'] = response.xpath("/html/body/form/table[2]/tr[7]/td[4]/a/text()").extract_first()
        item['room_status'] = response.xpath("/html/body/form/table[2]/tr[8]/td[2]/text()").extract_first()
        yield item



