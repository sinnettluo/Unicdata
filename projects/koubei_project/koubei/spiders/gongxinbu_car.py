# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GongxinbuCarItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests

website='gongxinbu_car_fix'

class CarSpider(scrapy.Spider):

    name=website
    # start_urls = [
    #     "http://www.miit.gov.cn/datainfo/resultSearch?searchType=advancedSearch&categoryTreeId=1128",
    # ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.headers = {
            'User-agent': "User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }

        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        urls = []
        for i in range(1, 69):
            urls.append(scrapy.Request(url="http://www.miit.gov.cn/datainfo/resultSearch?searchType=advancedSearch&categoryTreeId=1128&pagenow=%d" % i, headers=self.headers))
        return urls

    def parse(self, response):

        # next = response.xpath("//*[@aria-label='Next']")
        # if next:
        #     pagenow = next.xpath("@onclick").re("\d+")[0]
        #     url = "http://www.miit.gov.cn/datainfo/resultSearch?searchType=advancedSearch&categoryTreeId=1128&pagenow=%s" % pagenow
        #     yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

        cars = response.xpath("//*[@id='page-wrapper']/div[2]/table/tbody/tr")
        for car in cars:
            url = car.xpath("td[2]/a/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(url), headers=self.headers, callback=self.parse_details)


    def parse_details(self, response):
        item = GongxinbuCarItem()

        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url.split("&")[0]
        item['shangbiao'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[1]/td[1]/text()').extract_first()
        item['xinghao'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[1]/td[2]/text()').extract_first()
        item['mingcheng'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[1]/td[3]/text()').extract_first()
        item['qiyemingcheng'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[2]/td[1]/text()').extract_first()
        item['zhucedizhi'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[2]/td[2]/text()').extract_first()
        item['muluxuhao'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[3]/td[1]/text()').extract_first()
        item['shengchandizhi'] = response.xpath('//*[@class="w_banner"]/table[1]/tr[3]/td[2]/text()').extract_first()
        item['changkuangao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[1]/td/text()').extract_first()
        item['huoxiangchangkuangao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[2]/td/text()').extract_first()
        item['paifangyijubiaozhun'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[3]/td[1]/text()').extract_first()
        item['ranliaozhonglei'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[3]/td[2]/text()').extract_first()
        item['zuigaochesu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[4]/td[1]/text()').extract_first()
        item['zongzhiliang'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[4]/td[2]/text()').extract_first()
        item['zaizhiliangliyongxishu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[5]/td[1]/text()').extract_first()
        item['edingzaizhiliang'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[5]/td[2]/text()').extract_first()
        item['zhuanxiangxingshi'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[6]/td[1]/text()').extract_first()
        item['zhengbeizhiliang'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[6]/td[2]/text()').extract_first()
        item['zhoushu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[7]/td[1]/text()').extract_first()
        item['zhuntuoguachezongzhiliang'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[7]/td[2]/text()').extract_first()
        item['zhouju'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[8]/td[1]/text()').extract_first()
        item['luntaiguige'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[8]/td[2]/text()').extract_first()
        item['gangbantanhuangpianshu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[9]/td[1]/text()').extract_first()
        item['banguacheanzuozuidayunxuchengzaizhiliang'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[9]/td[2]/text()').extract_first()
        item['luntaishu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[10]/td[1]/text()').extract_first()
        item['jiashishizhunchengrenshu'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[10]/td[2]/text()').extract_first()
        item['edingzaike'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[11]/td/text()').extract_first()
        item['lunju'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[12]/td[1]/text()').extract_first()
        item['jiejinjiaoliqujiao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[12]/td[2]/text()').extract_first()
        item['fanguangbiaoshishengchangqiye'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[13]/td[1]/text()').extract_first()
        item['fanguangbiaoshixinghao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[13]/td[2]/text()').extract_first()
        item['fanguangbiaoshishangbiao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[14]/td[1]/text()').extract_first()
        item['fangbaosizhidongxitong'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[14]/td[2]/text()').extract_first()
        item['cheliangshibiedaihao'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[15]/td[1]/text()').extract_first()
        item['qianxuanhouxuan'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[15]/td[2]/text()').extract_first()
        item['qita'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[16]/td/text()').extract_first()
        item['shuoming'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[17]/td/text()').extract_first()
        item['youhaoshenbaozhi'] = response.xpath('//*[@class="w_banner"]/table[2]/tr[18]/td/text()').extract_first()
        item['shifoutongqishenbao'] = response.xpath('//*[@class="w_banner"]/table[3]/tr[2]/td[1]/text()').extract_first()
        item['dipanid'] = response.xpath('//*[@class="w_banner"]/table[3]/tr[2]/td[2]/text()').extract_first()
        item['dipanxinghao'] = response.xpath('//*[@class="w_banner"]/table[3]/tr[2]/td[3]/text()').extract_first()
        item['dipanshengchanqiye'] = response.xpath('//*[@class="w_banner"]/table[3]/tr[2]/td[4]/text()').extract_first()
        item['dipanleibie'] = response.xpath('//*[@class="w_banner"]/table[3]/tr[2]/td[5]/text()').extract_first()
        item['fadongjixinghao'] = response.xpath('//*[@class="w_banner"]/table[4]/tr[2]/td[1]/text()').extract_first()
        item['fadongjiqiye'] = response.xpath('//*[@class="w_banner"]/table[4]/tr[2]/td[2]/text()').extract_first()
        item['pailiang'] = response.xpath('//*[@class="w_banner"]/table[4]/tr[2]/td[3]/text()').extract_first()
        item['gonglv'] = response.xpath('//*[@class="w_banner"]/table[4]/tr[2]/td[4]/text()').extract_first()
        item['youhao'] = response.xpath('//*[@class="w_banner"]/table[4]/tr[2]/td[5]/text()').extract_first()

        # print(item)
        yield item