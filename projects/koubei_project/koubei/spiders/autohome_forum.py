# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import AutohomeForumItem
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse
import pymysql
import requests
# from fontTools.ttLib import TTFont
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

website ='autohome_forum_pasate'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://club.autohome.com.cn/bbs/forum-c-614-1.html?qaType=-1#pvareaid=101061']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

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
        # # 连接数据库
        # db = pymysql.connect("192.168.1.94", "root", "Datauser@2017", "people_zb")
        # # 使用cursor()方法创建一个游标对象
        # cursor = db.cursor()
        # # 使用execute()方法执行SQL语句
        # cursor.execute("SELECT distinct(vin) FROM chinacar_vin")
        # # 使用fetall()获取全部数据
        # vins = cursor.fetchall()
        for i in range(1000):
            pageindex = i+1
            url = "https://club.autohome.com.cn/bbs/forum-c-528-%d.html" % pageindex
            yield scrapy.FormRequest(url=url, headers=self.headers)

    def parse(self, response):
        # print(response.text)
        dls = response.xpath("//dl[@class='list_dl']")
        # print(len(dls))
        for dl in dls:
            try:
                url = dl.xpath("dt/a/@href").extract_first()
                title = dl.xpath("dt/a/text()").extract_first().strip()
                meta = {
                    "title":title
                }
                yield scrapy.Request(url=response.urljoin(url), meta=meta, headers=self.headers, callback=self.parse_content)
            except Exception as e:
                pass

    def parse_content(self, response):
        # # 匹配ttf font
        # cmp = re.compile(",url\('(//.*.ttf)'\) format\('woff'\)")
        # rst = cmp.findall(response.text)
        # ttf = requests.get("http:" + rst[0], stream=True)
        # with open("autohome.ttf", "wb") as pdf:
        #     for chunk in ttf.iter_content(chunk_size=1024):
        #         if chunk:
        #             pdf.write(chunk)
        # # 解析字体库font文件
        # font = TTFont('autohome.ttf')
        # uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        # utf8List = [eval("u'\\u" + uni[3:] + "'") for uni in uniList[1:]]

        item = AutohomeForumItem()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['url'] = response.url
        item['status'] = response.url + "_0"
        item['title'] = response.meta["title"]
        item['username'] = response.xpath("//*[@id='maxwrap-maintopic']/div[2]/div[2]/ul[1]/li[1]/a[1]/text()").extract_first().strip()
        item['posttime'] = response.xpath("//*[@id='maxwrap-maintopic']/div[2]/div[3]/div[1]/span[2]/text()").extract_first().strip()
        item['content'] = response.xpath("//*[@class='tz-paragraph']").extract_first()
        pre = re.compile('>(.*?)<')
        try:
            item['content'] = ''.join(pre.findall(item['content']))
        except Exception as e:
            item['content'] = ""
        # for i in range(len(utf8List)):
        #     item['content'] = item['content'].replace(utf8List[i], str(utf8List[i].encode("utf-8"), "utf-8"))
        item['userid'] = response.xpath("//*[@id='maxwrap-maintopic']/div[2]/div[2]/ul[1]/li[1]/a[1]/@href").re("\d+")[0]

        # print(item)
        yield item

        replies = response.xpath("//*[@id='maxwrap-reply']/div[@class='clearfix contstxt outer-section']")
        for reply in replies:
            item = AutohomeForumItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['status'] = response.url + str(replies.index(reply)+ 1)
            item['title'] = response.meta["title"]
            item['username'] = reply.xpath("div[1]/ul[1]/li[1]/a[1]/text()").extract_first().strip()
            item['posttime'] = reply.xpath("div[2]/div/div[1]/span[2]").extract_first().strip()
            item['content'] = reply.xpath(".//div[@xname='content']").extract_first()
            pre = re.compile('>(.*?)<')
            try:
                item['content'] = ''.join(pre.findall(item['content']))
            except Exception as e:
                item['content'] = ""
            # for i in range(len(utf8List)):
            #     item['content'] = item['content'].replace(utf8List[i], str(utf8List[i].encode("utf-8"), "utf-8"))
            item['userid'] = reply.xpath("div[1]/ul[1]/li[1]/a[1]/@href").extract_first().strip()

            print(item)
            # yield item


