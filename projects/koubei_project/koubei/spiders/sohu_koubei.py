# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import SohuKoubeiItem
# from scrapy.conf import settings
from lxml import etree

website ='sohu_koubei_new'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://db.auto.sohu.com/home/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 200000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self, response):
        brands = response.xpath("//*[@class='close_child']")
        for brand in brands:
            brandname = brand.xpath("h4/a/text()[2]").extract_first().strip()
            brandid = brand.xpath("h4/a/@id").extract_first().replace("b", "").strip()
            factories = brand.xpath("ul")
            for factory in factories:
                factoryname = factory.xpath("li[@class='con_tit']/a/text()[2]").extract_first().strip()
                factoryid = factory.xpath("li[@class='con_tit']/a/@id").extract_first().replace("c", "").strip()
                families = factory.xpath("li")
                for family in families[1:]:
                    familyname = family.xpath("a/text()[2]").extract_first().strip()
                    familyid = family.xpath("a/@id").extract_first().replace("m", "").strip()
                    url = response.urljoin(family.xpath("a/@href").extract_first()) + "/dianping.html"
                    # url = "http://db.m.auto.sohu.com/model/%s/microEval/list-more.json?number=20&page=1" % familyid

                    meta = {
                        "brandname": brandname,
                        "brandid": brandid,
                        "factoryname": factoryname,
                        "factoryid": factoryid,
                        "familyname": familyname,
                        "familyid": familyid
                    }
                    # if familyid == "2051":
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_model)

    def parse_model(self, response):
        car_list = response.xpath("//ul[@class='carlist']/li")
        for car in car_list[1:]:
            modelname = car.xpath("span[1]/a/text()").extract_first().strip()
            modelid = car.xpath("span[1]/a/@href").re("\d+")[1]
            meta = {
                "modelname": modelname,
                "modelid": modelid
            }
            url = car.xpath("span[1]/a/@href").extract_first().strip()
            yield scrapy.Request(url=response.urljoin(url), meta=dict(meta, **response.meta), callback=self.parse_koubei)

    def parse_koubei(self, response):

        score = response.xpath("//*[@class='dpcon']/div[2]/h3/span[3]/strong/text()").extract_first().strip()
        waiguan = response.xpath("//*[@class='dpcon']/div[3]/ul/li[1]/a/text()[1]").extract_first().strip()
        neishi = response.xpath("//*[@class='dpcon']/div[3]/ul/li[2]/a/text()[1]").extract_first().strip()
        kongjian = response.xpath("//*[@class='dpcon']/div[3]/ul/li[3]/a/text()[1]").extract_first().strip()
        dongli = response.xpath("//*[@class='dpcon']/div[3]/ul/li[4]/a/text()[1]").extract_first().strip()
        caokong = response.xpath("//*[@class='dpcon']/div[3]/ul/li[5]/a/text()[1]").extract_first().strip()
        youhao = response.xpath("//*[@class='dpcon']/div[3]/ul/li[6]/a/text()[1]").extract_first().strip()
        shushixing = response.xpath("//*[@class='dpcon']/div[3]/ul/li[7]/a/text()[1]").extract_first().strip()
        xingjiabi = response.xpath("//*[@class='dpcon']/div[3]/ul/li[8]/a/text()[1]").extract_first().strip()
        sell_service = response.xpath("//*[@class='dpcon']/div[3]/ul/li[9]/a/text()[1]").extract_first().strip()


        categories = response.xpath("//*[@class='koubei-box']/div/a")
        for category in categories:
            categoryname = category.xpath("text()").extract_first().strip()
            koubei_list = response.xpath("//*[@class='koubeico']/div[%d]/ul/li" % (categories.index(category) + 1))
            for koubei in koubei_list:
                item = SohuKoubeiItem()
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['categoryname'] = categoryname

                item['score'] = score
                item['waiguan'] = waiguan
                item['neishi'] = neishi
                item['kongjian'] = kongjian
                item['dongli'] = dongli
                item['caokong'] = caokong
                item['youhao'] = youhao
                item['shushixing'] = shushixing
                item['xingjiabi'] = xingjiabi
                item['sell_service'] = sell_service
                spans = koubei.xpath("div/div[1]/div/span")
                for span in spans:
                    if span.xpath("text()").extract_first().strip() == u"平均油耗":
                        item['oil_consumption'] = koubei.xpath("div/div[1]/div/text()[%d]" % (spans.index(span) + 2)).extract_first().strip()
                    if span.xpath("text()").extract_first().strip() == u"裸车":
                        item['naked_price'] = koubei.xpath("div/div[1]/div/text()[%d]" % (spans.index(span) + 2)).extract_first().strip()
                item['post_time'] = koubei.xpath("div/div[2]/span/text()").extract_first().strip()
                item['description'] = koubei.xpath("div/p/text()").extract_first().strip()
                item['good_num'] = koubei.xpath("div/div[2]/div/div[1]/span/text()").extract_first().strip()
                item['bad_num'] = koubei.xpath("div/div[2]/div/div[2]/span/text()").extract_first().strip()
                item['brandname'] = response.meta["brandname"]
                item['brandid'] = response.meta["brandid"]
                item['factoryname'] = response.meta["factoryname"]
                item['factoryid'] = response.meta["factoryid"]
                item['familyname'] = response.meta["familyname"]
                item['familyid'] = response.meta["familyid"]
                item['modelname'] = response.meta["modelname"]
                item['modelid'] = response.meta["modelid"]

                item['status'] = item['categoryname'] + "-" + item['modelname'] + "-" + item['oil_consumption'] + "-" + item['naked_price'] + "-" + item['post_time'] + "-" + item['good_num'] + "-" + item['bad_num']
                # print(item)
                yield item








