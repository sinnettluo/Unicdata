# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import YicheKoubeiItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

website ='yiche_koubei_new'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    # start_urls = ['http://koubei.bitauto.com/','http://dianping.bitauto.com/']
    start_urls = ['http://dianping.bitauto.com/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 200000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self, response):
        for urlbase in response.xpath('//ul[@class="screen-box"]/li[2]/div/a'):
            url = urlbase.xpath('@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_middle1)

    def parse_middle1(self, response):
        for urlbase in response.xpath('//div[@class="kb-result"]/div/a'):
            url = urlbase.xpath('@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_middle2)
        next = response.xpath('//div[@class="pagination"]/div/a[@class="next_on"]/@href')
        if next:
            nextpage = next.extract_first()
            yield scrapy.Request(nextpage, callback=self.parse_middle1)

    def parse_middle2(self, response):
        # http://car.bitauto.com/bc301-3424/koubei/
        carinfo = dict()
        carinfo['brandname'] = response.xpath('//div[@class="crumbs-txt"]/a[4]/text()').extract_first()
        carinfo['familyname'] = response.xpath('//div[@class="crumbs-txt"]/a[5]/text()').extract_first()
        carinfo['familynameid'] = response.url.split("/")[3]

        leave_list = response.xpath('//span[@class="kb-txt"]//text()').extract()
        carinfo['leave'] = ""   #排名
        for i in leave_list:
            carinfo['leave'] += i

        carinfo['composite_score'] = response.xpath('//p[@class="mark"]/span/text()').extract_first()  #综合得分
        carnum_base1  = re.findall("carNum1 = (.*?), carPowerType", response.body.decode("utf-8"))[0]
        carnum_obj = json.loads(carnum_base1)
        # print(carnum_obj)

        carinfo['oil_consumption'] = carnum_obj[0]["num1"]   # 油耗
        carinfo['control'] = carnum_obj[1]["num1"]           # 操控
        carinfo['cost_performance'] = carnum_obj[2]["num1"]  # 性价比
        carinfo['power'] = carnum_obj[3]["num1"]             # 动力
        carinfo['to_configure'] = carnum_obj[4]["num1"]      # 配置
        carinfo['comfort_degree'] = carnum_obj[5]["num1"]    # 舒适度
        carinfo['space'] = carnum_obj[6]["num1"]            # 空间
        carinfo['appearance'] = carnum_obj[7]["num1"]       # 外观
        carinfo['interior'] = carnum_obj[8]["num1"]          # 内饰

        metadata = {"carinfo":carinfo}
        # print(metadata)
        url = response.xpath('//a[@id="aTopicListUrl"]/@href').extract_first()
        yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle3)

    def parse_middle3(self, response):
        metadata = response.meta['metadata']
        area_list = response.xpath('//div[@class="kb-list-box"]//div[@class="main"]')
        for area in area_list:
            url = area.xpath('p/a/@href').extract_first()
            yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_middle4)
        next = response.xpath('//div[@class="pagination"]//a[@class="next_on"]/@href')
        if next:
            next_page = next.extract_first()
            yield scrapy.Request(next_page, meta={"metadata":metadata}, callback=self.parse_middle3)

    def parse_middle4(self, response):
        # http://car.bitauto.com/junpaia50/koubei/828329/
        metadata = response.meta['metadata']
        u_carinfo = dict()
        u_carinfo['title'] = response.xpath('//div[@class="con-l"]/h6/text()').extract_first()    #汽车标题
        u_carinfo['year'] = re.findall("\d{4}", u_carinfo['title'])[0]    #年款
        u_carinfo['address'] = response.xpath('//span[@class="addredd"]/em/text()').extract_first()   #购车地址
        u_carinfo['time'] = response.xpath('//span[@class="time"]/em/text()').extract_first()         #购车时间
        u_carinfo['price'] = response.xpath('//div[@class="price"]//em/strong/text()').extract_first()    #裸车价
        u_carinfo['date'] = response.xpath('//div[@class="explain"]/span[@class="date"]/text()').extract_first()  #购车x月后发布
        u_carinfo['mileage'] = response.xpath(u'//div[@class="explain"]/span[contains(text(),"当前里程")]/em/text()').extract_first()  #当前里程
        u_carinfo['currently_oil_consumption'] = response.xpath(u'//div[@class="explain"]/span[contains(text(),"当前油耗")]/em/text()').extract_first() #当前油耗
        u_carinfo['vehicle_maintenance_fee'] = response.xpath(u'//div[@class="explain"]/span[contains(text(),"养车费用")]/em/text()').extract_first() #养车费用
        u_carinfo['score'] = response.xpath('//div[@class="pf-box"]/p/text()').extract_first()   #综合得分

        u_carinfo['koubei'] = dict()
        a = [u'\u6ee1\xa0\xa0\u610f\uff1a', #满意
             u'\u4e0d\u6ee1\u610f\uff1a',   #不满意
             u'\u6cb9\xa0\xa0\u8017\uff1a', #油耗
             u'\u64cd\xa0\xa0\u63a7\uff1a', #操控
             u'\u6027\u4ef7\u6bd4\uff1a',   #性价比
             u'\u52a8\xa0\xa0\u529b\uff1a', #动力
             u'\u914d\xa0\xa0\u7f6e\uff1a', #配置
             u'\u8212\u9002\u5ea6\uff1a',   #舒适度
             u'\u7a7a\xa0\xa0\u95f4\uff1a', #空间
             u'\u5916\xa0\xa0\u89c2\uff1a', #外观
             u'\u5185\xa0\xa0\u9970\uff1a', #内饰
             u'\u7efc\xa0\xa0\u5408\uff1a'  #综合
        ]

        # a = [
        #     u'满  意：',
        #     u'不满意：',
        #     u'油  耗：',
        #     u'操  控：',
        #     u'性价比：',
        #     u'动  力：',
        #     u'配  置：',
        #     u'舒适度：',
        #     u'空  间：',
        #     u'外  观：',
        #     u'内  饰：',
        #     u'综  合：'
        # ]


        context = response.xpath('//div[@class="details-cont"]/div[contains(@class, "item-box")]')
        for area in context:
            test = area.xpath('div/text()').extract_first().strip()
            # print(test)
            # if test==u"满  意：":
            if test == a[0]:
                u_carinfo['koubei']['u_satisfied'] = area.xpath('p/text()').extract_first()  # 这里对应于网页上的满意
            # elif test==u"不满意：":
            elif test == a[1]:
                u_carinfo['koubei']['u_not_satisfied'] = area.xpath('p/text()').extract_first()      # 不满意
            # elif test==u"油  耗：":
            elif test == a[2]:
                css_str = area.xpath('//em/@style').extract_first()  # 油耗
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_fuel'] = int(score) / 20
                u_carinfo['koubei']['u_oil_consumption'] = area.xpath('p/text()').extract_first()      # 油耗
            # elif test==u"操  控：":
            elif test == a[3]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_control'] = int(score) / 20
                u_carinfo['koubei']['u_control'] = area.xpath('p/text()').extract_first()      # 操控
            # elif test==u"性价比：":
            elif test == a[4]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_cost'] = int(score) / 20
                u_carinfo['koubei']['u_cost_performance'] = area.xpath('p/text()').extract_first()      # 性价比
            # elif test==u"动  力：":
            elif test == a[5]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_power'] = int(score) / 20
                u_carinfo['koubei']['u_power'] = area.xpath('p/text()').extract_first()      # 动力
            # elif test==u"配  置：":
            elif test == a[6]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_configure'] = int(score) / 20
                u_carinfo['koubei']['u_to_configure'] = area.xpath('p/text()').extract_first()      # 配置
            # elif test==u"舒适度：":
            elif test == a[7]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_comfort'] = int(score) / 20
                u_carinfo['koubei']['u_comfort_degree'] = area.xpath('p/text()').extract_first()      # 舒适度
            # elif test==u"空  间：":
            elif test == a[8]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_space'] = int(score) / 20
                u_carinfo['koubei']['u_space'] = area.xpath('p/text()').extract_first()      # 空间
            # elif test==u"外  观：":
            elif test == a[9]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_appearance'] = int(score) / 20
                u_carinfo['koubei']['u_appearance'] = area.xpath('p/text()').extract_first()      # 外观
            # elif test==u"内  饰：":
            elif test == a[10]:
                css_str = area.xpath('//em/@style').extract_first()
                score = re.findall("\d+", css_str)[0]
                u_carinfo['koubei']['score_trim'] = int(score) / 20
                u_carinfo['koubei']['u_interior'] = area.xpath('p/text()').extract_first()      # 内饰
            # elif test==u"综  合：":
            elif test == a[11]:
                if area.xpath('text()').extract_first().strip():
                    css_str = area.xpath('//em/@style').extract_first()
                    score = re.findall("\d+", css_str)[0]
                    u_carinfo['koubei']['score_comprehensive'] = int(score) / 20
                    u_carinfo['koubei']['u_comprehensive'] = area.xpath('text()').extract_first().strip()      # 综合
                # else:
                #     try:
                #         u_carinfo['koubei']['u_comprehensive'] = area.xpath('p/text()').extract_first().strip()  # 综合
                #     except:
                #         u_carinfo['koubei']['u_comprehensive'] = area.xpath('p/span/text()').extract_first().strip()  # 综合

        u_carinfo['url'] = response.url
        u_carinfo['helpfulCount'] = response.xpath("//*[@id='spSupportCount']/text()").extract_first()
        u_carinfo['visitCount'] = response.xpath("//*[@class='comment-summary']/span/em[1]/text()").re("\d+")[0]
        u_carinfo['commentCount'] = response.xpath("//*[@class='comment-summary']/span/em[2]/text()").re("\d+")[0]
        u_carinfo['post_time'] = response.xpath("//*[@class='comment-summary']/span/text()[1]").re("\d+\-\d+\-\d+")[0]
        addmeta = {"u_carinfo":u_carinfo}
        metadata = dict(metadata, **addmeta)

        url = response.xpath('//div[@class="con-r"]/a/@href').extract_first()
        yield scrapy.Request(url, meta={"metadata":metadata}, callback=self.parse_finally, dont_filter=True)

    def parse_finally(self, response):
        # http://i.yiche.com/u25936032/
        metadata = response.meta['metadata']
        item = YicheKoubeiItem()
        userinfo = dict()
        userinfo['userid'] = re.findall("\d+", response.url)[0]
        userinfo['username'] = response.xpath('//div[@class="his_infor_box"]//h4/a/@title').extract_first() # 用户名
        userinfo['follow'] = response.xpath(u'//div[@class="his_infor_box"]//div[@class="ta_guanzhu"]//dd[contains(text(),"关注")]/../dt/text()').extract_first() # 关注
        userinfo['fans'] = response.xpath(u'//div[@class="his_infor_box"]//div[@class="ta_guanzhu"]//dd[contains(text(),"粉丝")]/../dt/text()').extract_first() # 粉丝
        userinfo['authentication'] = response.xpath(u'//div[@class="his_infor_box"]//div[@class="ta_guanzhu"]//dd[contains(text(),"认证车主")]/../dt/img/@alt').extract_first() #认证车主
        userinfo['grade'] = response.xpath(u'//div[@class="his_infor_box"]//ul[@class="list"]//b[contains(text(),"等级")]/../div/span/text()').extract_first()  # 等级
        medal = response.xpath(u'//div[@class="his_infor_box"]//ul[@class="list"]//b[contains(text(),"勋章")]/../p/text()').extract() # 勋章
        userinfo['medal'] = ""
        flag = 0
        for x in medal:
            if flag:
                userinfo['medal'] += "," + x.strip().strip("\r").strip("\n")
            else:
                userinfo['medal'] = x.strip().strip("\r").strip("\n")
                flag = 1
        # item['carinfo'] = metadata['carinfo']
        # item['u_carinfo'] = metadata['u_carinfo']
        # item['userinfo'] = userinfo
        item['url'] = metadata['u_carinfo']['url']
        # item['website'] = website

        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        item['familyname'] = metadata['carinfo']['familyname']
        item['brand'] = metadata['carinfo']['brandname']
        item['familynameid'] = metadata['carinfo']['familynameid']
        item['shortdesc'] = metadata['u_carinfo']['title']

        item['buy_date'] = metadata['u_carinfo']['time']
        item['buy_location'] = metadata['u_carinfo']['address']
        item['buy_pure_price'] = metadata['u_carinfo']['price']
        item['buyerid'] = userinfo['userid']
        item['buyername'] = userinfo['username']

        item['mileage'] = metadata['u_carinfo']['mileage']
        item['oil_consume'] = metadata['u_carinfo']['currently_oil_consumption']

        item['score'] = metadata['u_carinfo']['score']

        # print(metadata['u_carinfo']['koubei'])

        item['score_appearance_compare'] = metadata['u_carinfo']['koubei']['u_appearance'] if "u_appearance" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_comfort_compare']= metadata['u_carinfo']['koubei']['u_comfort_degree'] if "u_comfort_degree" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_control_compare'] = metadata['u_carinfo']['koubei']['u_control'] if "u_control" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_cost_compare'] = metadata['u_carinfo']['koubei']['u_cost_performance'] if "u_cost_performance" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_fuel_compare'] = metadata['u_carinfo']['koubei']['u_oil_consumption'] if "u_oil_consumption" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_power_compare'] = metadata['u_carinfo']['koubei']['u_power'] if "u_power" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_space_compare'] = metadata['u_carinfo']['koubei']['u_space'] if "u_space" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['score_trim_compare'] = metadata['u_carinfo']['koubei']['u_interior'] if "u_interior" in metadata['u_carinfo']['koubei'].keys() else "-"

        item['satisfied'] = metadata['u_carinfo']['koubei']['u_satisfied'] if "u_satisfied" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['unsatisfied'] = metadata['u_carinfo']['koubei']['u_not_satisfied'] if "u_not_satisfied" in metadata['u_carinfo']['koubei'].keys() else "-"

        # item['ucid'] = None
        item['guideprice'] = None
        item['usage'] = None
        item['fuel'] = None
        item['comment_detail'] = None
        item['comment_people'] = None
        item['isGoodComment'] = None
        item['picurl'] = None
        item['score_star'] = None
        item['score_appearance'] = metadata['u_carinfo']['koubei']['score_appearance'] if "score_appearance" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_comfort'] = metadata['u_carinfo']['koubei']['score_comfort'] if "score_comfort" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_control'] = metadata['u_carinfo']['koubei']['score_control'] if "score_control" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_cost'] = metadata['u_carinfo']['koubei']['score_cost'] if "score_cost" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_fuel'] = metadata['u_carinfo']['koubei']['score_fuel'] if "score_fuel" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_power'] = metadata['u_carinfo']['koubei']['score_power'] if "score_power" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_space'] = metadata['u_carinfo']['koubei']['score_space'] if "score_space" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['score_trim'] = metadata['u_carinfo']['koubei']['score_trim'] if "score_trim" in metadata['u_carinfo']['koubei'].keys() else "-"
        item['description'] = None
        item['visitCount'] = metadata['u_carinfo']['visitCount']
        item['helpfulCount'] = metadata['u_carinfo']['helpfulCount']
        item['commentCount'] = metadata['u_carinfo']['commentCount']
        item['post_time'] = metadata['u_carinfo']['post_time']
        item['spec_id'] = None

        item['status'] = metadata['u_carinfo']['url'] + "-" + str(item['visitCount']) + "-" + str(
                item['helpfulCount']) + "-" + str(item['commentCount'])

        # yield item
        print(item)