# -*- coding: utf-8 -*-
import scrapy
from ..items import che300
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
from hashlib import md5
import re
import json
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import csv

#https://dingjia.che300.com/app/CarDetail/getModelConfigure/70
from scrapy.conf import settings
# update_code = settings["UPDATE_CODE"]
update_code = time.strftime("%Y%m%d", time.localtime())

# website = 'che300_app_modelinfo2_update'
website = 'che300_app_modelinfo2_update'
spidername_new = 'che300_app_modelinfo2_new'
spidername_update = 'che300_app_modelinfo2_update_old'
#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]
    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider, self).__init__(*args, **kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 20000000
        self.dbname = 'usedcar_evaluation'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'
        self.part=int(part)
        self.parts=int(parts)

    def start_requests(self):
        with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        cars = []
        for model in modellist:
            i = model['salesdescid']
            print(i)
            url = 'https://dingjia.che300.com/app/CarDetail/getModelConfigure/' + str(i)
            print(url)
            if not (dfcheck(self.df, url, self.tag)):
                yield scrapy.Request(url=url, meta={"datainfo": {"salesdescid":i}}, callback=self.parse)

    def parse(self, response):
        dffile(self.fa, response.url, self.tag)
        item = che300()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['id'] = re.findall(r'\d+',response.url)[1]
        #item['salesdesc'] = response.xpath('//div[@class="main-wrap clearfix"]/h1/text()').extract_first().replace(u" - \u5168\u90e8\u53c2\u6570","")
        # item['datasave'] = response.xpath('//p/text()').extract_first()
        item['datasave'] = response.text
        temp=json.loads(item['datasave'])
        modelConfigure=temp['success']['modelConfigure']
        item['salesdesc']=temp['success']['modelInfo']['name']
        item['status'] = md5(response.url + "-" + update_code).hexdigest()
        item = dict(response.meta['datainfo'],**item)
        modelInfolist=['drive_name','model_status', 'highlight_config','name','short_name','market_date','stop_make_year','level_id','level','sname','ssname','maker_name','maker_type','star','sid','bid','brand_name','year','price','discharge_standard','gear_type','liter','liter_turbo','door_number','body_type','min_reg_year','max_reg_year','engine_power']
        for i in modelInfolist:
            item[i]=temp['success']['modelInfo'][i]

        modelConfigureList=[]
        for i in modelConfigure:
            for j in i:
                modelConfigureList.append(j)


        namedic={
            'output':u'\u6392\u91cf\uff08\u5347\uff09'
            ,'factoryname': u'\u5382\u5546'
            ,'gear':u'\u53d8\u901f\u7bb1'
            ,'petrol_test1':u'\u5e02\u533a\u5de5\u51b5\u6cb9\u8017'
            ,'petrol_test2':u'\u5e02\u90ca\u5de5\u51b5\u6cb9\u8017'
            ,'petrol':u'\u7efc\u5408\u5de5\u51b5\u6cb9\u8017'
            ,'hundred_petrol':u'\u767e\u516c\u91cc\u7b49\u901f\u6cb9\u8017'
            ,'accelerate':u'\u52a0\u901f\u65f6\u95f4'
            ,'accelerate_test':u'\u52a0\u901f\u65f6\u95f4(0\u2014100km/h)'
            ,'masspeed':u'\u6700\u9ad8\u8f66\u901f'
            ,'seats':u'\u4e58\u5458\u4eba\u6570\uff08\u533a\u95f4\uff09'
            ,'color':u'\u8f66\u8eab\u989c\u8272'
            ,'length':u'\u957f'
            ,'width':u'\u5bbd'
            ,'heigh':u'\u9ad8'
            ,'wheelbase':u'\u8f74\u8ddd'
            ,'frontgauge':u'\u524d\u8f6e\u8ddd'
            ,'backgauge':u'\u540e\u8f6e\u8ddd'
            ,'weigth':u'\u6574\u5907\u8d28\u91cf'
            ,'full_weight':u'\u6ee1\u8f7d\u8d28\u91cf'
            ,'min_ground_dis':u'\u6700\u5c0f\u79bb\u5730\u95f4\u9699'
            ,'close_angel':u'\u63a5\u8fd1\u89d2'
            ,'departure_angel':u'\u79bb\u53bb\u89d2'
            ,'baggage':u'\u884c\u674e\u53a2\u5bb9\u79ef'
            ,'baggage_compartment_cover_mode':u'\u884c\u674e\u53a2\u76d6\u5f00\u5408\u65b9\u5f0f'
            ,'baggage_open_way':u'\u884c\u674e\u53a2\u6253\u5f00\u65b9\u5f0f'
            ,'doors':u'\u8f66\u95e8\u6570'
            ,'roof_type':u'\u8f66\u9876\u578b\u5f0f'
            ,'roof_style':u'\u8f66\u7bf7\u578b\u5f0f'
            ,'movement_surround':u'\u8fd0\u52a8\u5305\u56f4'
            ,'sport_appearance_suite':u'\u8fd0\u52a8\u5916\u89c2\u5957\u4ef6'
            ,'engine_position':u'\u53d1\u52a8\u673a\u4f4d\u7f6e'
            ,'engine_type':u'\u53d1\u52a8\u673a\u578b\u53f7'
            ,'output1':u'\u6392\u91cf(L)'
            ,'cylinder':u'\u6392\u91cf'
            ,'method':u'\u8fdb\u6c14\u5f62\u5f0f'
            ,'lwv':u'\u6c14\u7f38\u6392\u5217\u578b\u5f0f'
            ,'lwvnumber':u'\u6c7d\u7f38\u6570'
            ,'valve':u'\u6bcf\u7f38\u6c14\u95e8\u6570'
            ,'valve_mechanism':u'\u6c14\u95e8\u7ed3\u6784'
            ,'compress':u'\u538b\u7f29\u6bd4'
            ,'boremm':u'\u7f38\u5f84'
            ,'strokemm':u'\u884c\u7a0b'
            ,'maxps':u'\u6700\u5927\u9a6c\u529b'
            ,'maxpower':u'\u6700\u5927\u529f\u7387-\u529f\u7387\u503c'
            ,'maxrpm':u'\u6700\u5927\u529f\u7387-\u8f6c\u901f'
            ,'maxnm':u'\u6700\u5927\u626d\u77e9-\u626d\u77e9\u503c'
            ,'maxtorque':u'\u6700\u5927\u626d\u77e9\u2014\u8f6c\u901f'
            ,'engine_technology':u'\u7279\u6709\u6280\u672f'
            # ,'fueltyp1e':u'\u71c3\u6599\u7c7b\u578b'
            ,'fueltype':u"\u80fd\u6e90\u7c7b\u578b"
            ,'fuelmethod':u'\u4f9b\u6cb9\u65b9\u5f0f'
            ,'fulevolumn':u'\u71c3\u6cb9\u7bb1\u5bb9\u79ef'
            ,'head_port':u'\u7f38\u76d6\u6750\u6599'
            ,'cylinder_material':u'\u7f38\u4f53\u6750\u6599'
            ,'emission':u'\u73af\u4fdd\u6807\u51c6'
            ,'gear1':u'\u53d8\u901f\u7bb1'
            ,'shift_paddles':u'\u6362\u6863\u62e8\u7247'
            ,'body_structure':u'\u8f66\u4f53\u7ed3\u6784'
            ,'minimum_turning_radius':u'\u6700\u5c0f\u8f6c\u5f2f\u534a\u5f84'
            ,'power_steering':u'\u8f6c\u5411\u52a9\u529b'
            ,'frontbrake':u'\u524d\u5236\u52a8\u7c7b\u578b'
            ,'backbrake':u'\u540e\u5236\u52a8\u7c7b\u578b'
            ,'handbrake':u'\u624b\u5239\u7c7b\u578b'
            ,'driveway':u'\u9a71\u52a8\u65b9\u5f0f'
            ,'aimatic':u'\u7a7a\u6c14\u60ac\u6302'
            ,'fronthang':u'\u524d\u60ac\u6302\u7c7b\u578b'
            ,'backhang':u'\u540e\u60ac\u6302\u7c7b\u578b'
            ,'driver_codrive_airbag':u'\u9a7e\u9a76\u4f4d\u5b89\u5168\u6c14\u56ca'
            ,'driver_codrive_airbag1':u'\u526f\u9a7e\u9a76\u4f4d\u5b89\u5168\u6c14\u56ca'
            ,'front_back_side_airbag':u'\u524d\u6392\u4fa7\u5b89\u5168\u6c14\u56ca'
            ,'front_back_head_airbag':u'\u524d\u6392\u5934\u90e8\u6c14\u56ca(\u6c14\u5e18)'
            ,'knee_airbag':u'\u819d\u90e8\u6c14\u56ca'
            ,'front_back_side_airbag1':u'\u540e\u6392\u4fa7\u5b89\u5168\u6c14\u56ca'
            ,'front_back_head_airbag1':u'\u540e\u6392\u5934\u90e8\u6c14\u56ca(\u6c14\u5e18)'
            ,'safety_belt_is_not_prompt':u'\u5b89\u5168\u5e26\u672a\u7cfb\u63d0\u793a'
            ,'seats_belt_force_limiter':u'\u5b89\u5168\u5e26\u9650\u529b\u529f\u80fd'
            ,'belt_tightening_function':u'\u5b89\u5168\u5e26\u9884\u6536\u7d27\u529f\u80fd'
            ,'front_belt_adjust':u'\u524d\u5b89\u5168\u5e26\u8c03\u8282'
            ,'back_belt':u'\u540e\u6392\u5b89\u5168\u5e26'
            ,'back_row_threepoint_belt':u'\u540e\u6392\u4e2d\u95f4\u4e09\u70b9\u5f0f\u5b89\u5168\u5e26'
            ,'electronic_speed_limit':u'\u7535\u5b50\u9650\u901f'
            ,'tire_pressure_monitoring':u'\u80ce\u538b\u76d1\u6d4b\u88c5\u7f6e'
            ,'zero_tire_pressure':u'\u96f6\u538b\u7eed\u884c(\u96f6\u80ce\u538b\u7ee7\u7eed\u884c\u9a76)'
            ,'Collapsible_steering_column':u'\u53ef\u6e83\u7f29\u8f6c\u5411\u67f1'
            ,'central_lock':u'\u8f66\u5185\u4e2d\u63a7\u9501'
            ,'central_door_lock':u'\u4e2d\u63a7\u95e8\u9501'
            ,'children_lock':u'\u513f\u7ae5\u9501'
            ,'remote_control_key':u'\u9065\u63a7\u94a5\u5319'
            ,'keyless_start_system':u'\u65e0\u94a5\u5319\u542f\u52a8\u7cfb\u7edf'
            ,'engine_electronic_control_unit':u'\u53d1\u52a8\u673a\u7535\u5b50\u9632\u76d7'
            ,'frontwheel':u'\u524d\u8f6e\u80ce\u89c4\u683c'
            ,'backwheel':u'\u540e\u8f6e\u80ce\u89c4\u683c'
            ,'fronthub':u'\u524d\u8f6e\u6bc2\u89c4\u683c'
            ,'backhub':u'\u540e\u8f6e\u6bc2\u89c4\u683c'
            ,'sparewheel':u'\u5907\u80ce\u7c7b\u578b'
            ,'hubmaterial':u'\u8f6e\u6bc2\u6750\u6599'
            ,'abs_antilock':u'ABS(\u5239\u8f66\u9632\u62b1\u6b7b\u5236\u52a8\u7cfb\u7edf)'
            ,'braking_force_distribution_ebd_cbc':u'\u7535\u5b50\u5236\u52a8\u529b\u5206\u914d\u7cfb\u7edf'
            ,'brake_assist_eba_bas_ba':u'EBA/EVA(\u7d27\u6025\u5236\u52a8\u8f85\u52a9\u7cfb\u7edf)'
            ,'traction_control_system_asr_tcs_trc':u'TCS(\u7275\u5f15\u529b\u63a7\u5236\u7cfb\u7edf)'
            ,'vehicle_stability_control_esp_dsc_vsc':u'DSC(\u52a8\u6001\u7a33\u5b9a\u63a7\u5236\u7cfb\u7edf)'
            ,'EPS':u'\u968f\u901f\u52a9\u529b\u8f6c\u5411\u8c03\u8282(EPS)'
            ,'automatic_parking':u'\u81ea\u52a8\u9a7b\u8f66'
            ,'hill_start_assist':u'\u4e0a\u5761\u8f85\u52a9'
            ,'hill_descent_control':u'\u9661\u5761\u7f13\u964d'
            ,'backing_radar':u'\u6cca\u8f66\u96f7\u8fbe(\u8f66\u524d)'
            ,'baking_radar1':u'\u5012\u8f66\u96f7\u8fbe'
            ,'rear_video_monitor':u'\u5012\u8f66\u5f71\u50cf'
            ,'panoramic_camera':u'\u5168\u666f\u6444\u50cf\u5934'
            ,'cruise_control':u'\u5b9a\u901f\u5de1\u822a\u7cfb\u7edf'
            ,'adaptive_cruise':u'\u81ea\u9002\u5e94\u5de1\u822a'
            ,'gps_navigation':u'GPS\u7535\u5b50\u5bfc\u822a'
            ,'human_computer_interaction_system':u'\u4eba\u673a\u4ea4\u4e92\u7cfb\u7edf'
            ,'park_assist':u'\u81ea\u52a8\u6cca\u8f66\u5165\u4f4d'
            ,'abls':u'\u4e3b\u52a8\u5239\u8f66/\u4e3b\u52a8\u5b89\u5168\u7cfb\u7edf'
            ,'active_front_steering':u'\u6574\u4f53\u4e3b\u52a8\u8f6c\u5411\u7cfb\u7edf'
            ,'night_vision':u'\u591c\u89c6\u7cfb\u7edf'
            ,'blind_spot_detecttion':u'\u76f2\u70b9\u68c0\u6d4b'
            ,'front_rear_lectric_windows':u'\u8f66\u7a97'
            ,'windows':u'\u8f66\u7a97'
            ,'window_clip_hand_safety':u'\u7535\u52a8\u7a97\u9632\u5939\u529f\u80fd'
            ,'skylight_opening_and_closing_mode':u'\u5929\u7a97\u5f00\u5408\u65b9\u5f0f'
            ,'skylight_type':u'\u5929\u7a97\u578b\u5f0f'
            ,'backglass_sunshade':u'\u540e\u7a97\u906e\u9633\u5e18'
            ,'backsideglass_sunshade':u'\u540e\u6392\u4fa7\u906e\u9633\u5e18'
            ,'rear_windshield_wiper':u'\u540e\u96e8\u5237\u5668'
            ,'rain_sensor':u'\u96e8\u5237\u4f20\u611f\u5668'
            ,'electric_door':u'\u7535\u52a8\u5438\u5408\u95e8'
            ,'Rearview_m_with_sideturuning_light':u'\u540e\u89c6\u955c\u5e26\u4fa7\u8f6c\u5411\u706f'
            ,'rearview_mirror_memory':u'\u5916\u540e\u89c6\u955c\u8bb0\u5fc6\u529f\u80fd'
            ,'rearview_mirror_heating':u'\u5916\u540e\u89c6\u955c\u52a0\u70ed\u529f\u80fd'
            ,'rearview_mirror_electric_folding':u'\u5916\u540e\u89c6\u955c\u7535\u52a8\u6298\u53e0\u529f\u80fd'
            ,'rearview_mirror_electric_adjustment':u'\u5916\u540e\u89c6\u955c\u7535\u52a8\u8c03\u8282'
            ,'rearview_mirror_auto_anti_glare':u'\u5185\u540e\u89c6\u955c\u9632\u7729\u76ee\u529f\u80fd'
            ,'visor__mirror':u'\u906e\u9633\u677f\u5316\u5986\u955c'
            ,'headlamp_type':u'\u524d\u7167\u706f\u7c7b\u578b'
            ,'headlight_automatic_shutdown':u'\u524d\u5927\u706f\u81ea\u52a8\u5f00\u95ed'
            ,'headlamp_automatic_washing_function':u'\u524d\u7167\u706f\u81ea\u52a8\u6e05\u6d17\u529f\u80fd'
            ,'headlamp_following_steering':u'\u524d\u5927\u706f\u968f\u52a8\u8f6c\u5411'
            ,'headlamp_heigth_adjust':u'\u524d\u7167\u706f\u7167\u5c04\u9ad8\u5ea6\u8c03\u8282'
            ,'antifog_ligths':u'\u524d\u96fe\u706f'
            ,'body_read_light':u'\u8f66\u53a2\u524d\u9605\u8bfb\u706f'
            ,'body_read_back_light':u'\u8f66\u53a2\u540e\u9605\u8bfb\u706f'
            ,'inside_atmosphere_lights':u'\u8f66\u5185\u6c1b\u56f4\u706f'
            ,'daytime__lights':u'\u65e5\u95f4\u884c\u8f66\u706f'
            ,'taillight':u'LED\u5c3e\u706f'
            ,'height_third_brakelight':u'\u9ad8\u4f4d(\u7b2c\u4e09)\u5236\u52a8\u706f'
            ,'corner_lamp':u'\u8f6c\u5411\u5934\u706f\uff08\u8f85\u52a9\u706f\uff09'
            ,'steering_headlights':u'\u4fa7\u8f6c\u5411\u706f'
            ,'luggage_compartment_light':u'\u884c\u674e\u53a2\u706f'
            ,'steering_wheel_adjustment':u'\u65b9\u5411\u76d8\u524d\u540e\u8c03\u8282'
            ,'steering_wheel_adjustment1':u'\u65b9\u5411\u76d8\u4e0a\u4e0b\u8c03\u8282'
            ,'steering_wheel_adjustment_type':u'\u65b9\u5411\u76d8\u8c03\u8282\u65b9\u5f0f'
            ,'steering_wheel_surface_material':u'\u65b9\u5411\u76d8\u8868\u9762\u6750\u6599'
            ,'multi_function_steering_wheel':u'\u591a\u529f\u80fd\u65b9\u5411\u76d8'
            ,'multi_function_steering_wheel_function':u'\u591a\u529f\u80fd\u65b9\u5411\u76d8\u529f\u80fd'
            ,'computer_screen_of_driving':u'\u884c\u8f66\u7535\u8111\u663e\u793a\u5c4f'
            ,'heads_up_display':u'HUD\u62ac\u5934\u6570\u5b57\u663e\u793a'
            ,'interior_color':u'\u5185\u9970\u989c\u8272'
            ,'rear_row_hang_cup':u'\u540e\u6392\u676f\u67b6'
            ,'car_power_supply_voltage':u'\u8f66\u5185\u7535\u6e90\u7535\u538b'
            ,'sports_seats':u'\u8fd0\u52a8\u5ea7\u6905'
            ,'seats_fabric':u'\u5ea7\u6905\u9762\u6599'
            ,'driver_seat_electric_adjustment':u'\u9a7e\u9a76\u5ea7\u5ea7\u6905\u8c03\u8282\u65b9\u5f0f'
            ,'driver_seat_electric_adjustment1':u'\u526f\u9a7e\u9a76\u5ea7\u6905\u8c03\u8282\u65b9\u5f0f'
            ,'adjustable_lumbar_support':u'\u9a7e\u9a76\u5ea7\u8170\u90e8\u652f\u6491\u8c03\u8282'
            ,'adjustable_shoulder_support':u'\u9a7e\u9a76\u5ea7\u80a9\u90e8\u652f\u6491\u8c03\u8282'
            ,'seat_armrest':u'\u524d\u5ea7\u4e2d\u592e\u6276\u624b'
            ,'seat_armrest1':u'\u540e\u5ea7\u4e2d\u592e\u6276\u624b'
            ,'seat_ventilation':u'\u5ea7\u6905\u901a\u98ce'
            ,'front_back_seat_heating':u'\u9a7e\u9a76\u5ea7\u5ea7\u6905\u52a0\u70ed'
            ,'massage_seat':u'\u5ea7\u6905\u6309\u6469\u529f\u80fd'
            ,'electric_chair_memory':u'\u7535\u52a8\u5ea7\u6905\u8bb0\u5fc6'
            ,'children_safty_chair_fixed_device':u'\u513f\u7ae5\u5b89\u5168\u5ea7\u6905\u56fa\u5b9a\u88c5\u7f6e'
            ,'third_row_seats':u'\u7b2c\u4e09\u6392\u5ea7\u6905'
            ,'interactive_location_services':u'\u5b9a\u4f4d\u4e92\u52a8\u670d\u52a1'
            ,'bluetooth_car_phone':u'\u8f66\u8f7d\u7535\u8bdd'
            ,'bluetooth_car_phone1':u'\u84dd\u7259\u7cfb\u7edf'
            ,'interior_harddisk':u'\u5185\u7f6e\u786c\u76d8'
            ,'onboard_tv':u'\u8f66\u8f7d\u7535\u89c6'
            ,'speakers_number':u'\u626c\u58f0\u5668\u6570\u91cf'
            ,'DVD':u'DVD'
            ,'single_cd_player':u'CD'
            ,'color_screen_display_control':u'\u4e2d\u63a7\u53f0\u6db2\u6676\u5c4f'
            ,'rear_lcd_screen':u'\u540e\u6392\u6db2\u6676\u663e\u793a\u5668'
            ,'auto_ac':u'\u7a7a\u8c03\u63a7\u5236\u65b9\u5f0f'
            ,'zone_temperature_control':u'\u6e29\u5ea6\u5206\u533a\u63a7\u5236'
            ,'rear_independent_ac':u'\u540e\u6392\u72ec\u7acb\u7a7a\u8c03'
            ,'rear_ac':u'\u540e\u6392\u51fa\u98ce\u53e3'
            ,'ac_pollen_filter':u'\u7a7a\u6c14\u8c03\u8282/\u82b1\u7c89\u8fc7\u6ee4'
            ,'car_refrigerator':u'\u8f66\u8f7d\u51b0\u7bb1'
            ,'accelerate1':u'\u52a0\u901f\u65f6\u95f4(0\u2014100km/h)'
            , 'allowance': u'\u56fd\u5bb6/\u5730\u533a\u8865\u52a9(\u5143)'
            , 'motor_type': u'\u7535\u673a\u7c7b\u578b'
            , 'total_power_EV': u'\u7535\u52a8\u673a\u603b\u529f\u7387(kW)'
            , 'total_torque_EV': u'\u7535\u52a8\u673a\u603b\u626d\u77e9(N\u00b7m)'
            , 'front_peak_power_EV': u'\u524d\u7535\u52a8\u673a\u6700\u5927\u529f\u7387(kW)'
            , 'front_peak_torque_EV': u'\u524d\u7535\u52a8\u673a\u6700\u5927\u626d\u77e9(N\u00b7m)'
            , 'rear_peak_power_EV': u'\u540e\u7535\u52a8\u673a\u6700\u5927\u529f\u7387(kW)'
            , 'rear_peak_torque_EV': u'\u540e\u7535\u52a8\u673a\u6700\u5927\u626d\u77e9(N\u00b7m)'
            , 'vehicle_power': u'\u7cfb\u7edf\u7efc\u5408\u529f\u7387(kW)'
            , 'vehicle_torque': u'\u7cfb\u7edf\u7efc\u5408\u626d\u77e9(N\u00b7m)'
            , 'battery_type': u'\u7535\u6c60\u7c7b\u578b'
            , 'battery_range_MIIT': u'\u5de5\u4fe1\u90e8\u7eed\u822a\u91cc\u7a0b(km)'
            , 'battery_capacity': u'\u7535\u6c60\u5bb9\u91cf(kWh)'
            , 'power_consumption': u'\u767e\u516c\u91cc\u8017\u7535\u91cf(kWh/100km)'
            , 'battery_pack_warrenty': u'\u7535\u6c60\u7ec4\u8d28\u4fdd'
            , 'charging_time': u'\u7535\u6c60\u5145\u7535\u65f6\u95f4'
            , 'fast_charge_electricity': u'\u5feb\u5145\u7535\u91cf(%)'
            , 'charging_pile_price': u'\u5145\u7535\u6869\u4ef7\u683c',}

        # namedic2={
        #     'factoryname':u'\u5382\u5546'
        #     ,'level':u'\u7ea7\u522b'
        #     ,'engine':u'\u53d1\u52a8\u673a'
        #     ,'geardesc':u'\u53d8\u901f\u7bb1'
        #     ,'bodystyle':u'\u8f66\u8eab\u7ed3\u6784'
        #     ,'masspeed':u'\u6700\u9ad8\u8f66\u901f(km/h)'
        #     ,'accelerate':u'\u5b98\u65b90-100km/h\u52a0\u901f(s)'
        #     ,'accelerate_test':u'\u5b9e\u6d4b0-100km/h\u52a0\u901f(s)'
        #     ,'brake_test':u'\u5b9e\u6d4b100-0km/h\u5236\u52a8(m)'
        #     ,'petrol_test':u'\u5b9e\u6d4b\u6cb9\u8017(L/100km)'
        #     ,'petrol':u'\u5de5\u4fe1\u90e8\u7efc\u5408\u6cb9\u8017(L/100km)'
        #     ,'ground_distance_test':u'\u5b9e\u6d4b\u79bb\u5730\u95f4\u9699(mm)'
        #     ,'vehicle_warranty ':u'\u6574\u8f66\u8d28\u4fdd'
        #     ,'length':u'\u957f\u5ea6(mm)'
        #     ,'width':
        # }
        namedic2 = {'front_back_head_airbag': u'\u524d/\u540e\u6392\u5934\u90e8\u6c14\u56ca(\u6c14\u5e18)'
            , 'central_lock': u'\u8f66\u5185\u4e2d\u63a7\u9501'
            , 'keyless_start_system': u'\u65e0\u94a5\u5319\u542f\u52a8\u7cfb\u7edf'
            , 'safety_belt_is_not_prompt': u'\u5b89\u5168\u5e26\u672a\u7cfb\u63d0\u793a'
            , 'engine_electronic_control_unit': u'\u53d1\u52a8\u673a\u7535\u5b50\u9632\u76d7'
            , 'remote_control_key': u'\u9065\u63a7\u94a5\u5319'
            , 'zero_tire_pressure': u'\u96f6\u80ce\u538b\u7ee7\u7eed\u884c\u9a76'
            , 'isofix_child_seat_interface': u'ISOFIX\u513f\u7ae5\u5ea7\u6905\u63a5\u53e3'
            , 'knee_airbag': u'\u819d\u90e8\u6c14\u56ca'
            , 'driver_codrive_airbag': u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u5b89\u5168\u6c14\u56ca'
            , 'pke': u'\u65e0\u94a5\u5319\u8fdb\u5165\u7cfb\u7edf'
            , 'tire_pressure_monitoring': u'\u80ce\u538b\u76d1\u6d4b\u88c5\u7f6e'
            , 'front_back_side_airbag': u'\u524d/\u540e\u6392\u4fa7\u6c14\u56ca'
            , 'geartype': u'\u53d8\u901f\u7bb1'
            , 'gear':u'\u7b80\u79f0'
            , 'gearnumber': u'\u6321\u4f4d\u4e2a\u6570'
            , 'geardesc': u'\u53d8\u901f\u7bb1\u7c7b\u578b'
            , 'rearview_mirror_electric_folding': u'\u540e\u89c6\u955c\u7535\u52a8\u6298\u53e0'
            , 'rearview_mirror_memory': u'\u540e\u89c6\u955c\u8bb0\u5fc6'
            , 'window_clip_hand_safety': u'\u8f66\u7a97\u9632\u5939\u624b\u529f\u80fd'
            , 'rearview_mirror_electric_adjustment': u'\u540e\u89c6\u955c\u7535\u52a8\u8c03\u8282'
            , 'visor__mirror': u'\u906e\u9633\u677f\u5316\u5986\u955c'
            , 'back_privacy_glass': u'\u540e\u6392\u4fa7\u9690\u79c1\u73bb\u7483'
            , 'rearview_mirror_auto_anti_glare': u'\u5185/\u5916\u540e\u89c6\u955c\u81ea\u52a8\u9632\u7729\u76ee'
            , 'backglass_sunshade': u'\u540e\u98ce\u6321\u906e\u9633\u5e18'
            , 'windshield_wiper_sensor': u'\u611f\u5e94\u96e8\u5237'
            , 'rear_windshield_wiper': u'\u540e\u96e8\u5237'
            , 'insulating_glass': u'\u9632\u7d2b\u5916\u7ebf/\u9694\u70ed\u73bb\u7483'
            , 'backsideglass_sunshade': u'\u540e\u6392\u4fa7\u906e\u9633\u5e18'
            , 'rearview_mirror_heating': u'\u540e\u89c6\u955c\u52a0\u70ed'
            , 'front_rear_lectric_windows': u'\u524d/\u540e\u7535\u52a8\u8f66\u7a97'
            , 'brake_assist_eba_bas_ba': u'\u5239\u8f66\u8f85\u52a9(EBA/BAS/BA\u7b49)'
            , 'hill_descent_control': u'\u9661\u5761\u7f13\u964d'
            , 'back_vaq': u'\u540e\u6865\u9650\u6ed1\u5dee\u901f\u5668/\u5dee\u901f\u9501'
            , 'vehicle_stability_control_esp_dsc_vsc': u'\u8f66\u8eab\u7a33\u5b9a\u63a7\u5236(ESC/ESP/DSC\u7b49)'
            , 'aimatic': u'\u7a7a\u6c14\u60ac\u67b6'
            , 'front_vaq': u'\u524d\u6865\u9650\u6ed1\u5dee\u901f\u5668/\u5dee\u901f\u9501'
            , 'hill_start_assist': u'\u4e0a\u5761\u8f85\u52a9'
            , 'braking_force_distribution_ebd_cbc': u'\u5236\u52a8\u529b\u5206\u914d(EBD/CBC\u7b49)'
            , 'variable_suspension': u'\u53ef\u53d8\u60ac\u67b6'
            , 'automatic_parking': u'\u81ea\u52a8\u9a7b\u8f66'
            , 'limited_slip_differential': u'\u4e2d\u592e\u5dee\u901f\u5668\u9501\u6b62\u529f\u80fd'
            , 'variable_gear_steering_ratio': u'\u53ef\u53d8\u8f6c\u5411\u6bd4'
            , 'traction_control_system_asr_tcs_trc': u'\u7275\u5f15\u529b\u63a7\u5236(ASR/TCS/TRC\u7b49)'
            , 'abs_antilock': u'ABS\u9632\u62b1\u6b7b'
            , 'parking_brake_type': u'\u9a7b\u8f66\u5236\u52a8\u7c7b\u578b'
            , 'frontbrake': u'\u524d\u5236\u52a8\u5668\u7c7b\u578b'
            , 'backbrake': u'\u540e\u5236\u52a8\u5668\u7c7b\u578b'
            , 'sparewheel': u'\u5907\u80ce\u89c4\u683c'
            , 'frontwheel': u'\u524d\u8f6e\u80ce\u89c4\u683c'
            , 'backwheel': u'\u540e\u8f6e\u80ce\u89c4\u683c'
            , 'length': u'\u957f\u5ea6(mm)'
            , 'baggage': u'\u884c\u674e\u53a2\u5bb9\u79ef(L)'
            , 'seats': u'\u5ea7\u4f4d\u6570(\u4e2a)'
            , 'min_ground_distance': u'\u6700\u5c0f\u79bb\u5730\u95f4\u9699(mm)'
            , 'doors': u'\u8f66\u95e8\u6570(\u4e2a)'
            , 'frontgauge': u'\u524d\u8f6e\u8ddd(mm)'
            , 'heigh': u'\u9ad8\u5ea6(mm)'
            , 'wheelbase': u'\u8f74\u8ddd(mm)'
            , 'backgauge': u'\u540e\u8f6e\u8ddd(mm)'
            , 'weigth': u'\u6574\u5907\u8d28\u91cf(kg)'
            , 'width': u'\u5bbd\u5ea6(mm)'
            , 'fulevolumn': u'\u6cb9\u7bb1\u5bb9\u79ef(L)'
            , 'steering_headlights': u'\u8f6c\u5411\u5934\u706f'
            , 'Headlights_full': u'\u8fdc\u5149\u706f'
            , 'inside_atmosphere_lights': u'\u8f66\u5185\u6c1b\u56f4\u706f'
            , 'adjustable_headlight_height': u'\u5927\u706f\u9ad8\u5ea6\u53ef\u8c03'
            , 'headlight_cleaning_device': u'\u5927\u706f\u6e05\u6d17\u88c5\u7f6e'
            , 'antifog_ligths': u'\u524d\u96fe\u706f'
            , 'automatic_headlights': u'\u81ea\u52a8\u5934\u706f'
            , 'daytime__lights': u'\u65e5\u95f4\u884c\u8f66\u706f'
            , 'Headlights_dipped': u'\u8fd1\u5149\u706f'
            , 'adaptive_light_distance': u'\u81ea\u9002\u5e94\u8fdc\u8fd1\u5149'
            , 'corner_lamp': u'\u8f6c\u5411\u8f85\u52a9\u706f'
            , 'body_structure': u'\u8f66\u4f53\u7ed3\u6784'
            , 'backhang': u'\u540e\u60ac\u67b6\u7c7b\u578b'
            , 'driveway':u'\u9a71\u52a8\u65b9\u5f0f'
            , 'fronthang': u'\u524d\u60ac\u67b6\u7c7b\u578b'
            , 'assistanttype': u'\u52a9\u529b\u7c7b\u578b'
            , 'mp3_audio_support': u'CD\u652f\u6301MP3/WMA'
            , 'bluetooth_car_phone': u'\u84dd\u7259/\u8f66\u8f7d\u7535\u8bdd'
            , 'speakers_number': u'\u626c\u58f0\u5668\u6570\u91cf'
            , 'speaker_brand': u'\u626c\u58f0\u5668\u54c1\u724c'
            , 'rear_lcd_screen': u'\u540e\u6392\u6db2\u6676\u5c4f'
            , 'gps_navigation': u'GPS\u5bfc\u822a\u7cfb\u7edf'
            , 'power_supply': u'220V/230V\u7535\u6e90'
            , 'single_cd_player': u'\u591a\u5a92\u4f53\u7cfb\u7edf'
            , 'onboard_tv': u'\u8f66\u8f7d\u7535\u89c6'
            , 'external_audio_source_connectors': u'\u5916\u63a5\u97f3\u6e90\u63a5\u53e3'
            , 'interactive_location_services': u'\u5b9a\u4f4d\u4e92\u52a8\u670d\u52a1'
            , 'color_screen_display_control': u'\u4e2d\u63a7\u53f0\u5f69\u8272\u5927\u5c4f'
            , 'fuelmethod': u'\u4f9b\u6cb9\u65b9\u5f0f'
            , 'maxtorque': u'\u6700\u5927\u626d\u77e9\u8f6c\u901f(rpm)'
            , 'maxrpm': u'\u6700\u5927\u529f\u7387\u8f6c\u901f(rpm)'
            , 'maxps': u'\u6700\u5927\u9a6c\u529b(Ps)'
            , 'fuelnumber': u'\u71c3\u6cb9\u6807\u53f7'
            , 'fueltype': u'\u80fd\u6e90\u7c7b\u578b'
            , 'strokemm': u'\u884c\u7a0b(mm)'
            , 'lwvnumber': u'\u6c14\u7f38\u6570(\u4e2a)'
            , 'valve': u'\u6bcf\u7f38\u6c14\u95e8\u6570(\u4e2a)'
            , 'valve_mechanism': u'\u914d\u6c14\u673a\u6784'
            , 'emission': u'\u73af\u4fdd\u6807\u51c6'
            , 'boremm': u'\u7f38\u5f84(mm)'
            , 'maxpower': u'\u6700\u5927\u529f\u7387(kW)'
            , 'engine_technology': u'\u53d1\u52a8\u673a\u7279\u6709\u6280\u672f'
            , 'lwv': u'\u6c14\u7f38\u6392\u5217\u5f62\u5f0f'
            , 'method': u'\u8fdb\u6c14\u5f62\u5f0f'
            , 'maxnm': u'\u6700\u5927\u626d\u77e9(N\xb7m)'
            , 'cylinder_material': u'\u7f38\u4f53\u6750\u6599'
            , 'compress': u'\u538b\u7f29\u6bd4'
            , 'engine_type': u'\u53d1\u52a8\u673a\u578b\u53f7'
            , 'cylinder': u'\u6392\u91cf(mL)'
            , 'head_port': u'\u7f38\u76d6\u6750\u6599'
            , 'park_assist': u'\u81ea\u52a8\u6cca\u8f66\u5165\u4f4d'
            , 'doubling_asisst': u'\u5e76\u7ebf\u8f85\u52a9'
            , 'night_vision': u'\u591c\u89c6\u7cfb\u7edf'
            , 'ldws': u'\u8f66\u9053\u504f\u79bb\u9884\u8b66\u7cfb\u7edf'
            , 'adaptive_cruise': u'\u81ea\u9002\u5e94\u5de1\u822a'
            , 'panoramic_camera': u'\u5168\u666f\u6444\u50cf\u5934'
            , 'lcd_screen_display_control': u'\u4e2d\u63a7\u6db2\u6676\u5c4f\u5206\u5c4f\u663e\u793a'
            , 'engine_start_stop': u'\u53d1\u52a8\u673a\u542f\u505c\u6280\u672f'
            , 'abls': u'\u4e3b\u52a8\u5239\u8f66/\u4e3b\u52a8\u5b89\u5168\u7cfb\u7edf'
            , 'active_front_steering': u'\u6574\u4f53\u4e3b\u52a8\u8f6c\u5411\u7cfb\u7edf'
            , 'level': u'\u7ea7\u522b'
            , 'vehicle_warranty':u'\u6574\u8f66\u8d28\u4fdd'
            , 'bodystyle': u'\u8f66\u8eab\u7ed3\u6784'
            , 'salesdesc':u'\u8f66\u578b\u540d\u79f0'
            , 'masspeed': u'\u6700\u9ad8\u8f66\u901f(km/h)'
            # ,'price':u'\u5382\u5546\u6307\u5bfc\u4ef7(\u5143)'
            , 'output':u'\u6392\u91cf(L)'
            , 'factoryname': u'\u5382\u5546'
            , 'accelerate': u'\u5b98\u65b90-100km/h\u52a0\u901f(s)'
            , 'petrol_test': u'\u5b9e\u6d4b\u6cb9\u8017(L/100km)'
            , 'accelerate_test': u'\u5b9e\u6d4b0-100km/h\u52a0\u901f(s)'
            , 'petrol':u'\u5de5\u4fe1\u90e8\u7efc\u5408\u6cb9\u8017(L/100km)'
            , 'ground_distance_test': u'\u5b9e\u6d4b\u79bb\u5730\u95f4\u9699(mm)'
            , 'engine':u'\u53d1\u52a8\u673a'
            , 'brake_test': u'\u5b9e\u6d4b100-0km/h\u5236\u52a8(m)'
            , 'zone_temperature_control': u'\u6e29\u5ea6\u5206\u533a\u63a7\u5236'
            , 'rear_ac': u'\u540e\u5ea7\u51fa\u98ce\u53e3'
            , 'car_refrigerator': u'\u8f66\u8f7d\u51b0\u7bb1'
            , 'rear_independent_ac': u'\u540e\u6392\u72ec\u7acb\u7a7a\u8c03'
            , 'ac_pollen_filter': u'\u8f66\u5185\u7a7a\u6c14\u8c03\u8282/\u82b1\u7c89\u8fc7\u6ee4'
            , 'auto_ac': u'\u7a7a\u8c03\u63a7\u5236\u65b9\u5f0f'
            , 'computer_screen_of_driving': u'\u884c\u8f66\u7535\u8111\u663e\u793a\u5c4f'
            , 'steering_wheel_shift': u'\u65b9\u5411\u76d8\u6362\u6321'
            , 'lhz': u'\u65b9\u5411\u76d8\u52a0\u70ed'
            , 'backing_radar': u'\u524d/\u540e\u9a7b\u8f66\u96f7\u8fbe'
            , 'leather_steering_wheel': u'\u771f\u76ae\u65b9\u5411\u76d8'
            , 'steering_wheel_adjustment': u'\u65b9\u5411\u76d8\u8c03\u8282'
            , 'rear_video_monitor': u'\u5012\u8f66\u89c6\u9891\u5f71\u50cf'
            , 'memory_code': u'\u65b9\u5411\u76d8\u8bb0\u5fc6'
            , 'steering_wheel_electric_adjustment': u'\u65b9\u5411\u76d8\u7535\u52a8\u8c03\u8282'
            , 'cruise_control': u'\u5b9a\u901f\u5de1\u822a'
            , 'multi_function_steering_wheel': u'\u591a\u529f\u80fd\u65b9\u5411\u76d8'
            , 'lcd_panel': u'\u5168\u6db2\u6676\u4eea\u8868\u76d8'
            , 'heads_up_display': u'HUD\u62ac\u5934\u6570\u5b57\u663e\u793a'
            , 'induction_trunk': u'\u611f\u5e94\u540e\u5907\u53a2'
            , 'electric_sunroof': u'\u7535\u52a8\u5929\u7a97'
            , 'hubtype': u'\u94dd\u5408\u91d1\u8f6e\u5708'
            , 'panoramic_sunroof': u'\u5168\u666f\u5929\u7a97'
            , 'electric_trunk': u'\u7535\u52a8\u540e\u5907\u53a2'
            , 'sliding_door': u'\u4fa7\u6ed1\u95e8'
            , 'sport_appearance_suite': u'\u8fd0\u52a8\u5916\u89c2\u5957\u4ef6'
            , 'roof_rack': u'\u8f66\u9876\u884c\u674e\u67b6'
            , 'electric_door': u'\u7535\u52a8\u5438\u5408\u95e8'
            , 'sports_seats': u'\u8fd0\u52a8\u98ce\u683c\u5ea7\u6905'
            , 'adjustable_seat_height': u'\u5ea7\u6905\u9ad8\u4f4e\u8c03\u8282'
            , 'third_row_seats': u'\u7b2c\u4e09\u6392\u5ea7\u6905'
            , 'rear_seat_electric_adjustment': u'\u540e\u6392\u5ea7\u6905\u7535\u52a8\u8c03\u8282'
            , 'leather_seats': u'\u5ea7\u6905\u6750\u8d28'
            , 'adjustable_rear_row_backrest_angle': u'\u7b2c\u4e8c\u6392\u9760\u80cc\u89d2\u5ea6\u8c03\u8282'
            , 'rear_seat_down': u'\u540e\u6392\u5ea7\u6905\u653e\u5012\u65b9\u5f0f'
            , 'rear_row_seat_movement': u'\u7b2c\u4e8c\u6392\u5ea7\u6905\u79fb\u52a8'
            , 'seat_armrest': u'\u524d/\u540e\u4e2d\u592e\u6276\u624b'
            , 'driver_seat_electric_adjustment': u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u7535\u52a8\u8c03\u8282'
            , 'rear_row_hang_cup': u'\u540e\u6392\u676f\u67b6'
            , 'front_back_seat_heating': u'\u524d/\u540e\u6392\u5ea7\u6905\u52a0\u70ed'
            , 'seat_ventilation': u'\u524d/\u540e\u6392\u5ea7\u6905\u901a\u98ce'
            , 'electric_chair_memory': u'\u7535\u52a8\u5ea7\u6905\u8bb0\u5fc6'
            , 'adjustable_lumbar_support': u'\u8170\u90e8\u652f\u6491\u8c03\u8282'
            , 'massage_seat': u'\u524d/\u540e\u6392\u5ea7\u6905\u6309\u6469'
            , 'adjustable_shoulder_support': u'\u80a9\u90e8\u652f\u6491\u8c03\u8282'
            , 'allowance':u'\u56fd\u5bb6/\u5730\u533a\u8865\u52a9(\u5143)'
            ,'motor_type':u'\u7535\u673a\u7c7b\u578b'
            ,'total_power_EV':u'\u7535\u52a8\u673a\u603b\u529f\u7387(kW)'
            ,'total_torque_EV':u'\u7535\u52a8\u673a\u603b\u626d\u77e9(N\u00b7m)'
            ,'front_peak_power_EV':u'\u524d\u7535\u52a8\u673a\u6700\u5927\u529f\u7387(kW)'
            ,'front_peak_torque_EV':u'\u524d\u7535\u52a8\u673a\u6700\u5927\u626d\u77e9(N\u00b7m)'
            ,'rear_peak_power_EV':u'\u540e\u7535\u52a8\u673a\u6700\u5927\u529f\u7387(kW)'
            ,'rear_peak_torque_EV':u'\u540e\u7535\u52a8\u673a\u6700\u5927\u626d\u77e9(N\u00b7m)'
            ,'vehicle_power':u'\u7cfb\u7edf\u7efc\u5408\u529f\u7387(kW)'
            ,'vehicle_torque':u'\u7cfb\u7edf\u7efc\u5408\u626d\u77e9(N\u00b7m)'
            ,'battery_type':u'\u7535\u6c60\u7c7b\u578b'
            ,'battery_range_MIIT':u'\u5de5\u4fe1\u90e8\u7eed\u822a\u91cc\u7a0b(km)'
            ,'battery_capacity':u'\u7535\u6c60\u5bb9\u91cf(kWh)'
            ,'power_consumption':u'\u767e\u516c\u91cc\u8017\u7535\u91cf(kWh/100km)'
            ,'battery_pack_warrenty':u'\u7535\u6c60\u7ec4\u8d28\u4fdd'
            ,'charging_time':u'\u7535\u6c60\u5145\u7535\u65f6\u95f4'
            ,'fast_charge_electricity':u'\u5feb\u5145\u7535\u91cf(%)'
            ,'charging_pile_price':u'\u5145\u7535\u6869\u4ef7\u683c',}
        count=0
        ztlist=[]
        for i in modelConfigureList:
            temp1=modelConfigure[count][i]
            count=count+1
            for k in temp1:
                ztlist.append(k)

        ztdict={}
        for i in ztlist:
            for ename,uname in i.items():
                ztdict[ename]=uname


        flag=0
        if ztdict.get(u'\u6392\u91cf(L)'):
            flag=0
        else:
            flag=1



        #count1=0
        if flag==1:
            for ename, uname in namedic.items():
                item[ename] = "-"
                if ztdict.get(uname):
                    item[ename] = ztdict.get(uname)
                if ename == "fueltype" and item[ename] == "-" and ztdict.get(u'燃料类型'):
                    item[ename] = ztdict.get(u'燃料类型')

        else:
            for ename, uname in namedic2.items():
                item[ename] = "-"
                if ztdict.get(uname):
                    item[ename] = ztdict.get(uname)
                if ename == "fueltype" and item[ename] == "-" and  ztdict.get(u'燃料类型'):
                    item[ename] = ztdict.get(u'燃料类型')
            #count1=count1+1



        # print(item)
        yield item

# new
class CarSpider_new(CarSpider):

    # basesetting
    name = spidername_new

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")
        self.part = int(part)
        self.parts = int(parts)

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        self.part = int(part)
        self.parts = int(parts)
        #do
        super(update, self).start_requests()





