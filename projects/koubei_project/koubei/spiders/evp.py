# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import GEVItem
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
import pymongo
import os

website='evp_fix2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        self.category = {
            "7":"国家补贴",
            "2": "地方补贴",
            "1": "推广政策",
            "3": "充电桩补贴政策",
            "4": "充电价格政策",
            "9": "路权政策",
            "8": "充电设施建设规划",
            "10": "网约车政策",
            "5": "国外政策",
            "6": "其它政策",
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

        location = {}
        location[0] = {}
        location[1] = {}
        location[2] = {}
        location[0][2] = ['上海', '0', 'S']
        location[0][3] = ['北京', '0', 'B']
        location[0][5] = ['天津', '0', 'T']
        location[1][36] = ['广州', '17', 'G']
        location[1][38] = ['深圳', '17', 'S']
        location[1][110] = ['上海市', '2', 'S']
        location[1][131] = ['北京市', '3', 'B']
        location[0][4] = ['重庆', '0', 'C']
        location[0][6] = ['河北', '0', 'H']
        location[0][7] = ['山西', '0', 'S']
        location[0][8] = ['内蒙古', '0', 'N']
        location[0][9] = ['黑龙江', '0', 'H']
        location[0][10] = ['吉林', '0', 'J']
        location[0][11] = ['辽宁', '0', 'L']
        location[0][12] = ['山东', '0', 'S']
        location[0][13] = ['江苏', '0', 'J']
        location[0][14] = ['浙江', '0', 'Z']
        location[0][15] = ['安徽', '0', 'A']
        location[0][16] = ['福建', '0', 'F']
        location[0][17] = ['广东', '0', 'G']
        location[0][18] = ['广西', '0', 'G']
        location[0][19] = ['海南', '0', 'H']
        location[0][20] = ['河南', '0', 'H']
        location[0][21] = ['湖北', '0', 'H']
        location[0][22] = ['湖南', '0', 'H']
        location[0][23] = ['江西', '0', 'J']
        location[0][24] = ['四川', '0', 'S']
        location[0][25] = ['云南', '0', 'Y']
        location[0][26] = ['贵州', '0', 'G']
        location[0][27] = ['西藏', '0', 'X']
        location[0][28] = ['宁夏', '0', 'N']
        location[0][29] = ['新疆', '0', 'X']
        location[0][30] = ['青海', '0', 'Q']
        location[0][31] = ['陕西', '0', 'S']
        location[0][32] = ['甘肃', '0', 'G']
        location[0][33] = ['香港', '0', 'X']
        location[0][34] = ['澳门', '0', 'A']
        location[0][35] = ['台湾', '0', 'T']
        location[1][37] = ['韶关', '17', 'S']
        location[1][39] = ['珠海', '17', 'Z']
        location[1][40] = ['汕头', '17', 'S']
        location[1][41] = ['佛山', '17', 'F']
        location[1][42] = ['江门', '17', 'J']
        location[1][43] = ['湛江', '17', 'Z']
        location[1][44] = ['茂名', '17', 'M']
        location[1][45] = ['肇庆', '17', 'Z']
        location[1][46] = ['惠州', '17', 'H']
        location[1][47] = ['梅州', '17', 'M']
        location[1][48] = ['汕尾', '17', 'S']
        location[1][49] = ['河源', '17', 'H']
        location[1][50] = ['阳江', '17', 'Y']
        location[1][51] = ['清远', '17', 'Q']
        location[1][52] = ['东莞', '17', 'D']
        location[1][53] = ['中山', '17', 'Z']
        location[1][54] = ['潮州', '17', 'C']
        location[1][55] = ['揭阳', '17', 'J']
        location[1][56] = ['云浮', '17', 'Y']
        location[1][76] = ['南京', '13', 'N']
        location[1][77] = ['无锡', '13', 'W']
        location[1][78] = ['徐州', '13', 'X']
        location[1][79] = ['常州', '13', 'C']
        location[1][80] = ['苏州', '13', 'S']
        location[1][81] = ['南通', '13', 'N']
        location[1][82] = ['连云港', '13', 'L']
        location[1][83] = ['淮安', '13', 'H']
        location[1][84] = ['盐城', '13', 'Y']
        location[1][85] = ['扬州', '13', 'Y']
        location[1][86] = ['镇江', '13', 'Z']
        location[1][87] = ['泰州', '13', 'T']
        location[1][88] = ['宿迁', '13', 'S']
        location[1][151] = ['重庆市', '4', 'C']
        location[1][193] = ['天津市', '5', 'T']
        location[1][212] = ['石家庄', '6', 'S']
        location[1][213] = ['唐山', '6', 'T']
        location[1][214] = ['秦皇岛', '6', 'Q']
        location[1][215] = ['邯郸', '6', 'H']
        location[1][216] = ['邢台', '6', 'X']
        location[1][217] = ['保定', '6', 'B']
        location[1][218] = ['张家口', '6', 'Z']
        location[1][219] = ['承德', '6', 'C']
        location[1][220] = ['沧州', '6', 'C']
        location[1][221] = ['廊坊', '6', 'L']
        location[1][222] = ['衡水', '6', 'H']
        location[1][398] = ['太原', '7', 'T']
        location[1][399] = ['大同', '7', 'D']
        location[1][400] = ['阳泉', '7', 'Y']
        location[1][401] = ['长治', '7', 'C']
        location[1][402] = ['晋城', '7', 'J']
        location[1][403] = ['朔州', '7', 'S']
        location[1][404] = ['晋中', '7', 'J']
        location[1][405] = ['运城', '7', 'Y']
        location[1][406] = ['忻州', '7', 'X']
        location[1][407] = ['临汾', '7', 'L']
        location[1][408] = ['吕梁', '7', 'L']
        location[1][528] = ['呼和浩特', '8', 'H']
        location[1][529] = ['包头', '8', 'B']
        location[1][530] = ['乌海', '8', 'W']
        location[1][531] = ['赤峰', '8', 'C']
        location[1][532] = ['通辽', '8', 'T']
        location[1][533] = ['鄂尔多斯', '8', 'E']
        location[1][534] = ['呼伦贝尔', '8', 'H']
        location[1][535] = ['巴彦淖尔', '8', 'B']
        location[1][536] = ['乌兰察布', '8', 'W']
        location[1][537] = ['兴安盟', '8', 'X']
        location[1][538] = ['锡林郭勒盟', '8', 'X']
        location[1][539] = ['阿拉善盟', '8', 'A']
        location[1][641] = ['哈尔滨', '9', 'H']
        location[1][642] = ['齐齐哈尔', '9', 'Q']
        location[1][643] = ['鸡西', '9', 'J']
        location[1][644] = ['鹤岗', '9', 'H']
        location[1][645] = ['双鸭山', '9', 'S']
        location[1][646] = ['大庆', '9', 'D']
        location[1][647] = ['伊春', '9', 'Y']
        location[1][648] = ['佳木斯', '9', 'J']
        location[1][649] = ['七台河', '9', 'Q']
        location[1][650] = ['牡丹江', '9', 'M']
        location[1][651] = ['黑河', '9', 'H']
        location[1][652] = ['绥化', '9', 'S']
        location[1][653] = ['大兴安岭地区', '9', 'D']
        location[1][785] = ['长春', '10', 'C']
        location[1][786] = ['吉林', '10', 'J']
        location[1][787] = ['四平', '10', 'S']
        location[1][788] = ['辽源', '10', 'L']
        location[1][789] = ['通化', '10', 'T']
        location[1][790] = ['白山', '10', 'B']
        location[1][791] = ['松原', '10', 'S']
        location[1][792] = ['白城', '10', 'B']
        location[1][793] = ['延边朝鲜族自治州', '10', 'Y']
        location[1][858] = ['沈阳', '11', 'S']
        location[1][859] = ['大连', '11', 'D']
        location[1][860] = ['鞍山', '11', 'A']
        location[1][861] = ['抚顺', '11', 'F']
        location[1][862] = ['本溪', '11', 'B']
        location[1][863] = ['丹东', '11', 'D']
        location[1][864] = ['锦州', '11', 'J']
        location[1][865] = ['营口', '11', 'Y']
        location[1][866] = ['阜新', '11', 'F']
        location[1][867] = ['辽阳', '11', 'L']
        location[1][868] = ['盘锦', '11', 'P']
        location[1][869] = ['铁岭', '11', 'T']
        location[1][870] = ['朝阳', '11', 'C']
        location[1][871] = ['葫芦岛', '11', 'H']
        location[1][978] = ['济南', '12', 'J']
        location[1][979] = ['青岛', '12', 'Q']
        location[1][980] = ['淄博', '12', 'Z']
        location[1][981] = ['枣庄', '12', 'Z']
        location[1][982] = ['东营', '12', 'D']
        location[1][983] = ['烟台', '12', 'Y']
        location[1][984] = ['潍坊', '12', 'W']
        location[1][985] = ['济宁', '12', 'J']
        location[1][986] = ['泰安', '12', 'T']
        location[1][987] = ['威海', '12', 'W']
        location[1][988] = ['日照', '12', 'R']
        location[1][989] = ['莱芜', '12', 'L']
        location[1][990] = ['临沂', '12', 'L']
        location[1][991] = ['德州', '12', 'D']
        location[1][992] = ['聊城', '12', 'L']
        location[1][993] = ['滨州', '12', 'B']
        location[1][994] = ['菏泽', '12', 'H']
        location[1][1230] = ['杭州', '14', 'H']
        location[1][1231] = ['宁波', '14', 'N']
        location[1][1232] = ['温州', '14', 'W']
        location[1][1233] = ['嘉兴', '14', 'J']
        location[1][1234] = ['湖州', '14', 'H']
        location[1][1235] = ['绍兴', '14', 'S']
        location[1][1236] = ['金华', '14', 'J']
        location[1][1237] = ['衢州', '14', 'Q']
        location[1][1238] = ['舟山', '14', 'Z']
        location[1][1239] = ['台州', '14', 'T']
        location[1][1240] = ['丽水', '14', 'L']
        location[1][1331] = ['合肥', '15', 'H']
        location[1][1332] = ['芜湖', '15', 'W']
        location[1][1333] = ['蚌埠', '15', 'B']
        location[1][1334] = ['淮南', '15', 'H']
        location[1][1335] = ['马鞍山', '15', 'M']
        location[1][1336] = ['淮北', '15', 'H']
        location[1][1337] = ['铜陵', '15', 'T']
        location[1][1338] = ['安庆', '15', 'A']
        location[1][1339] = ['黄山', '15', 'H']
        location[1][1340] = ['滁州', '15', 'C']
        location[1][1341] = ['阜阳', '15', 'F']
        location[1][1342] = ['宿州', '15', 'S']
        location[1][1343] = ['巢湖', '15', 'C']
        location[1][1344] = ['六安', '15', 'L']
        location[1][1345] = ['毫州', '15', 'H']
        location[1][1346] = ['池州', '15', 'C']
        location[1][1347] = ['宣城', '15', 'X']
        location[1][1616] = ['福州', '16', 'F']
        location[1][1617] = ['厦门', '16', 'F']
        location[1][1618] = ['莆田', '16', 'P']
        location[1][1619] = ['三明', '16', 'S']
        location[1][1620] = ['泉州', '16', 'Q']
        location[1][1621] = ['漳州', '16', 'Z']
        location[1][1622] = ['南平', '16', 'N']
        location[1][1623] = ['龙岩', '16', 'L']
        location[1][1624] = ['宁德', '16', 'N']
        location[1][1710] = ['南宁', '18', 'N']
        location[1][1711] = ['柳州', '18', 'L']
        location[1][1712] = ['桂林', '18', 'G']
        location[1][1713] = ['梧州', '18', 'W']
        location[1][1714] = ['北海', '18', 'B']
        location[1][1715] = ['防城港', '18', 'F']
        location[1][1716] = ['钦州', '18', 'Q']
        location[1][1717] = ['贵港', '18', 'G']
        location[1][1718] = ['玉林', '18', 'Y']
        location[1][1719] = ['百色', '18', 'B']
        location[1][1720] = ['贺州', '18', 'H']
        location[1][1721] = ['河池', '18', 'H']
        location[1][1722] = ['来宾', '18', 'L']
        location[1][1723] = ['崇左', '18', 'C']
        location[1][1833] = ['海口', '19', 'H']
        location[1][1834] = ['三亚', '19', 'S']
        location[1][1835] = ['五指山', '19', 'W']
        location[1][1836] = ['琼海', '19', 'Q']
        location[1][1837] = ['儋州', '19', 'D']
        location[1][1838] = ['文昌', '19', 'W']
        location[1][1839] = ['万宁', '19', 'W']
        location[1][1840] = ['东方', '19', 'D']
        location[1][1841] = ['定安县', '19', 'D']
        location[1][1842] = ['屯昌县', '19', 'T']
        location[1][1843] = ['澄迈县', '19', 'C']
        location[1][1844] = ['临高县', '19', 'L']
        location[1][1845] = ['白沙黎族自治县', '19', 'B']
        location[1][1846] = ['昌江黎族自治县', '19', 'C']
        location[1][1847] = ['乐东黎族自治县', '19', 'L']
        location[1][1848] = ['陵水黎族自治县', '19', 'L']
        location[1][1849] = ['保亭黎族苗族自治县', '19', 'B']
        location[1][1850] = ['琼中黎族苗族自治县', '19', 'Q']
        location[1][1851] = ['西南中沙群岛办事处', '19', 'X']
        location[1][2038] = ['郑州', '20', 'Z']
        location[1][2039] = ['开封', '20', 'K']
        location[1][2040] = ['洛阳', '20', 'L']
        location[1][2041] = ['平顶山', '20', 'P']
        location[1][2042] = ['安阳', '20', 'A']
        location[1][2043] = ['鹤壁', '20', 'H']
        location[1][2044] = ['新乡', '20', 'X']
        location[1][2045] = ['焦作', '20', 'J']
        location[1][2046] = ['济源', '20', 'J']
        location[1][2047] = ['濮阳', '20', 'P']
        location[1][2048] = ['许昌', '20', 'X']
        location[1][2049] = ['漯河', '20', 'L']
        location[1][2050] = ['三门峡', '20', 'S']
        location[1][2051] = ['南阳', '20', 'N']
        location[1][2052] = ['商丘', '20', 'S']
        location[1][2053] = ['信阳', '20', 'X']
        location[1][2054] = ['周口', '20', 'Z']
        location[1][2055] = ['驻马店', '20', 'Z']
        location[1][2218] = ['武汉', '21', 'W']
        location[1][2219] = ['黄石', '21', 'H']
        location[1][2220] = ['十堰', '21', 'S']
        location[1][2221] = ['宜昌', '21', 'Y']
        location[1][2222] = ['襄阳', '21', 'X']
        location[1][2223] = ['鄂州', '21', 'E']
        location[1][2224] = ['荆门', '21', 'J']
        location[1][2225] = ['孝感', '21', 'X']
        location[1][2226] = ['荆州', '21', 'J']
        location[1][2227] = ['黄冈', '21', 'H']
        location[1][2228] = ['咸宁', '21', 'X']
        location[1][2229] = ['随州', '21', 'S']
        location[1][2230] = ['恩施土家族苗族自治州', '21', 'E']
        location[1][2231] = ['仙桃', '21', 'X']
        location[1][2232] = ['潜江', '21', 'Q']
        location[1][2233] = ['天门', '21', 'T']
        location[1][2234] = ['神农架林区', '21', 'S']
        location[1][2341] = ['香港岛', '33', 'X']
        location[1][2342] = ['九龙', '33', 'J']
        location[1][2343] = ['新界', '33', 'X']
        location[1][2362] = ['澳门半岛', '34', 'A']
        location[1][2363] = ['离岛', '34', 'L']
        location[1][2366] = ['台北市', '35', 'T']
        location[1][2367] = ['高雄市', '35', 'G']
        location[1][2368] = ['台南市', '35', 'T']
        location[1][2369] = ['台中市', '35', 'T']
        location[1][2370] = ['金门县', '35', 'J']
        location[1][2371] = ['南投县', '35', 'N']
        location[1][2372] = ['基隆市', '35', 'J']
        location[1][2373] = ['新竹市', '35', 'X']
        location[1][2374] = ['嘉义市', '35', 'J']
        location[1][2375] = ['台北县', '35', 'T']
        location[1][2376] = ['宜兰县', '35', 'Y']
        location[1][2377] = ['新竹县', '35', 'X']
        location[1][2378] = ['桃园县', '35', 'T']
        location[1][2379] = ['苗栗县', '35', 'M']
        location[1][2380] = ['台中县', '35', 'T']
        location[1][2381] = ['彰化县', '35', 'Z']
        location[1][2382] = ['嘉义县', '35', 'J']
        location[1][2383] = ['云林县', '35', 'Y']
        location[1][2384] = ['台南县', '35', 'T']
        location[1][2385] = ['高雄县', '35', 'G']
        location[1][2386] = ['屏东县', '35', 'P']
        location[1][2387] = ['台东县', '35', 'T']
        location[1][2388] = ['花莲县', '35', 'H']
        location[1][2389] = ['澎湖县', '35', 'P']
        location[1][2703] = ['长沙', '22', 'C']
        location[1][2704] = ['株洲', '22', 'Z']
        location[1][2705] = ['湘潭', '22', 'X']
        location[1][2706] = ['衡阳', '22', 'H']
        location[1][2707] = ['邵阳', '22', 'S']
        location[1][2708] = ['岳阳', '22', 'Y']
        location[1][2709] = ['常德', '22', 'C']
        location[1][2710] = ['张家界', '22', 'Z']
        location[1][2711] = ['益阳', '22', 'Y']
        location[1][2712] = ['郴州', '22', 'C']
        location[1][2713] = ['永州', '22', 'Y']
        location[1][2714] = ['怀化', '22', 'H']
        location[1][2715] = ['娄底', '22', 'L']
        location[1][2716] = ['湘西土家族苗族自治州', '22', 'X']
        location[1][2839] = ['南昌', '23', 'N']
        location[1][2840] = ['景德镇', '23', 'J']
        location[1][2841] = ['萍乡', '23', 'P']
        location[1][2842] = ['九江', '23', 'J']
        location[1][2843] = ['新余', '23', 'X']
        location[1][2844] = ['鹰潭', '23', 'Y']
        location[1][2845] = ['赣州', '23', 'G']
        location[1][2846] = ['吉安', '23', 'J']
        location[1][2847] = ['宜春', '23', 'Y']
        location[1][2848] = ['抚州', '23', 'F']
        location[1][2849] = ['上饶', '23', 'S']
        location[1][2953] = ['成都', '24', 'C']
        location[1][2954] = ['自贡', '24', 'Z']
        location[1][2955] = ['攀枝花', '24', 'P']
        location[1][2956] = ['泸州', '24', 'L']
        location[1][2957] = ['德阳', '24', 'D']
        location[1][2958] = ['绵阳', '24', 'M']
        location[1][2959] = ['广元', '24', 'G']
        location[1][2960] = ['遂宁', '24', 'S']
        location[1][2961] = ['内江', '24', 'N']
        location[1][2962] = ['乐山', '24', 'L']
        location[1][2963] = ['南充', '24', 'N']
        location[1][2964] = ['眉山', '24', 'M']
        location[1][2965] = ['宜宾', '24', 'Y']
        location[1][2966] = ['广安', '24', 'G']
        location[1][2967] = ['达州', '24', 'D']
        location[1][2968] = ['雅安', '24', 'Y']
        location[1][2969] = ['巴中', '24', 'B']
        location[1][2970] = ['资阳', '24', 'Z']
        location[1][2971] = ['阿坝藏族羌族自治州', '24', 'A']
        location[1][2972] = ['甘孜藏族自治州', '24', 'G']
        location[1][2973] = ['凉山彝族自治州', '24', 'L']
        location[1][3157] = ['昆明', '25', 'K']
        location[1][3158] = ['曲靖', '25', 'Q']
        location[1][3159] = ['玉溪', '25', 'Y']
        location[1][3160] = ['保山', '25', 'B']
        location[1][3161] = ['昭通', '25', 'Z']
        location[1][3162] = ['丽江', '25', 'L']
        location[1][3163] = ['普洱', '25', 'P']
        location[1][3164] = ['临沧', '25', 'L']
        location[1][3165] = ['楚雄彝族自治州', '25', 'C']
        location[1][3166] = ['红河哈尼族彝族自治州', '25', 'H']
        location[1][3167] = ['文山壮族苗族自治州', '25', 'W']
        location[1][3168] = ['西双版纳傣族自治州', '25', 'X']
        location[1][3169] = ['大理白族自治州', '25', 'D']
        location[1][3170] = ['德宏傣族景颇族自治州', '25', 'D']
        location[1][3171] = ['怒江傈僳族自治州', '25', 'N']
        location[1][3172] = ['迪庆藏族自治州', '25', 'D']
        location[1][3302] = ['贵阳', '26', 'G']
        location[1][3303] = ['六盘水', '26', 'L']
        location[1][3304] = ['遵义', '26', 'Z']
        location[1][3305] = ['安顺', '26', 'A']
        location[1][3306] = ['铜仁地区', '26', 'T']
        location[1][3307] = ['黔西南布依族苗族自治州', '26', 'Q']
        location[1][3308] = ['毕节地区', '26', 'B']
        location[1][3309] = ['黔东南苗族侗族自治州', '26', 'Q']
        location[1][3310] = ['黔南布依族苗族自治州', '26', 'Q']
        location[1][3400] = ['拉萨', '27', 'L']
        location[1][3401] = ['昌都地区', '27', 'C']
        location[1][3402] = ['山南地区', '27', 'S']
        location[1][3403] = ['日喀则地区', '27', 'R']
        location[1][3404] = ['那曲地区', '27', 'N']
        location[1][3405] = ['阿里地区', '27', 'A']
        location[1][3406] = ['林芝地区', '27', 'L']
        location[1][3480] = ['银川', '28', 'Y']
        location[1][3481] = ['石嘴山', '28', 'S']
        location[1][3482] = ['吴忠', '28', 'W']
        location[1][3483] = ['固原', '28', 'G']
        location[1][3484] = ['中卫', '28', 'Z']
        location[1][3506] = ['乌鲁木齐', '29', 'W']
        location[1][3507] = ['克拉玛依', '29', 'K']
        location[1][3508] = ['吐鲁番地区', '29', 'T']
        location[1][3509] = ['哈密地区', '29', 'H']
        location[1][3510] = ['昌吉回族自治州', '29', 'C']
        location[1][3511] = ['博尔塔拉蒙古自治州', '29', 'B']
        location[1][3512] = ['巴音郭楞蒙古自治州', '29', 'B']
        location[1][3513] = ['阿克苏地区', '29', 'A']
        location[1][3514] = ['克孜勒苏柯尔克孜自治州', '29', 'K']
        location[1][3515] = ['喀什地区', '29', 'K']
        location[1][3516] = ['和田地区', '29', 'H']
        location[1][3517] = ['伊犁哈萨克自治州', '29', 'Y']
        location[1][3518] = ['塔城地区', '29', 'T']
        location[1][3519] = ['阿勒泰地区', '29', 'A']
        location[1][3520] = ['石河子市', '29', 'S']
        location[1][3521] = ['阿拉尔市', '29', 'A']
        location[1][3522] = ['图木舒克市', '29', 'T']
        location[1][3523] = ['五家渠市', '29', 'W']
        location[1][3643] = ['西宁', '30', 'X']
        location[1][3644] = ['海东地区', '30', 'H']
        location[1][3645] = ['海北藏族自治州', '30', 'H']
        location[1][3646] = ['黄南藏族自治州', '30', 'H']
        location[1][3647] = ['海南藏族自治州', '30', 'H']
        location[1][3648] = ['果洛藏族自治州', '30', 'G']
        location[1][3649] = ['玉树藏族自治州', '30', 'Y']
        location[1][3650] = ['海西蒙古族藏族自治州', '30', 'H']
        location[1][3694] = ['西安', '31', 'X']
        location[1][3695] = ['铜川', '31', 'T']
        location[1][3696] = ['宝鸡', '31', 'B']
        location[1][3697] = ['咸阳', '31', 'X']
        location[1][3698] = ['渭南', '31', 'W']
        location[1][3699] = ['延安', '31', 'Y']
        location[1][3700] = ['汉中', '31', 'H']
        location[1][3701] = ['榆林', '31', 'Y']
        location[1][3702] = ['安康', '31', 'A']
        location[1][3703] = ['商洛', '31', 'S']
        location[1][3811] = ['兰州', '32', 'L']
        location[1][3812] = ['嘉峪关', '32', 'J']
        location[1][3813] = ['金昌', '32', 'J']
        location[1][3814] = ['白银', '32', 'B']
        location[1][3815] = ['天水', '32', 'T']
        location[1][3816] = ['武威', '32', 'W']
        location[1][3817] = ['张掖', '32', 'Z']
        location[1][3818] = ['平凉', '32', 'P']
        location[1][3819] = ['酒泉', '32', 'J']
        location[1][3820] = ['庆阳', '32', 'Q']
        location[1][3821] = ['定西', '32', 'D']
        location[1][3822] = ['陇南', '32', 'L']
        location[1][3823] = ['临夏回族自治州', '32', 'L']
        location[1][3824] = ['甘南藏族自治州', '32', 'G']

        sheng_html = '<div class="sheng"><span id-data="2">上海</span><span id-data="3">北京</span><span id-data="4">重庆</span><span id-data="5">天津</span><span id-data="6">河北</span><span id-data="7">山西</span><span id-data="8">内蒙古</span><span id-data="9">黑龙江</span><span id-data="10">吉林</span><span id-data="11">辽宁</span><span id-data="12">山东</span><span id-data="13">江苏</span><span id-data="14">浙江</span><span id-data="15">安徽</span><span id-data="16">福建</span><span id-data="17">广东</span><span id-data="18">广西</span><span id-data="19">海南</span><span id-data="20">河南</span><span id-data="21">湖北</span><span id-data="22">湖南</span><span id-data="23">江西</span><span id-data="24">四川</span><span id-data="25">云南</span><span id-data="26">贵州</span><span id-data="27">西藏</span><span id-data="28">宁夏</span><span id-data="29">新疆</span><span id-data="30">青海</span><span id-data="31">陕西</span><span id-data="32">甘肃</span><span id-data="33">香港</span><span id-data="34">澳门</span><span id-data="35">台湾</span></div>'
        selector = etree.fromstring(sheng_html)
        shengs = selector.xpath("//span")

        request_list = list()
        for i in range(1, 11):
            # url = "http://www.evpartner.com/news/policy-%d-2-0-0-0-1.html" % i
            # meta = {
            #     "t1": self.category[str(i)],
            #     "t2": "国外",
            #     "t3": "无",
            #     "t4": "无",
            #     "t5": "无"
            # }
            # request_list.append(scrapy.Request(url=url, meta=meta, headers=self.headers))


            url = "http://www.evpartner.com/news/policy-%d-1-1-0-0-1.html" % i
            meta = {
                "t1": self.category[str(i)],
                "t2": "国内",
                "t3": "国家政策",
                "t4": "无",
                "t5": "无"
            }
            request_list.append(scrapy.Request(url=url, meta=meta, headers=self.headers))

            for sheng in shengs:
                sheng_name = sheng.xpath("text()")[0]
                sheng_id = sheng.xpath("@id-data")[0]

                temp = {}

                for shi_id in location[1]:
                    if location[1][shi_id][1] == sheng_id:
                        temp[shi_id] = location[1][shi_id][0]
                # print(temp)

                for shi_id in temp:
                    meta = {
                        "t1": self.category[str(i)],
                        "t2": "国内",
                        "t3": "地方政策",
                        "t4": sheng_name,
                        "t5": temp[shi_id]
                    }
                    url = "http://www.evpartner.com/news/policy-%d-1-2-0-%d-1.html" % (i, shi_id)
                    request_list.append(scrapy.Request(url=url, meta=meta, headers=self.headers))
        print(request_list)
        return request_list


    def parse(self, response):

        next = response.xpath("//*[@class='PagedList-skipToNext']")
        if next:
            url = next.xpath("a/@href").extract_first()
            yield scrapy.Request(url=response.urljoin(url), meta=response.meta, headers=self.headers, callback=self.parse)

        articles = response.xpath("//*[@class='small-img']")
        for article in articles:
            postdate = article.xpath(".//*[@class='time']/@title").extract_first()
            if postdate:
                postdate = postdate.strip()
            url = article.xpath("div[2]/h1/a/@href").extract_first()
            meta = {
                "postdate":postdate,
            }
            meta = dict(meta, **response.meta)
            yield scrapy.Request(url=response.urljoin(url), meta=meta, headers=self.headers, callback=self.parse_details)

    def parse_details(self, response):
        try:
            item = GEVItem()
            item['url'] = response.url
            item['status'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['title'] = response.xpath('//*[@class="article-title"]/text()').extract_first().strip()
            contents = response.xpath('//*[@id="newscontent"]').extract()
            for content in contents:
                contents[contents.index(content)] = re.sub("<.*?>", '', content).strip()
            item['content'] = "\n".join(contents)
            item['postdate'] = response.meta["postdate"]
            imgs = response.xpath('//*[@id="newscontent"]//img/@src').extract()
            item['imgs'] = json.dumps(imgs)
            item["t1"] = response.meta["t1"]
            item["t2"] = response.meta["t2"]
            item["t3"] = response.meta["t3"]
            item["t4"] = response.meta["t4"]
            item["t5"] = response.meta["t5"]


            page_id = str(re.findall("\d+", response.url)[1])
            if not os.path.exists("evp/" + page_id):
                os.makedirs("evp/" + page_id)

            for img in imgs:
                try:
                    if not os.path.exists("evp/" + page_id + "/" + page_id + "_" + str(imgs.index(img)) + ".jpg"):
                        img_res = requests.request("get", url=img, headers={
                            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
                        with open("evp/" + page_id + "/" + page_id + "_" + str(imgs.index(img)) + ".jpg", "ab") as f:
                            f.write(img_res.content)
                            f.close()
                except Exception as e:
                    pass

            # print(item)
            yield item
        except Exception as e:
            with open("/root/evp_fix2_error.log", "a") as f:
                f.write(str(e))
                f.write("\n")
                f.write(response.url)
                f.write("\n")
                f.close()