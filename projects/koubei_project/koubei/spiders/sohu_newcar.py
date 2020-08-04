# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import SohuNewCarItem
# from scrapy.conf import settings
import logging
from urllib import parse
from lxml import etree


website ='sohu_newcar'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['http://db.auto.sohu.com/home/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def parse(self,response):
        lis = response.xpath("//ul[@class='tree']/li[@class='close_child']")
        for li in lis:
            brandname = li.xpath("h4/a/text()[2]").extract_first()
            brandid = li.xpath("h4/a/@id").extract_first().replace("b", "")
            # print(brandname)
            # print(brandid)
            uls = li.xpath("ul")
            for ul in uls:
                factoryid = ul.xpath("li[1]/a/@id").extract_first().replace("c","")
                sub_lis = ul.xpath("li")[1:]
                for sub_li in sub_lis:
                    # url = response.urljoin(li.xpath("a/@href").extract_first())
                    familyname = sub_li.xpath("a/text()[2]").extract_first()
                    familyid = sub_li.xpath("a/@href").extract_first().split("/")[-1]
                    url = "http://db.auto.sohu.com/api/para/data/model_" + str(familyid) + ".json"

                    metadata = {
                        "brandname": brandname,
                        "brandid": brandid,
                        "familyname": familyname,
                        "familyid": familyid,
                        "factoryid": factoryid
                    }

                    yield scrapy.Request(url=url, meta={"metadata":metadata}, callback=self.parse_model)

    def parse_model(self, response):
        res = response.text
        pattern = re.compile('%u[0-9a-f]{4}')
        for i in pattern.findall(res):
            res = res.replace(i, chr(int(i[2:], 16)))
        family_obj = json.loads(res)
        metadata = response.meta["metadata"]
        if "SIP_M_TRIMS" in family_obj:
            for line in family_obj['SIP_M_TRIMS']:
                trimid = line['SIP_T_ID']
                trimname = parse.unquote(line['SIP_T_NAME'])
                trimgear = parse.unquote(line['SIP_T_GEAR'])
                trimdisp = line['SIP_T_DISP']
                trimyear = line['SIP_T_YEAR']
                trimdata = dict({'trimid': trimid, 'trimname': trimname, 'trimgear': trimgear, 'trimdisp': trimdisp,
                                 'trimyear': trimyear}, **metadata)
                urlbase = "http://db.auto.sohu.com/api/para/data/trim_" + str(trimid) + ".json"
                yield scrapy.Request(urlbase, meta={'metadata': trimdata}, callback=self.parse_data)

    # def parse_model(self, response):
    #     on_sell_list = response.xpath("//div[@class='on_sell']/div[1]/ul[1]/li")
    #     print(on_sell_list)
    #     for li in on_sell_list[:1]:
    #         # url = response.urljoin(li.xpath("a/@href").extract_first())
    #         trimid = li.xpath("a/@href").extract_first().split("/")[-1]
    #         url = "http://db.auto.sohu.com/api/para/data/trim_" + str(trimid) + ".json"
    #         yield scrapy.Request(url=url, callback=self.parse_data)
    #
    #     if response.xpath("//div[@class='stop_sell']"):
    #         year_list = response.xpath("//div[@class='stop_sell']/h4")
    #         for year in year_list.xpath("a"):
    #             url = response.urljoin(year.xpath("@href").extract_first())
    #             yield scrapy.Request(url=url, callback=self.parse_model2)
    #
    # def parse_model2(self, response):
    #     trs = response.xpath("//*[@class='b jsq']/tr")
    #     for tr in trs:
    #         # url = response.urljoin(tr.xpath("td[1]/a/@href").extract_first())
    #         trimid = tr.xpath("td[1]/a/@href").extract_first().split("/")[-1]
    #         url = "http://db.auto.sohu.com/api/para/data/trim_" + str(trimid) + ".json"
    #         yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self, response):
        res = response.text
        pattern = re.compile('%u[0-9a-f]{4}')
        for i in pattern.findall(res):
            res = res.replace(i, chr(int(i[2:], 16)))
        data_obj = json.loads(res)
        item = SohuNewCarItem()
        # index = scrapy.Field()
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        # item['website'] = website
        item['status'] = response.url
        item['url'] = response.url

        item['trimmid'] = response.meta["metadata"]["trimid"]
        item['familyid'] = response.meta["metadata"]["familyid"]
        # item['brandcode'] = None
        item['brandname'] = response.meta["metadata"]["brandname"]
        item['brandid'] = response.meta["metadata"]["brandid"]
        item['factorycode'] = data_obj["brandNameDomain"] if "brandNameDomain" in data_obj else "-"
        item['factoryid'] = response.meta["metadata"]["factoryid"]
        item['familyname'] = response.meta["metadata"]["familyname"]

        item['factoryname'] = data_obj["SIP_C_104"] if "SIP_C_104" in data_obj else "-"
        item['makeyear'] = data_obj["SIP_T_YEAR"] if "SIP_T_YEAR" in data_obj else "-"


        item["shortdesc"] = response.meta["metadata"]["trimname"]
        item['guildprice'] = data_obj["SIP_C_102"] if "SIP_C_102" in data_obj else "-"
        item['shop4s_price'] = data_obj['SIP_C_103'] if "SIP_C_103" in data_obj else "-"
        item['factoryname'] = data_obj['SIP_C_104'] if "SIP_C_104" in data_obj else "-"
        item['level'] = data_obj['SIP_C_105'] if "SIP_C_105" in data_obj else "-"
        item['body'] = data_obj['SIP_C_106'] if "SIP_C_106" in data_obj else "-"
        item['l_w_h'] = data_obj['SIP_C_293'] if "SIP_C_293" in data_obj else "-"
        item['motor'] = data_obj['SIP_C_107'] if "SIP_C_107" in data_obj else "-"
        item['gear'] = data_obj['SIP_C_108'] if "SIP_C_108" in data_obj else "-"
        ##
        item['power_type'] = data_obj['SIP_C_303'] if "SIP_C_303" in data_obj else "-"
        item['top_speed'] = data_obj['SIP_C_112'] if "SIP_C_112" in data_obj else "-"
        item['oil_consumption'] = data_obj['SIP_C_294'] if "SIP_C_294" in data_obj else "-"
        item['acceleration'] = data_obj['SIP_C_113'] if "SIP_C_113" in data_obj else "-"
        ##
        item['maintenance_period'] = data_obj['SIP_C_114'] if "SIP_C_114" in data_obj else "-"
        ##
        item['maintenance_fee'] = data_obj['SIP_C_304'] if "SIP_C_304" in data_obj else "-"
        item['warranty_policy'] = data_obj['SIP_C_115'] if "SIP_C_115" in data_obj else "-"
        item['collision_star'] = data_obj['SIP_C_116'] if "SIP_C_116" in data_obj else "-"
        ##
        item['more_parameters'] = data_obj['SIP_C_295'] if "SIP_C_295" in data_obj else "-"
        item['length'] = data_obj['SIP_C_117'] if "SIP_C_117" in data_obj else "-"
        item['width'] = data_obj['SIP_C_118'] if "SIP_C_118" in data_obj else "-"
        item['height'] = data_obj["SIP_C_119"] if "SIP_C_119" in data_obj else "-"
        item['wheelbase'] = data_obj['SIP_C_120'] if "SIP_C_120" in data_obj else "-"
        item['front_wheel'] = data_obj['SIP_C_121'] if "SIP_C_121" in data_obj else "-"
        item['back_whell'] = data_obj['SIP_C_122'] if "SIP_C_122" in data_obj else "-"
        item['weight'] = data_obj['SIP_C_123'] if "SIP_C_123" in data_obj else "-"
        item['body_structure'] = data_obj['SIP_C_124'] if "SIP_C_124" in data_obj else "-"
        item['door'] = data_obj['SIP_C_125'] if "SIP_C_125" in data_obj else "-"
        item['seat'] = data_obj['SIP_C_126'] if "SIP_C_126" in data_obj else "-"
        item['tank_volume'] = data_obj['SIP_C_127'] if "SIP_C_127" in data_obj else "-"
        item['luggage_volume'] = data_obj['SIP_C_128'] if "SIP_C_128" in data_obj else "-"
        item['min_ground'] = data_obj['SIP_C_129'] if "SIP_C_129" in data_obj else "-"
        item['min_turning'] = data_obj['SIP_C_130'] if "SIP_C_130" in data_obj else "-"
        item['approach_angle'] = data_obj['SIP_C_131'] if "SIP_C_131" in data_obj else "-"
        item['departure_angle'] = data_obj['SIP_C_132'] if "SIP_C_132" in data_obj else "-"
        item['desc_motor'] = data_obj['SIP_C_134'] if "SIP_C_134" in data_obj else "-"
        item['motor_type'] = data_obj['SIP_C_135'] if "SIP_C_135" in data_obj else "-"
        item['output'] = data_obj["SIP_C_136"] if "SIP_C_136" in data_obj else "-"
        item['cylinder_capacity'] = data_obj['SIP_C_137'] if "SIP_C_137" in data_obj else "-"
        item['workingtype'] = data_obj['SIP_C_138'] if "SIP_C_138" in data_obj else "-"
        item['cylinder_num'] = data_obj['SIP_C_139'] if "SIP_C_139" in data_obj else "-"
        ##
        item['cylinder_arrangement'] = data_obj['SIP_C_140'] if "SIP_C_140" in data_obj else "-"
        item['each_cylinder_num'] = data_obj['SIP_C_141'] if "SIP_C_141" in data_obj else "-"
        ##
        item['valve_structure'] = data_obj['SIP_C_142'] if "SIP_C_142" in data_obj else "-"
        item['compression_ratio'] = data_obj['SIP_C_143'] if "SIP_C_143" in data_obj else "-"
        item['maxps'] = data_obj['SIP_C_297'] if "SIP_C_297" in data_obj else "-"
        item['maxpower'] = data_obj['SIP_C_298'] if "SIP_C_298" in data_obj else "-"
        ##
        item['maxtorque'] = data_obj['SIP_C_299'] if "SIP_C_299" in data_obj else "-"
        item['rise_power'] = data_obj['SIP_C_148'] if "SIP_C_148" in data_obj else "-"
        item['mixedtype'] = data_obj['SIP_C_305'] if "SIP_C_305" in data_obj else "-"
        item['plugform'] = data_obj['SIP_C_306'] if "SIP_C_306" in data_obj else "-"
        ##
        item['electric_motor_maxpower'] = data_obj['SIP_C_307'] if "SIP_C_307" in data_obj else "-"
        ##
        item['electric_motor_maxtorque'] = data_obj['SIP_C_308'] if "SIP_C_308" in data_obj else "-"
        ##
        item['maxmileage'] = data_obj['SIP_C_309'] if "SIP_C_309" in data_obj else "-"
        ##
        item['battery_type'] = data_obj['SIP_C_310'] if "SIP_C_310" in data_obj else "-"
        item['battery_capacity'] = data_obj['SIP_C_311'] if "SIP_C_311" in data_obj else "-"
        item['fuel'] = data_obj['SIP_C_149'] if "SIP_C_149" in data_obj else "-"
        ##
        item['oil_supply_mode'] = data_obj['SIP_C_150'] if "SIP_C_150" in data_obj else "-"
        ##
        item['cylinder_head_material'] = data_obj['SIP_C_151'] if "SIP_C_151" in data_obj else "-"
        item['cylinder_body_material'] = data_obj['SIP_C_152'] if "SIP_C_152" in data_obj else "-"
        item['emission'] = data_obj['SIP_C_155'] if "SIP_C_155" in data_obj else "-"
        item['gear_name'] = data_obj['SIP_C_156'] if "SIP_C_156" in data_obj else "-"
        ##
        item['block_num'] = data_obj['SIP_C_157'] if "SIP_C_157" in data_obj else "-"
        item['geartype'] = data_obj["SIP_C_158"] if "SIP_C_158" in data_obj else "-"
        item['motor_num'] = data_obj['SIP_C_353'] if "SIP_C_353" in data_obj else "-"
        item['drivemode'] = data_obj['SIP_C_159'] if "SIP_C_159" in data_obj else "-"
        item['front_suspension'] = data_obj['SIP_C_160'] if "SIP_C_160" in data_obj else "-"
        item['back_suspension'] = data_obj['SIP_C_161'] if "SIP_C_161" in data_obj else "-"

        item['chassis_structure'] = data_obj['SIP_C_162'] if "SIP_C_162" in data_obj else "-"
        item['front_tire'] = data_obj['SIP_C_163'] if "SIP_C_163" in data_obj else "-"
        item['back_tire'] = data_obj['SIP_C_164'] if "SIP_C_164" in data_obj else "-"
        item['front_brake'] = data_obj['SIP_C_167'] if "SIP_C_167" in data_obj else "-"
        item['back_brake'] = data_obj['SIP_C_168'] if "SIP_C_168" in data_obj else "-"
        item['m_d_airbag'] = data_obj['SIP_C_177_178'] if "SIP_C_177_178" in data_obj else "-"
        item['f_b_airbag'] = data_obj['SIP_C_179_180'] if "SIP_C_179_180" in data_obj else "-"
        item['ABS'] = data_obj['SIP_C_185'] if "SIP_C_185" in data_obj else "-"
        ##
        item['braking_force_distribution'] = data_obj['SIP_C_186'] if "SIP_C_186" in data_obj else "-"
        ##
        item['brake_assistant'] = data_obj['SIP_C_187'] if "SIP_C_187" in data_obj else "-"
        ##
        item['traction_control'] = data_obj['SIP_C_188'] if "SIP_C_188" in data_obj else "-"
        ##
        item['body_stability_control'] = data_obj['SIP_C_189'] if "SIP_C_189" in data_obj else "-"
        ##
        item['skylight_type'] = data_obj['SIP_C_316'] if "SIP_C_316" in data_obj else "-"
        item['f_b_reversing_radar'] = data_obj['SIP_C_201_343'] if "SIP_C_201_343" in data_obj else "-"
        item['body_color_opt'] = data_obj['SIP_C_291'] if "SIP_C_291" in data_obj else "-"

        item['inner_color_opt'] = data_obj['SIP_C_292'] if "SIP_C_292" in data_obj else "-"
        ##
        item['dipped_headlight'] = data_obj['SIP_C_318'] if "SIP_C_318" in data_obj else "-"
        ##
        item['high_beam'] = data_obj['SIP_C_347'] if "SIP_C_347" in data_obj else "-"
        item['daytime_lights'] = data_obj['SIP_C_260'] if "SIP_C_260" in data_obj else "-"
        item['front_inducer_wiper'] = data_obj['SIP_C_272'] if "SIP_C_272" in data_obj else "-"
        item['air_conditioning'] = data_obj['SIP_C_320'] if "SIP_C_320" in data_obj else "-"
        item['chargingtype'] = data_obj['SIP_C_355'] if "SIP_C_355" in data_obj else "-"
        item['quickcharge'] = data_obj['SIP_C_356'] if "SIP_C_356" in data_obj else "-"
        item['slowcharge'] = data_obj['SIP_C_357'] if "SIP_C_357" in data_obj else "-"
        ##
        item['hub_material'] = data_obj['SIP_C_165'] if "SIP_C_165" in data_obj else "-"
        item['spare_tire'] = data_obj['SIP_C_166'] if "SIP_C_166" in data_obj else "-"
        item['park_brake'] = data_obj['SIP_C_169'] if "SIP_C_169" in data_obj else "-"
        ##
        item['type_distributor'] = data_obj['SIP_C_170'] if "SIP_C_170" in data_obj else "-"
        ##
        item['steering_power'] = data_obj['SIP_C_171'] if "SIP_C_171" in data_obj else "-"
        item['adjust_suspension'] = data_obj['SIP_C_172'] if "SIP_C_172" in data_obj else "-"
        item['air_suspension'] = data_obj['SIP_C_173'] if "SIP_C_173" in data_obj else "-"
        item['central_differential_structure'] = data_obj['SIP_C_322'] if "SIP_C_322" in data_obj else "-"
        item['centr_diff_lock'] = data_obj['SIP_C_323'] if "SIP_C_323" in data_obj else "-"
        item['front_differential'] = data_obj['SIP_C_324'] if "SIP_C_324" in data_obj else "-"
        item['back_differential'] = data_obj['SIP_C_325'] if "SIP_C_325" in data_obj else "-"
        item['f_b_air_curtain'] = data_obj['SIP_C_181_182'] if "SIP_C_181_182" in data_obj else "-"
        item['knee_airbag'] = data_obj['SIP_C_183'] if "SIP_C_183" in data_obj else "-"
        ##
        item['belt_hint'] = data_obj['SIP_C_184'] if "SIP_C_184" in data_obj else "-"
        ##
        item['safety_system'] = data_obj['SIP_C_190'] if "SIP_C_190" in data_obj else "-"
        item['autoparking'] = data_obj['SIP_C_191'] if "SIP_C_191" in data_obj else "-"
        ##
        item['hill_start_assist'] = data_obj['SIP_C_358'] if "SIP_C_358" in data_obj else "-"
        item['HDC'] = data_obj['SIP_C_192'] if "SIP_C_192" in data_obj else "-"
        item['motorguard'] = data_obj['SIP_C_193'] if "SIP_C_193" in data_obj else "-"
        item['car_central_lock'] = data_obj['SIP_C_194'] if "SIP_C_194" in data_obj else "-"
        item['remote_key'] = data_obj['SIP_C_195'] if "SIP_C_195" in data_obj else "-"
        ##
        item['keylessstartup'] = data_obj['SIP_C_196'] if "SIP_C_196" in data_obj else "-"
        item['keylessenter'] = data_obj['SIP_C_336'] if "SIP_C_336" in data_obj else "-"
        ##
        item['tire_pressure_monitoring_device'] = data_obj['SIP_C_197'] if "SIP_C_197" in data_obj else "-"
        ##
        item['zero_tire_pressure'] = data_obj['SIP_C_198'] if "SIP_C_198" in data_obj else "-"
        ##
        item['parallel_auxiliary'] = data_obj['SIP_C_199'] if "SIP_C_199" in data_obj else "-"
        ##
        item['panoramic_camera'] = data_obj['SIP_C_204'] if "SIP_C_204" in data_obj else "-"
        item['nightvision'] = data_obj['SIP_C_205'] if "SIP_C_205" in data_obj else "-"
        ##
        item['ISO_FIX_child_seat_interface'] = data_obj['SIP_C_312'] if "SIP_C_312" in data_obj else "-"
        ##
        item['LATCH_child_seat_interface'] = data_obj['SIP_C_313'] if "SIP_C_313" in data_obj else "-"
        item['childlock'] = data_obj['SIP_C_314'] if "SIP_C_314" in data_obj else "-"
        ##
        item['sports_appearance_suite'] = data_obj['SIP_C_210'] if "SIP_C_210" in data_obj else "-"
        ##
        item['electric_suction_door'] = data_obj['SIP_C_212'] if "SIP_C_212" in data_obj else "-"
        ##
        item['electric_backup_box'] = data_obj['SIP_C_337'] if "SIP_C_337" in data_obj else "-"
        ##
        item['inductive_backup_box'] = data_obj['SIP_C_338'] if "SIP_C_338" in data_obj else "-"
        item['roofrack'] = data_obj['SIP_C_339'] if "SIP_C_339" in data_obj else "-"
        ##
        item['other_body_configuration'] = data_obj['SIP_C_300'] if "SIP_C_300" in data_obj else "-"
        ##
        item['leather_steering_wheel'] = data_obj['SIP_C_213'] if "SIP_C_213" in data_obj else "-"
        ##
        item['steering_wheel_adjustment'] = data_obj['SIP_C_214_215'] if "SIP_C_214_215" in data_obj else "-"
        ##
        item['steering_wheel_electric_control'] = data_obj['SIP_C_216'] if "SIP_C_216" in data_obj else "-"
        ##
        item['multifunction_steering_wheel'] = data_obj['SIP_C_217'] if "SIP_C_217" in data_obj else "-"
        ##
        item['steering_wheel_shift'] = data_obj['SIP_C_218'] if "SIP_C_218" in data_obj else "-"
        ##
        item['steering_wheel_heating'] = data_obj['SIP_C_340'] if "SIP_C_340" in data_obj else "-"
        ##
        item['steering_wheel_memory'] = data_obj['SIP_C_341'] if "SIP_C_341" in data_obj else "-"
        ##
        item['liquid_crystal_dashboard'] = data_obj['SIP_C_342'] if "SIP_C_342" in data_obj else "-"
        item['cruise_control'] = data_obj['SIP_C_175'] if "SIP_C_175" in data_obj else "-"
        item['adaptive_cruise'] = data_obj['SIP_C_176'] if "SIP_C_176" in data_obj else "-"
        item['computer_screen'] = data_obj['SIP_C_219'] if "SIP_C_219" in data_obj else "-"
        ##
        item['HUD_top_digital_display'] = data_obj['SIP_C_200'] if "SIP_C_200" in data_obj else "-"
        item['reversing_image'] = data_obj['SIP_C_202'] if "SIP_C_202" in data_obj else "-"
        ##
        item['auto_position_parking'] = data_obj['SIP_C_203'] if "SIP_C_203" in data_obj else "-"
        ##
        item['luggage_compartment_lamp'] = data_obj['SIP_C_221'] if "SIP_C_221" in data_obj else "-"
        ##
        item['independent_power_supply_interface'] = data_obj['SIP_C_222'] if "SIP_C_222" in data_obj else "-"
        ##
        item['LCD_panel_display'] = data_obj['SIP_C_223'] if "SIP_C_223" in data_obj else "-"
        ##
        item['other_inner_configuration'] = data_obj['SIP_C_301'] if "SIP_C_301" in data_obj else "-"
        item['seat_material'] = data_obj['SIP_C_224'] if "SIP_C_224" in data_obj else "-"
        item['sports_seats'] = data_obj['SIP_C_225'] if "SIP_C_225" in data_obj else "-"
        ##
        item['seat_height_adjustment'] = data_obj['SIP_C_226'] if "SIP_C_226" in data_obj else "-"
        ##
        item['waist_support_regulation'] = data_obj['SIP_C_227'] if "SIP_C_227" in data_obj else "-"
        ##
        item['shoulder_support_regulation'] = data_obj['SIP_C_228'] if "SIP_C_228" in data_obj else "-"
        ##
        item['seat_electric_adjustment'] = data_obj['SIP_C_229_230'] if "SIP_C_229_230" in data_obj else "-"
        ##
        item['back_seat_adjustment'] = data_obj['SIP_C_317'] if "SIP_C_317" in data_obj else "-"
        ##
        item['electric_seat_memory'] = data_obj['SIP_C_233'] if "SIP_C_233" in data_obj else "-"
        ##
        item['f_b_seat_heating'] = data_obj['SIP_C_234_235'] if "SIP_C_234_235" in data_obj else "-"
        ##
        item['f_b_seat_ventilation'] = data_obj['SIP_C_236_344'] if "SIP_C_236_344" in data_obj else "-"
        ##
        item['f_b_seat_massage'] = data_obj['SIP_C_237_345'] if "SIP_C_237_345" in data_obj else "-"
        ##
        item['back_seat_back_seat_way'] = data_obj['SIP_C_238_239'] if "SIP_C_238_239" in data_obj else "-"
        ##
        item['third_row_seats'] = data_obj['SIP_C_240'] if "SIP_C_240" in data_obj else "-"
        ##
        item['f_b_seat_central_armrest'] = data_obj['SIP_C_241_242'] if "SIP_C_241_242" in data_obj else "-"
        ##
        item['back_row_cup_frame'] = data_obj['SIP_C_346'] if "SIP_C_346" in data_obj else "-"
        item['CD_DVD'] = data_obj['SIP_C_321'] if "SIP_C_321" in data_obj else "-"
        item['CD_MP3'] = data_obj['SIP_C_247'] if "SIP_C_247" in data_obj else "-"
        ##
        item['external_source_interface'] = data_obj['SIP_C_248'] if "SIP_C_248" in data_obj else "-"
        ##
        item['loudspeaker_number'] = data_obj['SIP_C_249'] if "SIP_C_249" in data_obj else "-"
        item['bluetooth'] = data_obj['SIP_C_251'] if "SIP_C_251" in data_obj else "-"
        item['carTV'] = data_obj['SIP_C_252'] if "SIP_C_252" in data_obj else "-"
        item['LCD_screen'] = data_obj['SIP_C_253'] if "SIP_C_253" in data_obj else "-"
        ##
        item['back_LCD_screen'] = data_obj['SIP_C_254'] if "SIP_C_254" in data_obj else "-"
        item['GPS'] = data_obj['SIP_C_255'] if "SIP_C_255" in data_obj else "-"
        ##
        item['telematics'] = data_obj['SIP_C_257'] if "SIP_C_257" in data_obj else "-"
        ##
        item['human_computer_interaction'] = data_obj['SIP_C_258'] if "SIP_C_258" in data_obj else "-"
        ##
        item['front_fog_lamp'] = data_obj['SIP_C_261'] if "SIP_C_261" in data_obj else "-"
        ##
        item['automatic_opening_closing_headlights'] = data_obj['SIP_C_262'] if "SIP_C_262" in data_obj else "-"
        ##
        item['headlights_regulation'] = data_obj['SIP_C_263'] if "SIP_C_263" in data_obj else "-"
        ##
        item['height_adjustable_headlights'] = data_obj['SIP_C_264'] if "SIP_C_264" in data_obj else "-"
        ##
        item['headlights_cleaning_device'] = data_obj['SIP_C_265'] if "SIP_C_265" in data_obj else "-"
        ##
        item['inner_atmosphere_lamp'] = data_obj['SIP_C_266'] if "SIP_C_266" in data_obj else "-"
        ##
        item['adaptive_far_near_light'] = data_obj['SIP_C_348'] if "SIP_C_348" in data_obj else "-"
        ##
        item['steering_auxiliary_lamp'] = data_obj['SIP_C_349'] if "SIP_C_349" in data_obj else "-"
        ##
        item['f_b_electric_windows'] = data_obj['SIP_C_267_268'] if "SIP_C_267_268" in data_obj else "-"
        ##
        item['one_button_function_for_window'] = data_obj['SIP_C_269'] if "SIP_C_269" in data_obj else "-"
        ##
        item['anti_clamping_hand_function_for_window'] = data_obj['SIP_C_270'] if "SIP_C_270" in data_obj else "-"
        ##
        item['anti_ultraviolet_insulated_glass'] = data_obj['SIP_C_271'] if "SIP_C_271" in data_obj else "-"
        ##
        item['anti_glare_in_out_rearview_mirror'] = data_obj['SIP_C_319_277'] if "SIP_C_319_277" in data_obj else "-"
        ##
        item['rearview_mirror_electromotion'] = data_obj['SIP_C_278'] if "SIP_C_278" in data_obj else "-"
        ##
        item['rearview_mirror_heating'] = data_obj['SIP_C_279'] if "SIP_C_279" in data_obj else "-"
        ##
        item['rearview_mirror_electric_folding'] = data_obj['SIP_C_282'] if "SIP_C_282" in data_obj else "-"
        ##
        item['back_rear_wiper'] = data_obj['SIP_C_273'] if "SIP_C_273" in data_obj else "-"
        ##
        item['defrosting_rear_windshield'] = data_obj['SIP_C_274'] if "SIP_C_274" in data_obj else "-"
        ##
        item['rear_windscreen_shading_curtain'] = data_obj['SIP_C_275'] if "SIP_C_275" in data_obj else "-"
        ##
        item['rear_side_shading_curtain'] = data_obj['SIP_C_276'] if "SIP_C_276" in data_obj else "-"
        ##
        item['back_privacy_glass'] = data_obj['SIP_C_350'] if "SIP_C_350" in data_obj else "-"
        ##
        item['rearview_mirror_memory'] = data_obj['SIP_C_351'] if "SIP_C_351" in data_obj else "-"
        ##
        item['sunshade_make_up_mirror'] = data_obj['SIP_C_352'] if "SIP_C_352" in data_obj else "-"
        ##
        item['back_exhaust_vent'] = data_obj['SIP_C_285'] if "SIP_C_285" in data_obj else "-"
        ##
        item['front_temperature_control'] = data_obj['SIP_C_286'] if "SIP_C_286" in data_obj else "-"
        ##
        item['back_temperature_control'] = data_obj['SIP_C_287'] if "SIP_C_287" in data_obj else "-"
        ##
        item['pollen_filtration'] = data_obj['SIP_C_288'] if "SIP_C_288" in data_obj else "-"
        ##
        item['vehicle_efrigerator'] = data_obj['SIP_C_289'] if "SIP_C_289" in data_obj else "-"
        ##
        item['air_cooled_glove_box'] = data_obj['SIP_C_290'] if "SIP_C_290" in data_obj else "-"

        for k in item:
            try:
                item[k] = parse.unquote(item[k])
            except:
                pass

        if "-" not in item['body_color_opt']:
            temp = []
            selector = etree.fromstring(item['body_color_opt'])
            dts = selector.xpath("/dl/dt")
            for dt in dts:
                temp.append(dt.xpath("text()[1]")[0].strip())
            item['body_color_opt'] = '|'.join(temp)
            print(item['body_color_opt'])

        if "-" not in item['inner_color_opt']:
            temp = []
            selector = etree.fromstring(item['inner_color_opt'])
            dts = selector.xpath("/dl/dt")
            for dt in dts:
                temp.append(dt.xpath("text()[1]")[0].strip())
            item['inner_color_opt'] = '|'.join(temp)
            print(item['inner_color_opt'])

        yield item

        # item['soundbrand'] = scrapy.Field()
        # item['plugform'] = scrapy.Field()
        # item['SIP_T_LOGO'] = scrapy.Field()
        # item['service_cycle'] = scrapy.Field()
        # item['length'] = scrapy.Field()
        # item['mixedtype'] = scrapy.Field()
        # item['service_cost'] = scrapy.Field()
        # item['width'] = scrapy.Field()
        # item['motor_type'] = scrapy.Field()
        # item['warranty_policy'] = scrapy.Field()
        # item['collision_star'] = scrapy.Field()
        # item['in_out_rearview'] = scrapy.Field()
        # item['model_engine_type'] = scrapy.Field()
        # item['SIP_C_ISELECTRIC'] = scrapy.Field()
        # item['wheelbase'] = scrapy.Field()
        # item['overseas'] = scrapy.Field()
        # item['SIP_T_PRICE'] = scrapy.Field()
        # item['fog_lights'] = scrapy.Field()
        # item['SIP_T_ID'] = scrapy.Field()
        # item['SIP_T_GEAR'] = scrapy.Field()
        # item['body_structure'] = scrapy.Field()
        # item['door'] = scrapy.Field()
        # item['seat'] = scrapy.Field()
        # item['tank_volume'] = scrapy.Field()
        # item['thansfertype'] = scrapy.Field()
        # item['SIP_C_329'] = scrapy.Field()
        # item['steering'] = scrapy.Field()
        # item['central_differential'] = scrapy.Field()
        # item['SIP_T_MODELNAME'] = scrapy.Field()
        # ##
        # item['CD_DVD'] = scrapy.Field()
        # item['air_conditioning'] = scrapy.Field()
        # item['SIP_T_FUELCOST_USER'] = scrapy.Field()
        # item['ABS'] = scrapy.Field()
        # item['SIP_T_KOUBEI_SCORE'] = scrapy.Field()
        # item['SIP_C_283'] = scrapy.Field()
        # ##
        # item['dipped_headlight'] = scrapy.Field()
        # item['gear'] = scrapy.Field()
        # item['rear_seat_adjust'] = scrapy.Field()
        # item['f_b_central_armrest'] = scrapy.Field()
        # item['rear_diffuser'] = scrapy.Field()
        # item['SIP_C_319'] = scrapy.Field()
        # item['childlock'] = scrapy.Field()
        # item['maker_name'] = scrapy.Field()
        # item['LATCH'] = scrapy.Field()
        # item['level'] = scrapy.Field()
        # item['SIP_T_PV'] = scrapy.Field()
        # item['skylight'] = scrapy.Field()
        # item['body'] = scrapy.Field()
        # item['SIP_C_315'] = scrapy.Field()
        # item['motor'] = scrapy.Field()
        # item['battery'] = scrapy.Field()
        # item['ISOFIX'] = scrapy.Field()
        # item['guideprice'] = scrapy.Field()
        # ##
        # item['shop4s_price'] = scrapy.Field()
        # item['oil_consumption'] = scrapy.Field()
        # item['alimentation'] = scrapy.Field()
        # item['maxps'] = scrapy.Field()
        # item['body_color_opt'] = scrapy.Field()
        # item['l_w_h'] = scrapy.Field()
        # item['cylinder_material'] = scrapy.Field()
        # item['cylinder_body_material'] = scrapy.Field()
        # item['inter_color_opt'] = scrapy.Field()
        # item['SIP_T_DISPL'] = scrapy.Field()
        # item['gear_shift_tpye'] = scrapy.Field()
        # item['block'] = scrapy.Field()
        # item['gear_name'] = scrapy.Field()
        # item['emission'] = scrapy.Field()
        # item['maxpower'] = scrapy.Field()
        # item['maxnm'] = scrapy.Field()
        # item['drivemode'] = scrapy.Field()
        # item['seat_material'] = scrapy.Field()
        # item['front_suspension'] = scrapy.Field()
        # item['back_suspension'] = scrapy.Field()
        # item['chassis_structure'] = scrapy.Field()
        # item['front_tire'] = scrapy.Field()
        # item['back_tire'] = scrapy.Field()
        # item['wheel_material'] = scrapy.Field()
        # item['nameDomain'] = scrapy.Field()
        # item['front_brake'] = scrapy.Field()
        # item['spare_tire'] = scrapy.Field()
        # item['park_brake'] = scrapy.Field()
        # item['back_brake'] = scrapy.Field()
        # item['SIP_T_DEALERPRICE_DROP'] = scrapy.Field()
        # item['SIP_T_MODELID'] = scrapy.Field()
        # item['SIP_T_STA'] = scrapy.Field()
        # item['SIP_C_335'] = scrapy.Field()
        # item['SIP_C_333'] = scrapy.Field()
        # item['SIP_C_334'] = scrapy.Field()
        # item['SIP_C_332'] = scrapy.Field()
        # item['SIP_T_YEAR'] = scrapy.Field()
        # item['SIP_C_330'] = scrapy.Field()
        # item['cylinder_num'] = scrapy.Field()
        # item['workingtype'] = scrapy.Field()
        # item['cylinder_capacity'] = scrapy.Field()
        # item['output2'] = scrapy.Field()
        # item['motortype'] = scrapy.Field()
        # item['desc_motor'] = scrapy.Field()
        # item['SIP_T_FUELCOST_COMP'] = scrapy.Field()
        # item['SIP_T_KOUBEI_COUNT'] = scrapy.Field()
        # item['speaker_num'] = scrapy.Field()
        # item['cylinder_range'] = scrapy.Field()
        # item['each_cylinder_num'] = scrapy.Field()
        # item['high_lights'] = scrapy.Field()
        # item['valve'] = scrapy.Field()
        # item['brandNameDomain'] = scrapy.Field()
        # item['fuel'] = scrapy.Field()
        # item['lpower'] = scrapy.Field()
        # item['SIP_T_NAME'] = scrapy.Field()
        # item['SIP_C_241'] = scrapy.Field()
        # item['m_d_airbag'] = scrapy.Field()
        # item['doubling_auxiliary'] = scrapy.Field()
        # item['HDC'] = scrapy.Field()
        # item['autoparking'] = scrapy.Field()
        # item['car_central_lock'] = scrapy.Field()
        # item['motorguard'] = scrapy.Field()
        # item['keylessgo'] = scrapy.Field()
        # ##
        # item['remote_key'] = scrapy.Field()
        # item['zero_tire'] = scrapy.Field()
        # item['tire_pressure'] = scrapy.Field()
        # item['activebrake'] = scrapy.Field()
        # item['SIP_C_302'] = scrapy.Field()
        # item['SIP_C_177'] = scrapy.Field()
        # item['SIP_C_178'] = scrapy.Field()
        # item['SIP_C_179'] = scrapy.Field()
        # item['air_suspension'] = scrapy.Field()
        # item['adaptive_cruise'] = scrapy.Field()
        # item['cruise_control'] = scrapy.Field()
        # item['f_b_reversing_radar'] = scrapy.Field()
        # item['adjust_suspension'] = scrapy.Field()
        # item['SIP_C_327'] = scrapy.Field()
        # item['SIP_C_326'] = scrapy.Field()
        # item['back_differential'] = scrapy.Field()
        # item['front_differential'] = scrapy.Field()
        # item['centr_diff_lock'] = scrapy.Field()
        # item['ASR'] = scrapy.Field()
        # item['ESP'] = scrapy.Field()
        # item['EBA'] = scrapy.Field()
        # item['EBD'] = scrapy.Field()
        # item['belt'] = scrapy.Field()
        # item['knee_airbag'] = scrapy.Field()
        # item['SIP_C_182'] = scrapy.Field()
        # item['SIP_C_181'] = scrapy.Field()
        # item['SIP_C_180'] = scrapy.Field()
        # item['SIP_C_206'] = scrapy.Field()
        # item['nightvision'] = scrapy.Field()
        # item['pancamera'] = scrapy.Field()
        # item['autoparking_place'] = scrapy.Field()
        # item['reversing_image'] = scrapy.Field()
        # item['SIP_C_201'] = scrapy.Field()
        # item['HUD'] = scrapy.Field()
        # item['glove_box'] = scrapy.Field()
        # item['SIP_C_209'] = scrapy.Field()
        # item['SIP_C_208'] = scrapy.Field()
        # item['SIP_C_207'] = scrapy.Field()
        # item['f_b_massage_chairs'] = scrapy.Field()
        # item['SIP_C_259'] = scrapy.Field()
        # item['MMI'] = scrapy.Field()
        # item['Carwings'] = scrapy.Field()
        # item['GPS'] = scrapy.Field()
        # item['back_LCD_panel'] = scrapy.Field()
        # item['carTV'] = scrapy.Field()
        # item['panel_LCD_screen'] = scrapy.Field()
        # item['bluetooth'] = scrapy.Field()
        # item['acceleration'] = scrapy.Field()
        # item['top_speed'] = scrapy.Field()
        # item['air_curtain'] = scrapy.Field()
        # item['m_d_electric_adjust'] = scrapy.Field()
        # item['f_b_chair_cloud'] = scrapy.Field()
        # item['keytowindows'] = scrapy.Field()
        # item['inside_lights'] = scrapy.Field()
        # item['clear_headlights'] = scrapy.Field()
        # item['SIP_C_268'] = scrapy.Field()
        # item['SIP_C_267'] = scrapy.Field()
        # item['auto_headlights'] = scrapy.Field()
        # item['f_b_windows'] = scrapy.Field()
        # item['move_headlights'] = scrapy.Field()
        # item['f_b_chair_heat'] = scrapy.Field()
        # item['height_headlights'] = scrapy.Field()
        # item['rear_seat_down'] = scrapy.Field()
        # item['daytime_lights'] = scrapy.Field()
        # item['weight'] = scrapy.Field()
        # item['luggage_volume'] = scrapy.Field()
        # item['steering_adjust'] = scrapy.Field()
        # item['rearview_heat'] = scrapy.Field()
        # item['rearview_adjust'] = scrapy.Field()
        # item['SIP_C_277'] = scrapy.Field()
        # item['sunshade_shade'] = scrapy.Field()
        # item['hand_protect_windows'] = scrapy.Field()
        # item['insulating_glass'] = scrapy.Field()
        # item['windshield_defrost'] = scrapy.Field()
        # item['windshield_sun'] = scrapy.Field()
        # item['induction_wiper'] = scrapy.Field()
        # item['rear_wiper'] = scrapy.Field()
        # item['air_adjust'] = scrapy.Field()
        # item['b_control_temper'] = scrapy.Field()
        # item['refrigerator'] = scrapy.Field()
        # item['rearview_fold'] = scrapy.Field()
        # item['SIP_C_284'] = scrapy.Field()
        # item['f_control_temper'] = scrapy.Field()
        # item['steering_electric_adjust'] = scrapy.Field()
        # item['multisteering'] = scrapy.Field()
        # item['SIP_C_214'] = scrapy.Field()
        # item['SIP_C_215'] = scrapy.Field()
        # item['electric_door'] = scrapy.Field()
        # item['leather_steering'] = scrapy.Field()
        # item['motionsuite'] = scrapy.Field()
        # item['chargingtype'] = scrapy.Field()
        # item['motor_num'] = scrapy.Field()
        # item['charging_comp'] = scrapy.Field()
        # item['steeringshift'] = scrapy.Field()
        # item['HAC'] = scrapy.Field()
        # item['computer_screen'] = scrapy.Field()
        # item['cosmetic_mirror'] = scrapy.Field()
        # item['rearview_memory'] = scrapy.Field()
        # item['privacy_glass'] = scrapy.Field()
        # item['sports_seats'] = scrapy.Field()
        # item['seat_height_adjust'] = scrapy.Field()
        # item['lumbar_adjust'] = scrapy.Field()
        # item['shoulder_adjust'] = scrapy.Field()
        # item['baggage_light'] = scrapy.Field()
        # item['power_interface'] = scrapy.Field()
        # item['control_LCD'] = scrapy.Field()
        # item['SIP_C_229'] = scrapy.Field()
        # item['SIP_C_234'] = scrapy.Field()
        # item['SIP_C_235'] = scrapy.Field()
        # item['f_b_airbag'] = scrapy.Field()
        # item['chair_memory'] = scrapy.Field()
        # item['SIP_C_238'] = scrapy.Field()
        # item['SIP_C_239'] = scrapy.Field()
        # item['SIP_C_236'] = scrapy.Field()
        # item['roofrack'] = scrapy.Field()
        # item['SIP_C_237'] = scrapy.Field()
        # item['electric_load'] = scrapy.Field()
        # item['inductive_load'] = scrapy.Field()
        # item['keylessenter'] = scrapy.Field()
        # item['SIP_C_331'] = scrapy.Field()
        # item['SIP_C_230'] = scrapy.Field()
        # item['SIP_C_243'] = scrapy.Field()
        # item['SIP_C_244'] = scrapy.Field()
        # item['SIP_C_245'] = scrapy.Field()
        # item['SIP_C_246'] = scrapy.Field()
        # ##
        # item['CD_MP3'] = scrapy.Field()
        # item['USB'] = scrapy.Field()
        # item['rear_stand'] = scrapy.Field()
        # item['adaptive_lights'] = scrapy.Field()
        # item['assist_lights'] = scrapy.Field()
        # item['lcdpanel'] = scrapy.Field()
        # item['SIP_C_343'] = scrapy.Field()
        # item['SIP_C_344'] = scrapy.Field()
        # item['SIP_C_345'] = scrapy.Field()
        # item['steeringmemory'] = scrapy.Field()
        # item['steeringheat'] = scrapy.Field()
        # item['third_seats'] = scrapy.Field()
        # item['SIP_C_242'] = scrapy.Field()
        # item['SIP_C_280'] = scrapy.Field()
        # item['SIP_C_281'] = scrapy.Field()
        # item['min_ground'] = scrapy.Field()
        # item['min_turning'] = scrapy.Field()
        # item['SIP_C_220'] = scrapy.Field()
        # item['front_wheel'] = scrapy.Field()
        # item['back_whell'] = scrapy.Field()
        # item['compression_ratio'] = scrapy.Field()
        # item['other_configuration2'] = scrapy.Field()
        # item['other_configuration1'] = scrapy.Field()
        # item['approach_angle'] = scrapy.Field()
        # item['departure_angle'] = scrapy.Field()
        # item['max_range'] = scrapy.Field()
        # item['motortorque'] = scrapy.Field()
        # item['motorpower'] = scrapy.Field()
        # item['battery_capacity'] = scrapy.Field()
        # item['quickcharge'] = scrapy.Field()
        # item['slowcharge'] = scrapy.Field()