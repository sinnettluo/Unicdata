# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import GpjModelListItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from carbuisness.items import ZupukItem
from lxml import etree


website='gpj_modellist2'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://bj.gongpingjia.com/meta-data/new/get-brand/"]


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','residual_value',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    # def start_requests(self):
    #     yield scrapy.FormRequest(url="http://common.jingzhengu.com/carStyle/getMakesPanelHtml", formdata={"hasAppraise":"true", "hasNewCar":"true", "hasElec":"true"})

    def parse(self, response):
        brands = json.loads(response.text)
        for brand in brands["brand_source"]:
            for b in brand["list"]:
                brandname = b["name"]
                brandcode = b["slug"]
                url = "http://bj.gongpingjia.com/meta-data/new/get-model/?brand=%s" % brandcode
                yield scrapy.Request(url=url, meta={"brandname": brandname, "brandcode": brandcode},
                                     callback=self.parse_family)

    def parse_family(self, response):
        families = json.loads(response.text)
        for family in families["model_source"]:
            for f in family["list"]:
                factoryname = f["mum"]
                familyname = f["name"]
                familycode = f["slug"]
                url = "http://bj.gongpingjia.com/meta-data/new/get-model-detail/?model=%s" % familycode
                yield scrapy.Request(url=url, meta={"brandname": response.meta["brandname"],
                                                    "brandcode": response.meta["brandcode"], "factoryname": factoryname,
                                                    "familyname": familyname, "familycode": familycode},
                                     callback=self.parse_model)

    def parse_model(self, response):
        models = json.loads(response.text)
        for model in models["model_detail"]:
            for m in model["list"]:
                model_detail = m["model_detail"]
                emission_standard = m["emission_standard"]
                transmission = m["transmission"]
                max_reg_year = m["max_reg_year"]
                volume = m["volume"]
                min_reg_year = m["min_reg_year"]
                detail_model_slug = m["detail_model_slug"]
                year = m["year"]
                price_bn = m["price_bn"]
                url = "http://bj.gongpingjia.com/evaluate/eval-report/detail_param/%s/%s/%s/" % (response.meta["brandcode"], response.meta["familycode"], detail_model_slug)
                yield scrapy.Request(url=url, meta={"brandname": response.meta["brandname"],
                                                    "brandcode": response.meta["brandcode"],
                                                    "familyname": response.meta["familyname"],
                                                    "familycode": response.meta["familycode"],
                                                    "factoryname": response.meta["factoryname"],
                                                    "model_detail": model_detail,
                                                    "emission_standard": emission_standard,
                                                    "transmission": transmission, "max_reg_year": max_reg_year,
                                                    "volume": volume, "min_reg_year": min_reg_year,
                                                    "detail_model_slug": detail_model_slug, "year": year,
                                                    "price_bn": price_bn, },
                                     callback=self.parse_config)


    def parse_config(self, response):

        trs = response.xpath("//tr")



        config_list = {
            u"排量(升)": "displacement",
            u"车身型式": "body_structure",
            u"上市年份": "sell_year",
            u"销售名称": "salesdesc",
            u"车系": "family",
            u"品牌": "brand",
            u"指导价格": "guide_price",
            u"生产年份": "produce_year",
            u"上市月份": "sell_month",
            u"生产状态": "produce_status",
            u"销售状态": "sell_status",
            u"车型": "model",
            u"市郊工况油耗": "suburban_fuel_consumption",
            u"市区工况油耗": "urban_fuel_consumption",
            u"工信部综合油耗(L)": "national_oil_consumption",
            u"车辆级别": "level",
            u"年款": "make_year",
            u"厂家": "factory",
            u"国别": "country",
            u"加速时间(0-100km/h)": "acceleration",
            u"车辆类型": "type",
            u"国产合资进口": "property",
            u"刹车辅助(EBA/BAS/BA等)": "brake_assist",
            u"车身稳定控制(ESP/DSC/VSC等)": "vehicle_stability_control",
            u"空气悬挂": "air_suspension",
            u"制动力分配(EBD/CBC等)": "braking_force_distribution",
            u"自动驻车上坡辅助": "auto_parking_and_hill_start_assist",
            u"牵引力控制(ASR/TCS/TRC等)": "traction_control",
            u"ABS防抱死": "abs_anti_lock",
            u"可变悬挂": "variable_suspension",
            u"前轮毂规格": "front_tire_specification",
            u"后制动器类型": "rear_brake_type",
            u"后轮毂规格": "rear_tire_specification",
            u"前制动器类型": "front_brake_type",
            u"副驾驶座座椅电动调节": "auxiliary_driving_seat_adjusting",
            u"座椅按摩": "seat_massage",
            u"真皮座椅": "genuine_leather_seat",
            u"座椅高低调节": "seats_height_adjusting",
            u"前排座椅加热": "front_seat_heating",
            u"驾驶座座椅电动调节": "driving_seat_adjusting",
            u"后排座椅加热": "back_seat_heating",
            u"后排杯架": "back_cup_frame",
            u"后座中央扶手": "back_seat_center_handler",
            u"座椅通风": "seat_ventilation",
            u"电动座椅记忆": "elec_seat_memery",
            u"腰部支撑调节": "waist_support_adjusting",
            u"前座中央扶手": "front_seat_center_handler",
            u"长度(mm)": "length",
            u"前轮距(mm)": "front_wheelbase",
            u"整备质量(Kg)": "preparation_quality",
            u"高度(mm)": "height",
            u"轴距(mm)": "wheelbase",
            u"座位数": "number_seats",
            u"后轮距(mm)": "rear_wheelbase",
            u"宽度(mm)": "width",
            u"最大载重质量(kg)": "maximum_load_weight",
            u"油箱容积(L)": "tank_volume",
            u"车门数": "number_doors",
            u"温度分区控制": "temperature_zoning_control",
            u"空气调节/花粉过滤": "air_conditioning",
            u"自动空调": "auto_air_conditioning",
            u"后排独立空调": "rear_independent_air_conditioning",
            u"后座出风口": "rear_seat_outlet",
            u"空调": "air_conditioner",
            u"LED大灯": "led_headlights",
            u"车内氛围灯": "interior_atmosphere_lamp",
            u"大灯高度可调": "headlamp_height_adjustable",
            u"大灯清洗装置": "headlight_cleaning_device",
            u"日间行车灯": "drl",
            u"自动头灯": "automatic_headlamp",
            u"档位数": "number_gears",
            u"变速器描述": "gear_description",
            u"变速器类型": "gear_type",
            u"行车电脑显示屏": "driving_computer_display_screen",
            u"方向盘换挡": "steering_wheel_gearing",
            u"真皮方向盘": "leather_steering_wheel",
            u"倒车视频影像": "reversing_video",
            u"方向盘电动调节": "steering_wheel_elec_adjusting",
            u"方向盘上下调节": "steering_wheel_height_adjusting",
            u"定速巡航": "cruise_control",
            u"泊车辅助": "parking_assist",
            u"倒车雷达": "reversing_radar",
            u"多功能方向盘": "multifunctional_steering_wheel",
            u"方向盘前后调节": "steering_wheel_distance_adjusting",
            u"HUD抬头数字显示": "hud_rising_number_display",
            u"扬声器数量": "loudspeaker_quantity",
            u"多碟DVD": "multi_disk_dvd",
            u"蓝牙车载电话": "blueteeth_and_car_phone",
            u"音频支持MP3": "mp3_support",
            u"车载信息服务": "telematics",
            u"单碟DVD": "single_dish_dvd",
            u"外接音源接口(AUX/USB/iPod等)": "external_audio_interface",
            u"车载电视": "car_tv",
            u"GPS导航": "gps_navigation_system",
            u"人机交互系统": "man_machine_interaction_system",
            u"定位互动服务": "location_interaction_service",
            u"中控台彩色大屏": "central_console_color_screen",
            u"前电动车窗": "front_electric_window",
            u"后视镜电动折叠": "electric_folding_rearview_mirror",
            u"后视镜记忆": "rearview_mirror_memory",
            u"车窗防夹手功能": "window_clamping_function",
            u"后视镜电动调节": "rearview_mirror_elec_adjusting",
            u"遮阳板化妆镜": "sun_visor",
            u"后电动车窗": "rear_electric_window",
            u"隔热玻璃": "thermal_insulation_glass",
            u"后风挡遮阳帘": "rear_windshield_sunshade_curtain",
            u"感应雨刷": "induction_wiper",
            u"后排侧遮阳帘": "rear_side_sunshade_curtain",
            u"后视镜自动防眩目": "anti_glare_inner_rearview_mirror",
            u"后视镜加热": "rearview_mirror_heating",
            u"供油方式": "fuel_supply_mode",
            u"最大扭矩转速(rpm)": "maximum_torque_speed",
            u"最大功率转速(rpm)": "maximum_power_speed",
            u"燃油标号": "fuel_labeling",
            u"气缸数(个)": "number_cylinders",
            u"气缸容积": "cylinder_volume",
            u"发动机位置": "engine_position",
            u"排放标准": "emission_standard",
            u"最大功率(kW)": "maximum_power",
            u"气缸排列形式": "cylinder_arrangement",
            u"进气形式": "intake_mode",
            u"最大扭矩(N·m)": "maximum_torque",
            u"燃料类型": "fuel_type",
            u"最小离地间隙": "minimum_ground_clearance",
            u"转向机形式": "steering_gear_form",
            u"驱动方式": "driving_mode",
            u"驱动形式": "driving_type",
            u"前悬挂类型": "front_suspension_type",
            u"助力类型": "support_type",
            u"最小转弯半径": "minimum_turning_radius",
            u"后悬挂类型": "rear_suspension_type",
            u"后排头部气囊(气帘)": "rear_head_airbag",
            u"无钥匙启动系统": "keyless_starting_system",
            u"安全带未系提示": "seat_belt_warning",
            u"副驾驶安全气囊": "auxiliary_seat_safety_airbag",
            u"发动机电子防盗": "engine_electronic_anti_theft",
            u"中控锁": "central_control_lock",
            u"遥控钥匙": "remote_key",
            u"前排侧气囊": "front_side_airbag",
            u"后排侧气囊": "rear_side_airbag",
            u"ISOFIX儿童座椅接口": "isofix_children_seat_interface",
            u"驾驶座安全气囊": "driving_seat_safety_airbag",
            u"前排头部气囊(气帘)": "front_head_airbag",
            u"胎压监测装置": "tire_pressure_monitoring_device",
            u"后排座椅比例放倒": "rear_seats_resize",
            u"最高车速": "max_speed",
            u"停产年份": "discontinuation_year",
            u"行李厢容积(L)": "luggage_compartment_volume",
            u"前雾灯": "front_fog_lamp",
            u"压缩比": "compression_ratio",
            u"陡坡缓降": "hdc",
            u"单碟CD": "single_dish_cd",
            u"后排座椅整体放倒": "rear_seat_overall_reversion",
            u"第二排靠背角度调节": "second_row_backrest_angle_adjustment",
            u"后雨刷": "rear_wiper",
            u"第三排座椅": "third_row_seats",
            u"第二排座椅移动": "second_row_seat_movement",
            u"运动座椅": "sports_seat",
            u"多碟CD": "multi_disk_d",
            u"转向头灯": "turn_to_headlights",
            u"内置硬盘": "built_in_hard_disk",
            u"可变转向比": "variable_steering_ratio",
            u"氙气大灯": "xenon_headlamp",
            u"零胎压继续行驶": "zero_tire_pressure_driving",
            u"LATCH座椅接口": "latch_seat_interface",
            u"车载冰箱": "vehicle_refrigerator",
            u"膝部气囊": "knee_airbag",
            u"后排座椅电动调节": "rear_seat_adjusting",
            u"后排液晶屏": "rear_lcd_screen",
            u"虚拟多碟CD": "virtual_multi_disc_cd",
            u"肩部支撑调节": "shoulder_support_adjusting",
        }

        # config_list = {
        #     u"最高车速(km/h)": "fastest_speed",
        #     u"厂商": "factory",
        #     u"车身结构": "body_structure",
        #     u"长宽高(mm)": "l_w_h",
        #     u"变速箱": "gear",
        #     u"官方油耗(L/100km)": "offical_oil_consumption",
        #     u"工信部综合油耗(L/100km)": "national_oil_consumption",
        #     u"发动机": "engine",
        #     u"官方0-100km/h加速(s)": "acceleration",
        #     u"级别": "level",
        #     u"车顶型式": "roof_style",
        #     u"内饰颜色": "trim_color",
        #     u"车顶行李箱架": "roof_rack",
        #     u"车篷型式": "hood",
        #     u"挡位个数": "number_gears",
        #     u"换档拨片": "shift_dial",
        #     u"变速箱类型": "geartype",
        #     u"前排座椅加热": "front_seat_heating",
        #     u"后排座椅加热": "back_seat_heating",
        #     u"电动座椅记忆": "elec_seat_memery",
        #     u"肩部支撑调节": "shoulder_support_adjusting",
        #     u"前座中央扶手": "front_seat_center_handler",
        #     u"副驾驶座电动调节": "auxiliary_driving_seat_adjusting",
        #     u"座椅高低调节": "seats_height_adjusting",
        #     u"后排座椅通风": "back_seat_ventilation",
        #     u"第二排靠背角度调节": "second_seat_angle_adjusting",
        #     u"后座中央扶手": "back_seat_center_handler",
        #     u"主驾驶座电动调节": "driving_seat_adjusting",
        #     u"后排杯架": "back_cup_frame",
        #     u"前排座椅通风": "front_seat_ventilation",
        #     u"第二排座椅移动": "second_seat_moving",
        #     u"后排座椅按摩": "back_seat_massage",
        #     u"第三排座椅": "third_seat",
        #     u"运动风格座椅": "sport_style_seat",
        #     u"后排座椅放倒方式": "back_seat_lay_down_type",
        #     u"前排座椅按摩": "front_seat_massage",
        #     u"真皮/仿皮座椅": "genuine_imitation_leather_seat",
        #     u"腰部支撑调节": "waist_support_adjusting",
        #     u"前排座椅加热": "front_seat_heating",
        #     u"夜视系统": "night_vision_system",
        #     u"车道偏离预警系统": "ldws",
        #     u"发动机启停技术": "engine_start_stop_tech",
        #     u"自适应巡航": "adaptive_cruise_control",
        #     u"全景摄像头": "panoramic_camera",
        #     u"自动泊车入位": "automatic_parking",
        #     u"主动刹车/主动安全系统": "brake_and_safty_system",
        #     u"整体主动转向系统": "integrated_active_steering_system",
        #     u"中控液晶屏分屏显示": "central_control_panel_display",
        #     u"并线辅助": "parallel_auxiliary",
        #     u"前排座椅加热": "front_seat_heating",
        #     u"遮阳板化妆镜": "sun_visor",
        #     u"内后视镜自动防眩目": "anti_glare_inner_rearview_mirror",
        #     u"车窗防夹手功能": "window_clamping_function",
        #     u"后视镜电动折叠": "electric_folding_rearview_mirror",
        #     u"感应雨刷": "induction_wiper",
        #     u"后视镜加热": "rearview_mirror_heating",
        #     u"后风挡遮阳帘": "rear_windshield_sunshade_curtain",
        #     u"后电动车窗": "rear_electric_window",
        #     u"后视镜带侧转向灯": "rearview_mirror_side_signal",
        #     u"后排侧隐私玻璃": "rear_side_privacy_glass",
        #     u"后雨刷": "rear_wiper",
        #     u"前电动车窗": "front_electric_window",
        #     u"防紫外线/隔热玻璃": "uv_thermal_insulation_glass",
        #     u"后排侧遮阳帘": "rear_side_sunshade_curtain",
        #     u"后视镜记忆": "rearview_mirror_memory",
        #     u"外后视镜自动防眩目": "anti_glare_external_rearview_mirror",
        #     u"发动机位置": "engine_position",
        #     u"供油方式": "fuel_supply_mode",
        #     u"环保标准": "environmental_protection_standard",
        #     u"排量(L)": "displacement",
        #     u"进气方式": "intake_mode",
        #     u"最大马力(PS)": "maximum_horsepower",
        #     u"燃油标号": "fuel_labeling",
        #     u"行程(mm)": "trip",
        #     u"最大扭矩转速(rpm)": "maximum_torque_speed",
        #     u"燃料形式": "fuel_form",
        #     u"发动机特有技术": "engine_specific_tech",
        #     u"缸盖材料": "cylinder_head_material",
        #     u"最大扭矩(N.m)": "maximum_torque",
        #     u"气缸数(个)": "number_cylinders",
        #     u"发动机型号": "engine_type",
        #     u"缸径(mm)": "cylinder_diameter",
        #     u"最大功率转速(rpm)": "maximum_power_speed",
        #     u"气缸排列方式": "cylinder_arrangement",
        #     u"气门结构": "valve_structure",
        #     u"压缩比": "compression_ratio",
        #     u"缸体材料": "cylinder_material",
        #     u"最大功率(Kw)": "maximum_power",
        #     u"每缸气门数(个)": "valve_per_cylinder",
        #     u"座位数(个)": "number_seats",
        #     u"行李厢容积(L)": "luggage_compartment_volume",
        #     u"高度(mm)": "height",
        #     u"宽度(mm)": "width",
        #     u"长度(mm)": "length",
        #     u"油箱容积(L)": "tank_volume",
        #     u"后轮距(mm)": "rear_wheelbase",
        #     u"最小离地间(mm)": "minimum_ground_clearance",
        #     u"轴距(mm)": "wheelbase",
        #     u"最大载重质量(kg)": "maximum_load_weight",
        #     u"车门数(个)": "number_doors",
        #     u"前轮距(mm)": "front_wheelbase",
        #     u"整备质量(kg)": "preparation_quality",
        #     u"电动吸合门": "electrically_operated_suction_door",
        #     u"电动机类型": "motor_type",
        #     u"工信部续航里程": "mic_milestone",
        #     u"电动机总功率": "motor_total_power",
        #     u"电池容量(kWh)": "battery_capacity",
        #     u"前电动机最大扭矩(N·m)": "front_motor_maximum_torque",
        #     u"后电动机最大扭矩(N·m)": "rear_motor_maximum_torque",
        #     u"前电动机最大功率(kW)": "front_motor_maximum_power",
        #     u"后电动机最大功率(kW)": "rear_motor_maximum_power",
        #     u"驻车制动类型": "parking_brake_type",
        #     u"备胎规格": "spare_tire_specification",
        #     u"后轮胎规格": "rear_tire_specification",
        #     u"后制动器类型": "rear_brake_type",
        #     u"前轮胎规格": "front_tire_specification",
        #     u"前制动器类型": "front_brake_type",
        #     u"运动外观套件": "sports_appearance_kit",
        #     u"电动天窗": "electric_skylight",
        #     u"电动吸合门": "electrically_operated_suction_door",
        #     u"电动后备厢": "electric_reserve_compartment",
        #     u"感应后备厢": "induction_reserve_compartment",
        #     u"全景天窗": "panoramic_sunroof",
        #     u"侧滑门": "sideslip_door",
        #     u"扬声器数量": "loudspeaker_quantity",
        #     u"扬声器品牌": "speaker_brand",
        #     u"中控台彩色大屏": "central_console_color_screen",
        #     u"定位互动服务": "location_interaction_service",
        #     u"GPS导航系统": "gps_navigation_system",
        #     u"多媒体系统": "multimedia_system",
        #     u"车载电视": "car_tv",
        #     u"CD支持MP3/WMA": "mp3_wma_support",
        #     u"外接音源接口(AUX/USB/iPod等)": "external_audio_interface",
        #     u"蓝牙/车载电话": "blueteeth_and_car_phone",
        #     u"后排液晶屏": "rear_lcd_screfront_side_airbagen",
        #     u"前安全带调节": "front_seat_belt_adjustmentw",
        #     u"前排侧气囊": "front_side_airbag",
        #     u"无钥匙进入系统": "keyless_entry_system",
        #     u"后排头部气囊(气帘)": "rear_head_airbag",
        #     u"零胎压继续行驶": "zero_tire_pressure_driving",
        #     u"安全带预收紧功能": "seat_belt_pre_tightening",
        #     u"无钥匙启动系统": "keyless_starting_system",
        #     u"前排头部气囊(气帘)": "front_head_airbag",
        #     u"遥控钥匙": "remote_key",
        #     u"安全带限力功能": "seat_belt_limitation",
        #     u"儿童锁": "children_lock",
        #     u"安全带未系提示": "seat_belt_warning",
        #     u"副驾驶座安全气囊": "auxiliary_seat_safety_airbag",
        #     u"车内中控锁": "vehicle_central_control_lock",
        #     u"后排中间三点式安全带": "rear_center_seat_belt",
        #     u"发动机电子防盗": "engine_electronic_anti_theft",
        #     u"主驾驶座安全气囊": "driving_seat_safety_airbag",
        #     u"膝部气囊": "knee_airbag",
        #     u"后排安全带": "rear_seat_belt",
        #     u"ISOFIX儿童座椅接口": "isofix_children_seat_interface",
        #     u"后排侧气囊": "rear_side_airbag",
        #     u"胎压监测装置": "tire_pressure_monitoring_device",
        #     u"多功能方向盘": "multifunctional_steering_wheel",
        #     u"仪表盘亮度可调": "instrument_panel_brightness_adjusting",
        #     u"全液晶仪表盘": "full_lcd_dashboard",
        #     u"方向盘调节": "steering_wheel_adjusting",
        #     u"倒车视频影像": "reversing_video",
        #     u"方向盘记忆设置": "steering_wheel_memory_settings",
        #     u"HUD抬头数字显示": "hud_rising_number_display",
        #     u"方向盘加热": "steering_wheel_heating",
        #     u"行车电脑显示屏": "driving_computer_display_screen",
        #     u"后驻车雷达": "rear_parking_radar",
        #     u"定速巡航": "cruise_control",
        #     u"真皮方向盘": "leather_steering_wheel",
        #     u"前驻车雷达": "front_parking_radar",
        #     u"转向辅助灯": "steering_auxiliary_lamp",
        #     u"LED尾灯": "led_taillights",
        #     u"日间行车灯": "drl",
        #     u"转向头灯(辅助灯)": "turning_headlights",
        #     u"车厢前阅读灯": "front_reading_lamp",
        #     u"大灯高度可调": "headlamp_height_adjustable",
        #     u"前大灯随动转向": "front_headlamp_automatic_steering",
        #     u"大灯清洗装置": "headlight_cleaning_device",
        #     u"车内氛围灯": "interior_atmosphere_lamp",
        #     u"前雾灯": "front_fog_lamp",
        #     u"侧转向灯": "side_turn_lamp",
        #     u"自动头灯": "automatic_headlamp",
        #     u"LED大灯": "led_headlights",
        #     u"高位(第三)制动灯": "high_brake_lights",
        #     u"车内空气调节/花粉过滤": "air_conditioning",
        #     u"空调控制方式": "air_conditioning_control_mode",
        #     u"温度分区控制": "temperature_zoning_control",
        #     u"后座出风口": "rear_seat_outlet",
        #     u"车内空气净化装": "vehicle_air_purification_equipment",
        #     u"后排独立空调": "rear_independent_air_conditioning",
        #     u"车载冰箱": "vehicle_refrigerator",
        #     u"转向助力": "steering_power",
        #     u"前悬架类型": "front_suspension_type",
        #     u"后悬架类型": "rear_suspension_type",
        #     u"驱动方式": "driving_mode",
        #     u"中央差速器结构": "central_differential_structure",
        #     u"底盘结构": "chassis_structure",
        #     u"最小转弯半径(m)": "minimum_turning_radius",
        #     u"接近角(度)": "approach_angle",
        #     u"离去角(度)": "departure_angle",
        #     u"制动力分配(EBD/CBC等)": "braking_force_distribution",
        #     u"后桥限滑差速器/差速锁": "rear_limited_slip_differential",
        #     u"陡坡缓降": "hdc",
        #     u"中央差速器锁止功能": "central_differential_locking",
        #     u"可变转向比": "variable_steering_ratio",
        #     u"盲点检测": "blind_spot_detection",
        #     u"车身稳定控制": "vehicle_stability_control",
        #     u"上坡辅助": "hill_start_assist",
        #     u"可变悬架": "variable_suspension",
        #     u"随速助力转向调节(EPS)": "automatic_steering_adjusting",
        #     u"自动驻车": "auto_parking",
        #     u"ABS防抱死": "abs_anti_lock",
        #     u"前桥限滑差速器/差速锁": "front_limited_slip_differential",
        #     u"空气悬挂": "air_suspension",
        #     u"可调悬挂": "adjustable_suspension",
        #     u"刹车辅助(EBA/BAS/BA等)": "brake_assist",
        #     u"牵引力控制(ASR/TCS/TRC等)": "traction_control"
        # }

        item = GpjModelListItem()

        item["brandcode"] = response.meta["brandcode"]
        item["brandname"] = response.meta["brandname"]
        item["familyname"] = response.meta["familyname"]
        item["familycode"] = response.meta["familycode"]
        item["factoryname"] = response.meta["factoryname"]
        item["model_detail"] = response.meta["model_detail"]
        item["emission_standard"] = response.meta["emission_standard"]
        item["transmission"] = response.meta["transmission"]
        item["max_reg_year"] = response.meta["max_reg_year"]
        item["volume"] = response.meta["volume"]
        item["min_reg_year"] = response.meta["min_reg_year"]
        item["detail_model_slug"] = response.meta["detail_model_slug"]
        item["year"] = response.meta["year"]
        item["price_bn"] = response.meta["price_bn"]


        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["status"] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        for tr in trs:
            key = tr.xpath("td[1]/text()").extract_first()
            value = tr.xpath("td[2]/text()").extract_first()
            try:
                item[config_list[key]] = value
            except Exception as e:
                with open("/home/gpj.log", "a") as f:
                    f.write(str(e))
                    f.close()

        yield item