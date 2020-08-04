# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import VinSearchItem
# from scrapy.conf import self.settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse
import pymysql

website ='vin_search'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://www.shanghaiqixiu.org/repair/micro/search/company?fl=pic,type,sid,name,addr,tel,distance,kw,lon,lat,bizScope,brand,category,grade,tag&q=&page=0,4&sort=_score%20desc,distance&point=31.2867,121.50446&fq=status:1+AND+type:164+AND+-kw:4s']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=self.settings['PHANTOMJS_PATH'])

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
        # 连接数据库
        db = pymysql.connect("192.168.1.94", "root", "Datauser@2017", "people_zb")
        # 使用cursor()方法创建一个游标对象
        cursor = db.cursor()
        # 使用execute()方法执行SQL语句
        cursor.execute("SELECT distinct(vin) FROM chinacar_vin")
        # 使用fetall()获取全部数据
        vins = cursor.fetchall()

        for vin in vins:
            data = {
                "leftvin": vin[0][:8],
                "rightvin": vin[0][9:],
            }
            url = "http://www.chinacar.com.cn/vin_index.html"
            meta =  {
                "o_vin":vin[0],
            }
            headers = {
                "Referer": "http://www.chinacar.com.cn/vin_index.html",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            }
            cookies = {
                "vin_cookie": "6663",
                "relv":"1"
            }
            yield scrapy.FormRequest(url=url, method="post",formdata=data, meta=meta, dont_filter=True, headers=headers, cookies=cookies)

    def parse(self, response):
        # print(response.text)
        vin = response.xpath("//*[@class='searchresult-color']/p/text()").extract_first() + response.xpath("//*[@class='searchresult-color']/p/font/text()").extract_first() + response.xpath("//*[@class='searchresult-color']/p/text()[2]").extract_first()
        vin = vin.replace("您查询到的VIN码是： ", "")
        trs = response.xpath("//*[@class='table-list']/tr")
        for tr in trs[1:]:
            car = tr.xpath("td[1]/a/text()").extract_first()
            car_url = tr.xpath("td[1]/a/@href").extract_first()
            dipan = tr.xpath("td[2]/text()").extract_first()
            fadongji = tr.xpath("td[3]/text()").extract_first()
            shengchanshang = tr.xpath("td[4]/text()").extract_first()
            pailiang = tr.xpath("td[5]/text()").extract_first()
            gonglv = tr.xpath("td[6]/text()").extract_first()
            ranshao = tr.xpath("td[7]/text()").extract_first()
            zhoushu = tr.xpath("td[8]/text()").extract_first()
            pici = tr.xpath("td[9]/text()").extract_first()
            meta = {
                "car":car,
                "car_url": car_url,
                "dipan": dipan,
                "fadongji": fadongji,
                "shengchanshang": shengchanshang,
                "pailiang": pailiang,
                "gonglv": gonglv,
                "ranshao": ranshao,
                "zhoushu": zhoushu,
                "pici": pici,
                "vin":vin,
                "o_vin":response.meta["o_vin"]
            }
            yield scrapy.Request(url=response.urljoin(car_url), callback=self.parse_report, meta=meta)

    def parse_report(self, response):
        item = VinSearchItem()
        item['r_carname'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[2]/td[2]/a/text()').extract_first()
        item['r_cartype'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[2]/td[4]/span[1]/a/text()').extract_first()
        item['r_location'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[3]/td[2]/text()').extract_first()
        item['r_numtype'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[3]/td[4]/text()').extract_first()
        item['r_pici'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[4]/td[2]/text()').extract_first()
        item['r_date'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[4]/td[4]/text()').extract_first()
        item['r_chanpinhao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[5]/td[2]/span/text()').extract_first()
        item['r_muluxuhao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[5]/td[4]/text()').extract_first()
        item['r_brandcn'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[6]/td[2]/a/text()').extract_first()
        item['r_branden'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[6]/td[3]/text()').extract_first()
        item['r_noticetype'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[7]/td[2]/text()').extract_first()
        item['r_mianzheng'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[7]/td[4]/text()').extract_first()
        item['r_companyname'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[8]/td[2]/text()').extract_first()
        item['r_ranyou'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[8]/td[4]/text()').extract_first()
        item['r_companyaddress'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[9]/td[2]/text()').extract_first()
        item['r_huanbao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[9]/td[3]/text()').extract_first()
        item['r_mianjian'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[11]/td[2]/text()').extract_first()
        item['r_mianjiandate'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[11]/td[4]/text()').extract_first()
        item['r_noticestatus'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[13]/td[2]/text()').extract_first()
        item['r_noticedate'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[13]/td[4]/text()').extract_first()
        item['r_noticestatusmiaoshu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[14]/td[2]/text()').extract_first()
        item['r_noticechange'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[14]/td[4]/text()').extract_first()
        item['r_waixingchicun'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[16]/td[2]/span/text()').extract_first()
        item['r_huoxiangchicun'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[16]/td[4]/span/text()').extract_first()
        item['r_weight'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[17]/td[2]/span/text()').extract_first()
        item['r_zaizhiliangliyongxishu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[17]/td[4]/text()').extract_first()
        item['r_zhengbeishiliang'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[18]/td[2]/span/text()').extract_first()
        item['r_edingzaizhiliang'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[18]/td[4]/span/text()').extract_first()
        item['r_guachezhiliang'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[19]/td[2]/text()').extract_first()
        item['r_banguaanzuo'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[19]/td[4]/text()').extract_first()
        item['r_jiashishi'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[20]/td[2]/text()').extract_first()
        item['r_qianpaichengke'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[20]/td[4]/text()').extract_first()
        item['r_edingzaike'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[21]/td[2]/text()').extract_first()
        item['r_abs'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[21]/td[4]/text()').extract_first()
        item['r_jiejinjiao_liqujiao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[22]/td[2]/text()').extract_first()
        item['r_qianxuan_houxuan'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[22]/td[4]/span/text()').extract_first()
        item['r_zhouhe'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[23]/td[2]/text()').extract_first()
        item['r_zhouju'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[23]/td[4]/span/text()').extract_first()
        item['r_zhoushu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[24]/td[2]/text()').extract_first()
        item['r_zuigaochesu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[24]/td[4]/text()').extract_first()
        item['r_youhao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[25]/td[2]/text()').extract_first()
        item['r_tanhuangpianshu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[25]/td[4]/text()').extract_first()
        item['r_luntaishu'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[26]/td[2]/text()').extract_first()
        item['r_luntaiguige'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[26]/td[4]/text()').extract_first()
        item['r_qianlunju'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[27]/td[2]/span/text()').extract_first()
        item['r_houlunju'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[27]/td[4]/text()').extract_first()
        item['r_zhidongqian'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[28]/td[2]/text()').extract_first()
        item['r_zhidonghou'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[28]/td[4]/text()').extract_first()
        item['r_caozuoqian'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[29]/td[2]/text()').extract_first()
        item['r_caozuohou'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[29]/td[4]/text()').extract_first()
        item['r_zhuanxiangxingshi'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[30]/td[2]/text()').extract_first()
        item['r_qidongfangshi'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[30]/td[4]/text()').extract_first()
        item['r_chuandongxingshi'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[31]/td[2]/text()').extract_first()
        item['r_vin'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[32]/td[2]/span[1]/text()').extract_first()
        item['r_fadongji'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[35]/td[1]/text()').extract_first()
        item['r_shengchangqiye'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[35]/td[2]/text()').extract_first()
        item['r_pailiang'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[35]/td[3]/text()').extract_first()
        item['r_gonglv'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[35]/td[4]/text()').extract_first()
        item['r_ranyouzhonglei'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[37]/td[2]/text()').extract_first()
        item['r_yijubiaozhun'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[37]/td[4]/span/text()').extract_first()
        item['r_dipanpaifangbiaozhun'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[38]/td[2]/text()').extract_first()
        item['r_others'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[40]/td/text()').extract_first()
        item['r_biaoshiqiye'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[42]/td[2]/text()').extract_first()
        item['r_biaoshishangbiao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[42]/td[4]/text()').extract_first()
        item['r_biaoshixinghao'] = response.xpath('//*[@class="parameter_box_s"]/table/tr[43]/td[2]/text()').extract_first()

        item['r_carname'] = response.xpath('//*[@id="table"]/table/tr[2]/td[2]/a/text()').extract_first() if not item["r_carname"] else item["r_carname"]
        item['r_cartype'] = response.xpath(
            '//*[@id="table"]/table/tr[2]/td[4]/span[1]/a/text()').extract_first() if not item["r_cartype"] else item["r_cartype"]
        item['r_location'] = response.xpath('//*[@id="table"]/table/tr[3]/td[2]/text()').extract_first() if not item["r_location"] else item["r_location"]
        item['r_numtype'] = response.xpath('//*[@id="table"]/table/tr[3]/td[4]/text()').extract_first() if not item["r_numtype"] else item["r_numtype"]
        item['r_pici'] = response.xpath('//*[@id="table"]/table/tr[4]/td[2]/text()').extract_first() if not item["r_pici"] else item["r_pici"]
        item['r_date'] = response.xpath('//*[@id="table"]/table/tr[4]/td[4]/text()').extract_first() if not item["r_date"] else item["r_date"]
        item['r_chanpinhao'] = response.xpath(
            '//*[@id="table"]/table/tr[5]/td[2]/span/text()').extract_first() if not item["r_chanpinhao"] else item["r_chanpinhao"]
        item['r_muluxuhao'] = response.xpath('//*[@id="table"]/table/tr[5]/td[4]/text()').extract_first() if not item["r_muluxuhao"] else item["r_muluxuhao"]
        item['r_brandcn'] = response.xpath('//*[@id="table"]/table/tr[6]/td[2]/a/text()').extract_first() if not item["r_brandcn"] else item["r_brandcn"]
        item['r_branden'] = response.xpath('//*[@id="table"]/table/tr[6]/td[3]/text()').extract_first() if not item["r_branden"] else item["r_branden"]
        item['r_noticetype'] = response.xpath('//*[@id="table"]/table/tr[7]/td[2]/text()').extract_first() if not item["r_noticetype"] else item["r_noticetype"]
        item['r_mianzheng'] = response.xpath('//*[@id="table"]/table/tr[7]/td[4]/text()').extract_first() if not item["r_mianzheng"] else item["r_mianzheng"]
        item['r_companyname'] = response.xpath('//*[@id="table"]/table/tr[8]/td[2]/text()').extract_first() if not item["r_companyname"] else item["r_companyname"]
        item['r_ranyou'] = response.xpath('//*[@id="table"]/table/tr[8]/td[4]/text()').extract_first() if not item["r_ranyou"] else item["r_ranyou"]
        item['r_companyaddress'] = response.xpath(
            '//*[@id="table"]/table/tr[9]/td[2]/text()').extract_first() if not item["r_companyaddress"] else item["r_companyaddress"]
        item['r_huanbao'] = response.xpath('//*[@id="table"]/table/tr[9]/td[3]/text()').extract_first() if not item["r_huanbao"] else item["r_huanbao"]
        item['r_mianjian'] = response.xpath('//*[@id="table"]/table/tr[11]/td[2]/text()').extract_first() if not item["r_mianjian"] else item["r_mianjian"]
        item['r_mianjiandate'] = response.xpath(
            '//*[@id="table"]/table/tr[11]/td[4]/text()').extract_first() if not item["r_mianjiandate"] else item["r_mianjiandate"]
        item['r_noticestatus'] = response.xpath(
            '//*[@id="table"]/table/tr[13]/td[2]/text()').extract_first() if not item["r_noticestatus"] else item["r_noticestatus"]
        item['r_noticedate'] = response.xpath('//*[@id="table"]/table/tr[13]/td[4]/text()').extract_first() if not item["r_noticedate"] else item["r_noticedate"]
        item['r_noticestatusmiaoshu'] = response.xpath(
            '//*[@id="table"]/table/tr[14]/td[2]/text()').extract_first() if not item["r_noticestatusmiaoshu"] else item["r_noticestatusmiaoshu"]
        item['r_noticechange'] = response.xpath(
            '//*[@id="table"]/table/tr[14]/td[4]/text()').extract_first() if not item["r_noticechange"] else item["r_noticechange"]
        item['r_waixingchicun'] = response.xpath(
            '//*[@id="table"]/table/tr[16]/td[2]/span/text()').extract_first() if not item["r_waixingchicun"] else item["r_waixingchicun"]
        item['r_huoxiangchicun'] = response.xpath(
            '//*[@id="table"]/table/tr[16]/td[4]/span/text()').extract_first() if not item["r_huoxiangchicun"] else item["r_huoxiangchicun"]
        item['r_weight'] = response.xpath(
            '//*[@id="table"]/table/tr[17]/td[2]/span/text()').extract_first() if not item["r_weight"] else item["r_weight"]
        item['r_zaizhiliangliyongxishu'] = response.xpath(
            '//*[@id="table"]/table/tr[17]/td[4]/text()').extract_first() if not item["r_zaizhiliangliyongxishu"] else item["r_zaizhiliangliyongxishu"]
        item['r_zhengbeishiliang'] = response.xpath(
            '//*[@id="table"]/table/tr[18]/td[2]/span/text()').extract_first() if not item["r_zhengbeishiliang"] else item["r_zhengbeishiliang"]
        item['r_edingzaizhiliang'] = response.xpath(
            '//*[@id="table"]/table/tr[18]/td[4]/span/text()').extract_first() if not item["r_edingzaizhiliang"] else item["r_edingzaizhiliang"]
        item['r_guachezhiliang'] = response.xpath(
            '//*[@id="table"]/table/tr[19]/td[2]/text()').extract_first() if not item["r_guachezhiliang"] else item["r_guachezhiliang"]
        item['r_banguaanzuo'] = response.xpath(
            '//*[@id="table"]/table/tr[19]/td[4]/text()').extract_first() if not item["r_banguaanzuo"] else item["r_banguaanzuo"]
        item['r_jiashishi'] = response.xpath('//*[@id="table"]/table/tr[20]/td[2]/text()').extract_first() if not item["r_jiashishi"] else item["r_jiashishi"]
        item['r_qianpaichengke'] = response.xpath(
            '//*[@id="table"]/table/tr[20]/td[4]/text()').extract_first() if not item["r_qianpaichengke"] else item["r_qianpaichengke"]
        item['r_edingzaike'] = response.xpath('//*[@id="table"]/table/tr[21]/td[2]/text()').extract_first() if not item["r_edingzaike"] else item["r_edingzaike"]
        item['r_abs'] = response.xpath('//*[@id="table"]/table/tr[21]/td[4]/text()').extract_first() if not item["r_abs"] else item["r_abs"]
        item['r_jiejinjiao_liqujiao'] = response.xpath(
            '//*[@id="table"]/table/tr[22]/td[2]/text()').extract_first() if not item["r_jiejinjiao_liqujiao"] else item["r_jiejinjiao_liqujiao"]
        item['r_qianxuan_houxuan'] = response.xpath(
            '//*[@id="table"]/table/tr[22]/td[4]/span/text()').extract_first() if not item["r_qianxuan_houxuan"] else item["r_qianxuan_houxuan"]
        item['r_zhouhe'] = response.xpath('//*[@id="table"]/table/tr[23]/td[2]/text()').extract_first() if not item["r_zhouhe"] else item["r_zhouhe"]
        item['r_zhouju'] = response.xpath(
            '//*[@id="table"]/table/tr[23]/td[4]/span/text()').extract_first() if not item["r_zhouju"] else item["r_zhouju"]
        item['r_zhoushu'] = response.xpath('//*[@id="table"]/table/tr[24]/td[2]/text()').extract_first() if not item["r_zhoushu"] else item["r_zhoushu"]
        item['r_zuigaochesu'] = response.xpath(
            '//*[@id="table"]/table/tr[24]/td[4]/text()').extract_first() if not item["r_zuigaochesu"] else item["r_zuigaochesu"]
        item['r_youhao'] = response.xpath('//*[@id="table"]/table/tr[25]/td[2]/text()').extract_first() if not item["r_youhao"] else item["r_youhao"]
        item['r_tanhuangpianshu'] = response.xpath(
            '//*[@id="table"]/table/tr[25]/td[4]/text()').extract_first() if not item["r_tanhuangpianshu"] else item["r_tanhuangpianshu"]
        item['r_luntaishu'] = response.xpath('//*[@id="table"]/table/tr[26]/td[2]/text()').extract_first() if not item["r_luntaishu"] else item["r_luntaishu"]
        item['r_luntaiguige'] = response.xpath(
            '//*[@id="table"]/table/tr[26]/td[4]/text()').extract_first() if not item["r_luntaiguige"] else item["r_luntaiguige"]
        item['r_qianlunju'] = response.xpath(
            '//*[@id="table"]/table/tr[27]/td[2]/span/text()').extract_first() if not item["r_qianlunju"] else item["r_qianlunju"]
        item['r_houlunju'] = response.xpath('//*[@id="table"]/table/tr[27]/td[4]/text()').extract_first() if not item["r_houlunju"] else item["r_houlunju"]
        item['r_zhidongqian'] = response.xpath(
            '//*[@id="table"]/table/tr[28]/td[2]/text()').extract_first() if not item["r_zhidongqian"] else item["r_zhidongqian"]
        item['r_zhidonghou'] = response.xpath('//*[@id="table"]/table/tr[28]/td[4]/text()').extract_first() if not item["r_zhidonghou"] else item["r_zhidonghou"]
        item['r_caozuoqian'] = response.xpath('//*[@id="table"]/table/tr[29]/td[2]/text()').extract_first() if not item["r_caozuoqian"] else item["r_caozuoqian"]
        item['r_caozuohou'] = response.xpath('//*[@id="table"]/table/tr[29]/td[4]/text()').extract_first() if not item["r_caozuohou"] else item["r_caozuohou"]
        item['r_zhuanxiangxingshi'] = response.xpath(
            '//*[@id="table"]/table/tr[30]/td[2]/text()').extract_first() if not item["r_zhuanxiangxingshi"] else item["r_zhuanxiangxingshi"]
        item['r_qidongfangshi'] = response.xpath(
            '//*[@id="table"]/table/tr[30]/td[4]/text()').extract_first() if not item["r_qidongfangshi"] else item["r_qidongfangshi"]
        item['r_chuandongxingshi'] = response.xpath(
            '//*[@id="table"]/table/tr[31]/td[2]/text()').extract_first() if not item["r_chuandongxingshi"] else item["r_chuandongxingshi"]
        item['r_vin'] = response.xpath(
            '//*[@id="table"]/table/tr[32]/td[2]/span[1]/text()').extract_first() if not item["r_vin"] else item["r_vin"]
        item['r_fadongji'] = response.xpath('//*[@id="table"]/table/tr[35]/td[1]/text()').extract_first() if not item["r_fadongji"] else item["r_fadongji"]
        item['r_shengchangqiye'] = response.xpath(
            '//*[@id="table"]/table/tr[35]/td[2]/text()').extract_first() if not item["r_shengchangqiye"] else item["r_shengchangqiye"]
        item['r_pailiang'] = response.xpath('//*[@id="table"]/table/tr[35]/td[3]/text()').extract_first() if not item["r_pailiang"] else item["r_pailiang"]
        item['r_gonglv'] = response.xpath('//*[@id="table"]/table/tr[35]/td[4]/text()').extract_first() if not item["r_gonglv"] else item["r_gonglv"]
        item['r_ranyouzhonglei'] = response.xpath(
            '//*[@id="table"]/table/tr[37]/td[2]/text()').extract_first() if not item["r_ranyouzhonglei"] else item["r_ranyouzhonglei"]
        item['r_yijubiaozhun'] = response.xpath(
            '//*[@id="table"]/table/tr[37]/td[4]/span/text()').extract_first() if not item["r_yijubiaozhun"] else item["r_yijubiaozhun"]
        item['r_dipanpaifangbiaozhun'] = response.xpath(
            '//*[@id="table"]/table/tr[38]/td[2]/text()').extract_first() if not item["r_dipanpaifangbiaozhun"] else item["r_dipanpaifangbiaozhun"]
        item['r_others'] = response.xpath('//*[@id="table"]/table/tr[40]/td/text()').extract_first() if not item["r_others"] else item["r_others"]
        item['r_biaoshiqiye'] = response.xpath(
            '//*[@id="table"]/table/tr[42]/td[2]/text()').extract_first() if not item["r_biaoshiqiye"] else item["r_biaoshiqiye"]
        item['r_biaoshishangbiao'] = response.xpath(
            '//*[@id="table"]/table/tr[42]/td[4]/text()').extract_first() if not item["r_biaoshishangbiao"] else item["r_biaoshishangbiao"]
        item['r_biaoshixinghao'] = response.xpath(
            '//*[@id="table"]/table/tr[43]/td[2]/text()').extract_first() if not item["r_biaoshixinghao"] else item["r_biaoshixinghao"]

        item['r_carname'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[2]/td[2]/a/text()').extract_first() if not item[
            "r_carname"] else item["r_carname"]
        item['r_cartype'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[2]/td[4]/span[1]/a/text()').extract_first() if not item["r_cartype"] else item[
            "r_cartype"]
        item['r_location'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[3]/td[2]/text()').extract_first() if not item[
            "r_location"] else item["r_location"]
        item['r_numtype'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[3]/td[4]/text()').extract_first() if not item[
            "r_numtype"] else item["r_numtype"]
        item['r_pici'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[4]/td[2]/text()').extract_first() if not item[
            "r_pici"] else item["r_pici"]
        item['r_date'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[4]/td[4]/text()').extract_first() if not item[
            "r_date"] else item["r_date"]
        item['r_chanpinhao'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[5]/td[2]/span/text()').extract_first() if not item["r_chanpinhao"] else item[
            "r_chanpinhao"]
        item['r_muluxuhao'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[5]/td[4]/text()').extract_first() if not item[
            "r_muluxuhao"] else item["r_muluxuhao"]
        item['r_brandcn'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[6]/td[2]/a/text()').extract_first() if not item[
            "r_brandcn"] else item["r_brandcn"]
        item['r_branden'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[6]/td[3]/text()').extract_first() if not item[
            "r_branden"] else item["r_branden"]
        item['r_noticetype'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[7]/td[2]/text()').extract_first() if not item[
            "r_noticetype"] else item["r_noticetype"]
        item['r_mianzheng'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[7]/td[4]/text()').extract_first() if not item[
            "r_mianzheng"] else item["r_mianzheng"]
        item['r_companyname'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[8]/td[2]/text()').extract_first() if not item[
            "r_companyname"] else item["r_companyname"]
        item['r_ranyou'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[8]/td[4]/text()').extract_first() if not item[
            "r_ranyou"] else item["r_ranyou"]
        item['r_companyaddress'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[9]/td[2]/text()').extract_first() if not item["r_companyaddress"] else item[
            "r_companyaddress"]
        item['r_huanbao'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[9]/td[3]/text()').extract_first() if not item[
            "r_huanbao"] else item["r_huanbao"]
        item['r_mianjian'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[11]/td[2]/text()').extract_first() if not item[
            "r_mianjian"] else item["r_mianjian"]
        item['r_mianjiandate'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[11]/td[4]/text()').extract_first() if not item["r_mianjiandate"] else item[
            "r_mianjiandate"]
        item['r_noticestatus'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[13]/td[2]/text()').extract_first() if not item["r_noticestatus"] else item[
            "r_noticestatus"]
        item['r_noticedate'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[13]/td[4]/text()').extract_first() if not item[
            "r_noticedate"] else item["r_noticedate"]
        item['r_noticestatusmiaoshu'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[14]/td[2]/text()').extract_first() if not item["r_noticestatusmiaoshu"] else \
        item["r_noticestatusmiaoshu"]
        item['r_noticechange'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[14]/td[4]/text()').extract_first() if not item["r_noticechange"] else item[
            "r_noticechange"]
        item['r_waixingchicun'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[16]/td[2]/span/text()').extract_first() if not item["r_waixingchicun"] else item[
            "r_waixingchicun"]
        item['r_huoxiangchicun'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[16]/td[4]/span/text()').extract_first() if not item["r_huoxiangchicun"] else \
        item["r_huoxiangchicun"]
        item['r_weight'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[17]/td[2]/span/text()').extract_first() if not item["r_weight"] else item[
            "r_weight"]
        item['r_zaizhiliangliyongxishu'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[17]/td[4]/text()').extract_first() if not item["r_zaizhiliangliyongxishu"] else \
        item["r_zaizhiliangliyongxishu"]
        item['r_zhengbeishiliang'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[18]/td[2]/span/text()').extract_first() if not item["r_zhengbeishiliang"] else \
        item["r_zhengbeishiliang"]
        item['r_edingzaizhiliang'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[18]/td[4]/span/text()').extract_first() if not item["r_edingzaizhiliang"] else \
        item["r_edingzaizhiliang"]
        item['r_guachezhiliang'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[19]/td[2]/text()').extract_first() if not item["r_guachezhiliang"] else item[
            "r_guachezhiliang"]
        item['r_banguaanzuo'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[19]/td[4]/text()').extract_first() if not item["r_banguaanzuo"] else item[
            "r_banguaanzuo"]
        item['r_jiashishi'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[20]/td[2]/text()').extract_first() if not item[
            "r_jiashishi"] else item["r_jiashishi"]
        item['r_qianpaichengke'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[20]/td[4]/text()').extract_first() if not item["r_qianpaichengke"] else item[
            "r_qianpaichengke"]
        item['r_edingzaike'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[21]/td[2]/text()').extract_first() if not item[
            "r_edingzaike"] else item["r_edingzaike"]
        item['r_abs'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[21]/td[4]/text()').extract_first() if not item[
            "r_abs"] else item["r_abs"]
        item['r_jiejinjiao_liqujiao'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[22]/td[2]/text()').extract_first() if not item["r_jiejinjiao_liqujiao"] else \
        item["r_jiejinjiao_liqujiao"]
        item['r_qianxuan_houxuan'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[22]/td[4]/span/text()').extract_first() if not item["r_qianxuan_houxuan"] else \
        item["r_qianxuan_houxuan"]
        item['r_zhouhe'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[23]/td[2]/text()').extract_first() if not item[
            "r_zhouhe"] else item["r_zhouhe"]
        item['r_zhouju'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[23]/td[4]/span/text()').extract_first() if not item["r_zhouju"] else item[
            "r_zhouju"]
        item['r_zhoushu'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[24]/td[2]/text()').extract_first() if not item[
            "r_zhoushu"] else item["r_zhoushu"]
        item['r_zuigaochesu'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[24]/td[4]/text()').extract_first() if not item["r_zuigaochesu"] else item[
            "r_zuigaochesu"]
        item['r_youhao'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[25]/td[2]/text()').extract_first() if not item[
            "r_youhao"] else item["r_youhao"]
        item['r_tanhuangpianshu'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[25]/td[4]/text()').extract_first() if not item["r_tanhuangpianshu"] else item[
            "r_tanhuangpianshu"]
        item['r_luntaishu'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[26]/td[2]/text()').extract_first() if not item[
            "r_luntaishu"] else item["r_luntaishu"]
        item['r_luntaiguige'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[26]/td[4]/text()').extract_first() if not item["r_luntaiguige"] else item[
            "r_luntaiguige"]
        item['r_qianlunju'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[27]/td[2]/span/text()').extract_first() if not item["r_qianlunju"] else item[
            "r_qianlunju"]
        item['r_houlunju'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[27]/td[4]/text()').extract_first() if not item[
            "r_houlunju"] else item["r_houlunju"]
        item['r_zhidongqian'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[28]/td[2]/text()').extract_first() if not item["r_zhidongqian"] else item[
            "r_zhidongqian"]
        item['r_zhidonghou'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[28]/td[4]/text()').extract_first() if not item[
            "r_zhidonghou"] else item["r_zhidonghou"]
        item['r_caozuoqian'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[29]/td[2]/text()').extract_first() if not item[
            "r_caozuoqian"] else item["r_caozuoqian"]
        item['r_caozuohou'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[29]/td[4]/text()').extract_first() if not item[
            "r_caozuohou"] else item["r_caozuohou"]
        item['r_zhuanxiangxingshi'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[30]/td[2]/text()').extract_first() if not item["r_zhuanxiangxingshi"] else item[
            "r_zhuanxiangxingshi"]
        item['r_qidongfangshi'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[30]/td[4]/text()').extract_first() if not item["r_qidongfangshi"] else item[
            "r_qidongfangshi"]
        item['r_chuandongxingshi'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[31]/td[2]/text()').extract_first() if not item["r_chuandongxingshi"] else item[
            "r_chuandongxingshi"]
        item['r_vin'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[32]/td[2]/span[1]/text()').extract_first() if not item["r_vin"] else item[
            "r_vin"]
        item['r_fadongji'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[35]/td[1]/text()').extract_first() if not item[
            "r_fadongji"] else item["r_fadongji"]
        item['r_shengchangqiye'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[35]/td[2]/text()').extract_first() if not item["r_shengchangqiye"] else item[
            "r_shengchangqiye"]
        item['r_pailiang'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[35]/td[3]/text()').extract_first() if not item[
            "r_pailiang"] else item["r_pailiang"]
        item['r_gonglv'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[35]/td[4]/text()').extract_first() if not item[
            "r_gonglv"] else item["r_gonglv"]
        item['r_ranyouzhonglei'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[37]/td[2]/text()').extract_first() if not item["r_ranyouzhonglei"] else item[
            "r_ranyouzhonglei"]
        item['r_yijubiaozhun'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[37]/td[4]/span/text()').extract_first() if not item["r_yijubiaozhun"] else item[
            "r_yijubiaozhun"]
        item['r_dipanpaifangbiaozhun'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[38]/td[2]/text()').extract_first() if not item["r_dipanpaifangbiaozhun"] else \
        item["r_dipanpaifangbiaozhun"]
        item['r_others'] = response.xpath('//*[@id="p_dhArrCon_1"]/table/tr[40]/td/text()').extract_first() if not item[
            "r_others"] else item["r_others"]
        item['r_biaoshiqiye'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[42]/td[2]/text()').extract_first() if not item["r_biaoshiqiye"] else item[
            "r_biaoshiqiye"]
        item['r_biaoshishangbiao'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[42]/td[4]/text()').extract_first() if not item["r_biaoshishangbiao"] else item[
            "r_biaoshishangbiao"]
        item['r_biaoshixinghao'] = response.xpath(
            '//*[@id="p_dhArrCon_1"]/table/tr[43]/td[2]/text()').extract_first() if not item["r_biaoshixinghao"] else item[
            "r_biaoshixinghao"]

        item['car'] = response.meta['car']
        item['car_url'] = response.meta['car_url']
        item['dipan'] = response.meta['dipan']
        item['fadongji'] = response.meta['fadongji']
        item['shengchanshang'] = response.meta['shengchanshang']
        item['pailiang'] = response.meta['pailiang']
        item['gonglv'] = response.meta['gonglv']
        item['ranshao'] = response.meta['ranshao']
        item['zhoushu'] = response.meta['zhoushu']
        item['pici'] = response.meta['pici']
        item['vin'] = response.meta['vin']
        item['o_vin'] = response.meta['o_vin']

        item['url'] = response.url
        item['status'] = response.url + time.strftime('%Y-%m', time.localtime())
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # print(item)
        yield item





