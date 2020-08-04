# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import AllProvinceItem
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse
from scrapy.utils.project import get_project_settings
settings = get_project_settings()



website ='all_province_fix'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1']

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
        self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
        super(KoubeiSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self,response):
        ss = response.xpath("//*[@id='ss']/option")
        for s in ss[1:]:
            shengji = s.xpath("text()").extract_first()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
                # 'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
            yield scrapy.FormRequest(url="http://xzqh.mca.gov.cn/selectJson", formdata={"shengji" : shengji}, headers=headers, callback=self.parse_diji, meta={"shengji":shengji})


    def parse_diji(self, response):
        obj = json.loads(response.body)
        for item in obj:
            if item['diji'] != "省直辖县级行政单位":
                shengji = str(urllib.parse.quote(response.meta['shengji'].encode("gb2312")))
                diji = str(urllib.parse.quote(item['diji'].encode("gb2312")))
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'Cookie': 'JSESSIONID=D58506D8BF95AE1AF2A054633360CE5A',
                    'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
                }
                yield scrapy.Request(url="http://xzqh.mca.gov.cn/defaultQuery?shengji=%s&diji=%s&xianji=-1" % (shengji, diji), headers=headers, meta={"shengji":response.meta['shengji'], "diji":item['diji']}, callback=self.parse_list)

    def parse_list(self, response):
        trs = response.xpath("//*[@class='info_table']/tbody/tr")
        print(trs)
        # with open("D:/log.log", "a") as f:
        for tr in trs[1:]:
            # try:
            item = AllProvinceItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + "-" + str(trs.index(tr))
            if trs.index(tr) == 1:
                item['name'] = tr.xpath("td[1]/input[1]/@value").extract_first().strip() if tr.xpath("td[1]/input[1]/@value") else "-"
            else:
                item['name'] = tr.xpath("td[1]/text()").extract_first().strip() if tr.xpath("td[1]/text()") else "-"
            item['location'] = tr.xpath("td[2]/text()").extract_first().strip() if tr.xpath("td[2]/text()") else "-"
            item['population'] = tr.xpath("td[3]/text()").extract_first().strip() if tr.xpath("td[3]/text()") else "-"
            item['area'] = tr.xpath("td[4]/text()").extract_first().strip() if tr.xpath("td[4]/text()") else "-"
            item['code'] = tr.xpath("td[5]/text()").extract_first().strip() if tr.xpath("td[5]/text()") else "-"
            item['district_code'] = tr.xpath("td[6]/text()").extract_first().strip() if tr.xpath("td[6]/text()") else "-"
            item['postcode'] = tr.xpath("td[7]/text()").extract_first().strip() if tr.xpath("td[7]/text()") else "-"
            item['shengji'] = response.meta['shengji']
            item['diji'] = response.meta['diji']
            # except Exception as e:
            #     f.write(str(e))
            #     f.write(response.url)
        # f.close()
        #     yield item
            print(item)


