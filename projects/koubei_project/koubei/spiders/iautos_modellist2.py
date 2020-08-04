# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import IautosModelItem
# from scrapy.conf import settings

website ='iautos_modellist2_fixed2'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['https://www.iautos.cn/chexing/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 200000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')


    def start_requests(self):
        for i in range(1, 200001):
        # for i in range(200001, 300001):
            url = "http://www.iautos.cn/chexing/trim.asp?id=%d" % i
            yield scrapy.Request(url=url)

    def parse(self, response):
        # print(response.text)
        item = IautosModelItem()

        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = response.url

        # item['unicdatakey'] = response.xpath("")
        # item['brandname'] = response.xpath("")
        item['factoryname'] = response.xpath("//*[@id='bread']/text()[3]").extract_first().replace(">", "").replace("<", "").strip()
        item['familyname'] = response.xpath("//*[@id='bread']/a[3]/text()").extract_first().strip()
        # item['brandid']
        # item['factoryid']
        item['familyid'] = response.xpath("//*[@id='bread']/a[3]/@href").re("\d+")[0]
        item['makeyear'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][1]/div/table/tr[3]/td[2]/text()").extract_first().strip()
        # item['output'] =
        item['geartype'] = response.xpath("//*[@class='mainRight']/div[6]/div/table/tr[1]/td[2]/text()").extract_first().strip()
        item['salesdesc'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][1]/div/table/tr[1]/td[2]/text()").extract_first().strip()
        item['price'] = response.xpath("//*[@class='mainRight']/div[1]/div[2]/div[1]/ul[1]/li[1]/b/text()").extract_first().strip()
        # item['saleyear']
        # item['salemonth']
        item['produceyear'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][1]/div/table/tr[2]/td[2]/text()").extract_first().strip()
        # item['stopyear']
        # item['producestatus']
        # item['bigtype']
        # item['type']
        # item['level']
        # item['nation']
        # item['property']
        item['accelerate'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[1]/td[4]/text()").extract_first().strip()
        item['masspeed'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[1]/td[2]/text()").extract_first().strip()
        item['carstructure'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[1]/td[2]/text()").extract_first().strip()
        item['length'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[1]/td[4]/text()").extract_first().strip().split("/")[0]
        item['width'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[1]/td[4]/text()").extract_first().strip().split("/")[1]
        item['height'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[1]/td[4]/text()").extract_first().strip().split("/")[2]
        item['wheelbase'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[3]/td[2]/text()").extract_first().strip()
        try:
            item['frontgauge'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[2]/td[2]/text()").extract_first().strip().split("/")[0]
            item['backgauge'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[2]/td[2]/text()").extract_first().strip().split("/")[1]
        except Exception as e:
            item['frontgauge'] = "-"
            item['backgauge'] = "-"
        item['weight'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[4]/td[2]/text()").extract_first().strip()
        # item['maxload']
        item['fuelvolumn'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[5]/td[2]/text()").extract_first().strip()
        item['baggage'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[6]/td[2]/text()").extract_first().strip()
        item['doors'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[7]/td[2]/text()").extract_first().strip()
        # item['seats']
        # item['emission']
        # item['cylinder']
        # item['fueltype']
        # item['lwv']
        # item['maxrpm']
        # item['maxps']
        # item['maxtorque']
        # item['motor_type']
        # item['total_power_EV']
        # item['total_torque_EV']
        # item['front_peak_power_EV']
        # item['front_peak_torque_EV']
        # item['rear_peak_power_EV']
        # item['rear_peak_torque_EV']
        # item['vehicle_power']
        # item['vehicle_torque']
        # item['battery_type']
        # item['battery_range_MIIT']
        # item['battery_capacity']
        # item['power_consumption']
        # item['battery_pack_warrenty']
        # item['charging_time']
        # item['fast_charge_electricity']
        # item['charging_pile_price']
        item['geardesc'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[5]/td[2]/text()").extract_first().strip()
        # item['gearnumber']
        item['driveway'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[2]/td[2]/text()").extract_first().strip()
        item['fronthang'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[3]/td[2]/text()").extract_first().strip()
        item['backhang'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[3]/td[4]/text()").extract_first().strip()
        # item['assistanttype']
        # item['steeringbox']
        item['frontbrake'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[4]/td[2]/text()").extract_first().strip()
        item['backbrake'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[4]/td[4]/text()").extract_first().strip()
        item['frontwheel'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[6]/td[2]/text()").extract_first().strip()
        item['backwheel'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[6]/td[4]/text()").extract_first().strip()
        # item['fronthub']
        # item['backhub']
        # item['hubtype']
        item['sparewheel'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[7]/td[2]/text()").extract_first().strip()
        # item['bn']
        # item['bo']
        # item['bq']
        # item['br']
        # item['bs']
        # item['bp']
        # item['bt']
        # item['bu']
        # item['bv']
        # item['bw']
        # item['bx']
        # item['by']
        # item['cd']
        # item['ce']
        # item['cf']
        # item['cg']
        # item['ch']
        # item['cn']
        # item['co']
        # item['fw']
        # item['ga']
        # item['fz']
        # item['fy']
        # item['fv']
        # item['eu']
        # item['ci']
        # item['cj']
        # item['ck']
        # item['cl']
        # item['cm']
        item['cp'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[2]/td[4]/text()").extract_first().strip()
        # item['dy']
        # item['dz']
        # item['dw']
        # item['dx']
        # item['dv']
        # item['bz']
        # item['ca']
        # item['cb']
        # item['cc']
        # item['ev']
        # item['et']
        # item['cq']
        # item['cr']
        # item['cs']
        # item['ct']
        # item['cu']
        # item['cv']
        # item['ex']
        # item['ew']
        # item['cw']
        # item['cx']
        # item['cy']
        # item['cz']
        # item['da']
        # item['db']
        # item['dc']
        # item['dd']
        # item['de']
        # item['df']
        # item['dg']
        # item['dh']
        # item['di']
        # item['dj']
        # item['dk']
        # item['dl']
        # item['dm']
        # item['dn']
        # item['do']
        # item['dp']
        # item['dq']
        # item['ey']
        # item['ez']
        # item['fa']
        # item['fx']
        # item['fd']
        # item['fb']
        # item['gb']
        # item['fe']
        # item['ff']
        # item['fc']
        # item['fk']
        # item['fl']
        # item['fm']
        # item['fg']
        # item['fh']
        # item['fi']
        # item['fj']
        # item['fn']
        # item['ea']
        # item['eb']
        # item['ec']
        # item['ed']
        # item['ee']
        # item['ef']
        # item['eg']
        # item['eh']
        # item['dr']
        # item['ei']
        # item['ej']
        # item['ek']
        # item['el']
        # item['em']
        # item['en']
        # item['ep']
        # item['eq']
        # item['ds']
        # item['dt']
        # item['du']
        # item['eo']
        # item['er']
        # item['es']
        # item['fo']
        # item['fp']
        # item['fq']
        # item['fr']
        # item['fs']
        # item['ft']
        # item['fu']
        # item['exterior_color']
        # item['interior_color']
        # item['factory_brand_info']
        # item['vin_factory_brand']
        # item['vin_makeyear']
        # item['vin_fvs']
        # item['Price_low']
        # item['vin_price']
        # item['vin_config']
        # item['vin_otherconfig']
        # item['car_source']
        # item['sourceid']
        # item['sourcefactoryid']
        # item['sourcebrandid']
        # item['sourcefamilyid']
        # item['status']
        # item['note']
        # item['vw']

        item['enginedesc'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[2]/td[2]/text()").extract_first().strip()
        item['enginenumber'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[3]/td[2]/text()").extract_first().strip()
        item['shenggonglv'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[4]/td[2]/text()").extract_first().strip()
        item['compress'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[5]/td[2]/text()").extract_first().strip()
        item['xingcheng'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[6]/td[2]/text()").extract_first().strip()
        item['valve'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[7]/td[2]/text()").extract_first().strip()
        item['maxpower'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[8]/td[2]/text()").extract_first().strip()
        item['fuelnumber'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[9]/td[2]/text()").extract_first().strip()
        item['output'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[10]/td[2]/text()").extract_first().strip()
        item['enginedirection'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[11]/td[2]/text()").extract_first().strip()
        item['method'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[12]/td[2]/text()").extract_first().strip()

        item['engineproducer'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[3]/td[4]/text()").extract_first().strip()
        item['petrol'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[4]/td[4]/text()").extract_first().strip()
        item['gangjing'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[5]/td[4]/text()").extract_first().strip()
        item['ganggaicailiao'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[6]/td[4]/text()").extract_first().strip()
        item['gangticailiao'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[7]/td[4]/text()").extract_first().strip()
        item['maxnm'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[8]/td[4]/text()").extract_first().strip()
        item['fuelmethod'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[9]/td[4]/text()").extract_first().strip()
        item['lwvnumber'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[10]/td[4]/text()").extract_first().strip()
        item['engineposition'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[11]/td[4]/text()").extract_first().strip()
        item['lengquexitong'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][3]/div/table/tr[12]/td[4]/text()").extract_first().strip()
        item['qianlungucailiao'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[8]/td[2]/text()").extract_first().strip()
        item['qudongluntaikuandu'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[9]/td[2]/text()").extract_first().strip()
        item['qudongluntaifuhezhishu'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[10]/td[2]/text()").extract_first().strip()
        item['qudonglunguzhijing'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[11]/td[2]/text()").extract_first().strip()
        item['paidangfangshi'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[1]/td[4]/text()").extract_first().strip()
        item['zhengchepingtai'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[5]/td[4]/text()").extract_first().strip()
        item['beitailungucailiao'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[7]/td[4]/text()").extract_first().strip()
        item['houlungucailiao'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[8]/td[4]/text()").extract_first().strip()
        item['qudongluntaibianpingbi'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[9]/td[4]/text()").extract_first().strip()
        item['qudongluntaisudujibie'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][4]/div/table/tr[10]/td[4]/text()").extract_first().strip()
        item['zuidapapodu'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[2]/td[2]/text()").extract_first().strip()
        item['baoxiuqi'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[3]/td[2]/text()").extract_first().strip()
        item['anquanqinang'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[2]/td[4]/text()").extract_first().strip()
        item['zhidongjuli'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][5]/div/table/tr[3]/td[4]/text()").extract_first().strip()
        item['chengyuanshu'] = response.xpath("//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[7]/td[4]/text()").extract_first().strip()

        item['jiejinjiao'] = response.xpath(
            "//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[8]/td[2]/text()").extract_first().strip()
        item['liqujiao'] = response.xpath(
            "//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[8]/td[4]/text()").extract_first().strip()
        item['zuidazongzhiliang'] = response.xpath(
            "//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[4]/td[4]/text()").extract_first().strip()
        item['zuidaxinglixiangrongji'] = response.xpath(
            "//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[6]/td[4]/text()").extract_first().strip()
        item['fengzuxishu'] = response.xpath(
            "//*[@class='mainRight']/div[contains(@class, 'jbxx')][2]/div/table/tr[3]/td[4]/text()").extract_first().strip()

        yield item
        # print(item)