# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import WeixiuchangBeijingItem
# from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='weixiuchang_beijing'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://www.shanghaiqixiu.org/repair/micro/search/company?fl=pic,type,sid,name,addr,tel,distance,kw,lon,lat,bizScope,brand,category,grade,tag&q=&page=0,4&sort=_score%20desc,distance&point=31.2867,121.50446&fq=status:1+AND+type:164+AND+-kw:4s']

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
        for i in range(1, 189):
            url = "http://weixiu.bjysgl.cn/bjvmpsf/f/trRptRepairEnterprise/list"
            data = {
                "repairType":"汽车维修",
                "pageNo": str(i),
                "pageSize":"20"
            }
            print(data)
            urls.append(scrapy.FormRequest(method="post", url=url, formdata=data))
        return urls

    def parse(self, response):
        changs = response.xpath("//*[@id='contentTable']//tr")
        for chang in changs[1:]:
            code = chang.xpath("td[2]/a/@onclick").re("showDetail\(\'(.*?)\'\)")[0]
            print(code)
            data = {
                "recordId":code
            }
            headers = {
                "User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
            url = "http://weixiu.bjysgl.cn/bjvmpsf/f/trRptRepairEnterprise/detail"
            yield scrapy.FormRequest(method="post", url=url, formdata=data, headers=headers, callback=self.parse_chang)



    def parse_chang(self,response):
        res = json.loads(response.text)["repairEnterprise"]
        item = WeixiuchangBeijingItem()
        item['url'] = response.url
        item['status'] = res["id"]
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['enterpriseName'] = res["enterpriseName"] if "enterpriseName" in res else "-"
        item['jyAddress'] = res["jyAddress"] if "jyAddress" in res else "-"
        item['busNames'] = res["busNames"] if "busNames" in res else "-"
        item['busTel'] = res["busTel"] if "busTel" in res else "-"
        item['id'] = res["id"] if "id" in res else "-"
        item['regionLabel'] = res["regionLabel"] if "regionLabel" in res else "-"
        item['qalLevel'] = res["qalLevel"] if "qalLevel" in res else "-"
        item['pstlNum'] = res["pstlNum"] if "pstlNum" in res else "-"

        # print(item)
        yield item




