# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import YicheKoubeiItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from lxml import etree

website ='xcar_koubei_new'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://newcar.xcar.com.cn/price/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 200000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self, response):
        brands = response.xpath("//*[@class='container']/table/tbody/tr")
        for brand in brands:
            brandname = brand.xpath("td[1]/div/a/span/text()").extract_first()
            brandid = brand.xpath("td[1]/@id").re("\d+")[0]
            factories = brand.xpath("td[2]/div[@class='column_content']")
            for factory in factories:
                factoryname = factory.xpath("p/a/text()").extract_first()
                factoryid = factory.xpath("p/a/@href").re("\d+")[0]
                families = factory.xpath("ul/li")
                for family in families:
                    familyname = family.xpath("div/a/@title").extract_first()
                    familyid = family.xpath("div/a/@href").re("\d+")[0]
                    url = family.xpath("div/a/@href").extract_first()
                    meta = {
                        "brandname": brandname,
                        "brandid": brandid,
                        "factoryname": factoryname,
                        "factoryid": factoryid,
                        "familyname": familyname,
                        "familyid": familyid,
                    }
                    yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_model)

    def parse_model(self, response):
        models = response.xpath("//*[@class='table_bord']")
        for model in models:
            modelname = model.xpath("td[1]/p/a/text()").extract_first()
            modelid = model.xpath("td[1]/p/a/@href").re("\d+")[0]
            guideprice = model.xpath("td[3]/a/text()").extract_first().replace(u"万", "").strip() if model.xpath("td[3]/a/text()") else model.xpath("td[3]/span/text()").extract_first()
            url = model.xpath("td[1]/p/a/@href").extract_first() + "review.htm"
            meta = {
                "modelname": modelname,
                "modelid": modelid,
                "guideprice": guideprice,
            }
            meta_merge = dict(meta, **response.meta)
            yield scrapy.Request(url=response.urljoin(url), meta=meta_merge, callback=self.parse_finally)

    def parse_finally(self, response):

        # next = response.xpath("//*[@class='page_down']")
        max_page = int(response.xpath("//*[@class='unify_page mt20']/a[last()-1]/text()").extract_first()) if response.xpath("//*[@class='unify_page mt20']/a[last()-1]/text()") else 1
        # print(max_page)
        for i in range(1, max_page+1):
            url = "http://newcar.xcar.com.cn/auto/index.php?r=reputation/reputation/GetAjaxKbList2&page=%s&mid=%s&jh=0&wd=0" % (i, response.meta["modelid"])
            print(url)
            yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_finally)

        if response.url.find("reputation") > 0:
            selector = etree.HTML(response.text)
            home_lists = selector.xpath("//*[@class='home_list clearfix']")
            for home_list in home_lists:
                item = YicheKoubeiItem()
                item['url'] = response.url
                # website = website
                # status = scrapy.Field()
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                # u_carinfo = scrapy.Field()
                # carinfo = scrapy.Field()
                # userinfo = scrapy.Field()

                item['familyname'] = response.meta["familyname"]
                item['familynameid'] = response.meta["familyid"]
                item['shortdesc'] = response.meta["modelname"]
                item['guideprice'] = response.meta["guideprice"]
                usage = home_list.xpath("div[2]/div[2]/div[2]/div/em")
                usage_list = []
                for u in usage:
                    usage_list.append(u.xpath("text()")[0])
                item['usage'] = "|".join(usage_list)
                # item['fuel'] = scrapy.Field()
                item['buy_date'] = home_list.xpath("div[2]/div[2]/div[1]/div/dl[2]/dd/text()")[0]
                item['buy_location'] = home_list.xpath("div[2]/div[2]/div[1]/div/dl[3]/dd/text()")[0]
                item['buy_pure_price'] = home_list.xpath("div[2]/div[2]/div[1]/div/dl[4]/dd/text()")[0].split(" ")[0]
                # item['buyerid'] = scrapy.Field()
                item['buyername'] = home_list.xpath("div[1]/dl/dd/span/text()")[0]
                # item['comment_detail'] = scrapy.Field()
                # item['comment_people'] = scrapy.Field()
                # item['isGoodComment'] = scrapy.Field()
                # item['mileage'] = scrapy.Field()
                item['oil_consume'] = home_list.xpath("div[2]/div[2]/div[1]/div/dl[5]/dd/text()")[0]
                # item['picurl'] = scrapy.Field()
                item['score'] = home_list.xpath("div[1]/div/div/em/text()")[0]
                # item['score_star'] = scrapy.Field()
                item['score_appearance'] = home_list.xpath("div[1]/div/ul/li[1]/em/text()")[0]
                item['score_appearance_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_1']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_1']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_1']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_1']/dd/text()") else "-")
                item['score_comfort'] = home_list.xpath("div[1]/div/ul/li[4]/em/text()")[0]
                item['score_comfort_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_4']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_4']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_4']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_1']/dd/text()") else "-")
                item['score_control'] = home_list.xpath("div[1]/div/ul/li[7]/em/text()")[0]
                item['score_control_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_7']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_7']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_7']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_7']/dd/text()") else "-")
                item['score_cost'] = home_list.xpath("div[1]/div/ul/li[8]/em/text()")[0]
                item['score_cost_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_8']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_8']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_8']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_8']/dd/text()") else "-")
                item['score_fuel'] = home_list.xpath("div[1]/div/ul/li[5]/em/text()")[0]
                item['score_fuel_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_5']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_5']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_5']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_5']/dd/text()") else "-")
                item['score_power'] = home_list.xpath("div[1]/div/ul/li[6]/em/text()")[0]
                item['score_power_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_6']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_6']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_6']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_6']/dd/text()") else "-")
                item['score_space'] = home_list.xpath("div[1]/div/ul/li[3]/em/text()")[0]
                item['score_space_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_3']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_3']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_3']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_3']/dd/text()") else "-")
                item['score_trim'] = home_list.xpath("div[1]/div/ul/li[2]/em/text()")[0]
                item['score_trim_compare'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_2']/dd/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_2']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_2']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_2']/dd/text()") else "-")
                item['description'] = home_list.xpath("div[2]/div[2]/div[3]/p/text()")[0] if home_list.xpath("div[2]/div[2]/div[3]/p/text()") else "-"
                item['brand'] = response.meta['brandname']
                item['satisfied'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_22']/dd/text()")[0]  if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_22']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_22']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_22']/dd/text()") else "-")
                item['unsatisfied'] = home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_23']/dd/text()")[0]  if home_list.xpath("div[2]/div[3]/div/div[1]/dl[@class='dw_23']/dd/text()") else (home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_23']/dd/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[1]/dl[@class='dw_23']/dd/text()") else "-")

                item['visitCount'] = None
                item['helpfulCount'] = home_list.xpath("div[2]/div[3]/div/div[2]/div/a/text()")[0] if home_list.xpath("div[2]/div[3]/div/div[2]/div/a/text()") else (home_list.xpath("div[2]/div[4]/div/div[2]/div/a/text()")[0] if home_list.xpath("div[2]/div[4]/div/div[2]/div/a/text()") else "-")
                item['commentCount'] = None
                item['post_time'] = home_list.xpath("div[2]/div[1]/text()")[0]
                item['post_time'] = re.findall("\d+\-\d+\-\d+", item['post_time'])[0]
                item['spec_id'] = None

                item['status'] = response.url + "-" + str(home_lists.index(home_list)) + "-" + str(item['visitCount']) + "-" + str(
                    item['helpfulCount']) + "-" + str(item['commentCount'])
                # print(item)
                yield item