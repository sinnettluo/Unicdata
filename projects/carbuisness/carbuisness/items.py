# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarbuisnessItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class meituancarItem(scrapy.Item):
    url=scrapy.Field()
    website=scrapy.Field()
    status=scrapy.Field()
    grabtime=scrapy.Field()
    city=scrapy.Field()
    cityid=scrapy.Field()
    district=scrapy.Field()
    shopname=scrapy.Field()
    starnum=scrapy.Field()
    phone=scrapy.Field()
    location=scrapy.Field()
    commentnum=scrapy.Field()
    shop_hours=scrapy.Field()
    price=scrapy.Field()
    skillscore=scrapy.Field()
    enscore=scrapy.Field()
    servicescore=scrapy.Field()

class dianpingmarketitem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    city = scrapy.Field()
    cityid = scrapy.Field()
    district = scrapy.Field()
    shopname=scrapy.Field()
    starnum=scrapy.Field()
    phone=scrapy.Field()
    location=scrapy.Field()
    commentnum=scrapy.Field()
    shop_hours=scrapy.Field()
    price=scrapy.Field()
    productscore=scrapy.Field()
    enscore=scrapy.Field()
    servicescore=scrapy.Field()

class tuhucaritem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    shopname= scrapy.Field()
    shop_hours= scrapy.Field()
    shoptype= scrapy.Field()
    phone= scrapy.Field()
    location= scrapy.Field()
    province= scrapy.Field()
    city= scrapy.Field()
    shopid= scrapy.Field()
    commentscore= scrapy.Field()
    paytype= scrapy.Field()
    skillstar= scrapy.Field()
    servicestar= scrapy.Field()
    envirstar= scrapy.Field()

class GasDianpingItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    shopname = scrapy.Field()
    starnum = scrapy.Field()
    location = scrapy.Field()
    phone = scrapy.Field()
    shop_hours = scrapy.Field()
    commentnum = scrapy.Field()
    price = scrapy.Field()
    district = scrapy.Field()
    cityid = scrapy.Field()
    cityname = scrapy.Field()
    skillscore = scrapy.Field()
    enscore = scrapy.Field()
    servicescore = scrapy.Field()


class GasSinopecItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    #dotnum = scrapy.Field()     #序号
    dotname = scrapy.Field()
    location = scrapy.Field()
    sell_card = scrapy.Field()
    phonenum = scrapy.Field()
    electronic_prepaid_card_invoice = scrapy.Field()
    valueadd_tax_invoice = scrapy.Field()
    province = scrapy.Field()
    # pagenum = scrapy.Field()

class GasEnergyItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    stationname = scrapy.Field()
    parentfirm = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    phone = scrapy.Field()
    shop_hours = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()

class EsfFangItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    province = scrapy.Field()               # 没有使用这个字段
    city = scrapy.Field()                   # 城市
    district = scrapy.Field()               # 区
    location = scrapy.Field()               # 地址
    buildingname = scrapy.Field()           # 小区名
    housenum = scrapy.Field()               # 总 户 数
    opening_quotation = scrapy.Field()      # 开盘时间
    completetime = scrapy.Field()           # 竣工时间
    area = scrapy.Field()                   #  建筑面积
    parkingnum = scrapy.Field()             # 停 车 位
    price = scrapy.Field()                  # 本月均价
    buildtype = scrapy.Field()              # 物业类别
    factoryname = scrapy.Field()            # 开 发 商
    county = scrapy.Field()                 # 区下面的一个等级(乡村？街道？)

class NewhouseFangItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    province = scrapy.Field()               # 没有使用这个字段
    city = scrapy.Field()                   # 城市
    district = scrapy.Field()               # 区
    location = scrapy.Field()               # 地址
    buildingname = scrapy.Field()           # 小区名
    housenum = scrapy.Field()               # 总 户 数
    completetime = scrapy.Field()           # 竣工时间
    opening_quotation = scrapy.Field()      # 开盘时间
    area = scrapy.Field()                   #  面积
    parkingnum = scrapy.Field()             # 停 车 位
    price = scrapy.Field()                  # 本月均价
    buildtype = scrapy.Field()              # 物业类别
    factoryname = scrapy.Field()            # 开 发 商
    county = scrapy.Field()                 # 区下面的一个等级(乡村？街道？)
    city_district = scrapy.Field()



class Yangche51StoreItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    shopname = scrapy.Field()
    location = scrapy.Field()
    shopno = scrapy.Field()
    shop_hours = scrapy.Field()
    phone = scrapy.Field()
    carservice = scrapy.Field()
    skilllevel = scrapy.Field()
    commentnum = scrapy.Field()
    goodper = scrapy.Field()
    userscore = scrapy.Field()
    servicescore = scrapy.Field()
    envirscore = scrapy.Field()
    skillscore = scrapy.Field()
    city = scrapy.Field()

class CarGuaziItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()


class fangshopitem(scrapy.Item):
    url=scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    shortdesc=scrapy.Field()                # 标题描述
    houseid=scrapy.Field()                  # 房源编号
    posttime=scrapy.Field()                 # 发布时间
    price=scrapy.Field()                    # 价格
    paystyle=scrapy.Field()                 # 支付方式
    area=scrapy.Field()                     # 建筑面积
    phone=scrapy.Field()                    # 电话
    shopname=scrapy.Field()                 # 楼盘名称
    address=scrapy.Field()                  # 楼盘地址
    propertycost=scrapy.Field()             # 物业费
    sfb=scrapy.Field()                      # 适合经营
    type=scrapy.Field()                     # 房屋类型
    uniprice=scrapy.Field()                 # 租金

class fangofficeitem(scrapy.Item):
    url=scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    shortdesc= scrapy.Field()
    houseid= scrapy.Field()
    posttime= scrapy.Field()
    price= scrapy.Field()
    unitprice= scrapy.Field()
    area= scrapy.Field()
    phone= scrapy.Field()
    housename= scrapy.Field()
    address= scrapy.Field()
    propertycost= scrapy.Field()
    level= scrapy.Field()
    fitment= scrapy.Field()
    type= scrapy.Field()

class w58shopitem(scrapy.Item):
    url=scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    city= scrapy.Field()
    shortdesc= scrapy.Field()
    district= scrapy.Field()
    address= scrapy.Field()
    type1= scrapy.Field()
    area= scrapy.Field()
    price= scrapy.Field()
    agent= scrapy.Field()
    posttime= scrapy.Field()
    browse= scrapy.Field()
    phone= scrapy.Field()
    creditlevel= scrapy.Field()
    agentcompany= scrapy.Field()


class w58officeitem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()               # 城市
    shortdesc = scrapy.Field()          # 简短描述
    district = scrapy.Field()           # 小区
    detailed_address = scrapy.Field()   # 详细地址
    building = scrapy.Field()           # 楼盘
    section = scrapy.Field()            # 地段
    type1 = scrapy.Field()              # 类别
    area = scrapy.Field()               # 面积
    price = scrapy.Field()              # 价格
    agent = scrapy.Field()              # 联系人
    posttime = scrapy.Field()           # 发布时间
    browse = scrapy.Field()             # 浏览次数
    phone = scrapy.Field()              # 联系人电话
    creditlevel = scrapy.Field()        # 联系人信用等级
    agentcompany = scrapy.Field()       # 联系人所属公司
    desc=scrapy.Field()                 # 描述

class LianjiaEsfItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    price = scrapy.Field()                      # 价格
    price_m2 = scrapy.Field()                   # 每平米价格
    loop_information = scrapy.Field()           # 环线信息
    build_name = scrapy.Field()                 # 小区名称
    address = scrapy.Field()                    # 地址
    house_id = scrapy.Field()                   # 链家编号
    property_phone = scrapy.Field()             # 物业电话
    house_type = scrapy.Field()                 # 房屋户型
    elevator = scrapy.Field()                   # 配备电梯
    sizearea = scrapy.Field()                   # 建筑面积
    heating_type = scrapy.Field()               # 供暖方式
    floor_NO = scrapy.Field()                   # 所在楼层
    decoration_situation = scrapy.Field()       # 装修情况
    orientations = scrapy.Field()               # 房屋朝向
    parking_condition = scrapy.Field()          # 车位情况
    transaction_last = scrapy.Field()           # 上次交易
    age_limit = scrapy.Field()                  # 房本年限
    sale_reason = scrapy.Field()                # 售房原因
    building_type = scrapy.Field()              # 房屋类型
    average_price = scrapy.Field()              # 挂牌均价
    build_age = scrapy.Field()                  # 建筑年代
    property_type = scrapy.Field()              # 物业类型
    building_num = scrapy.Field()               # 楼栋总数
    house_num = scrapy.Field()                  # 房屋总数
    property_company = scrapy.Field()           # 物业公司
    developers = scrapy.Field()                 # 开发商
    listing_houses = scrapy.Field()             # 挂牌房源
    shortdesc = scrapy.Field()                  # 标题描述
    city = scrapy.Field()                       # 城市
    label = scrapy.Field()                      # 房源标签
    core_selling_point = scrapy.Field()         # 核心卖点
    traffic_trip = scrapy.Field()               # 交通出行
    community_introduction = scrapy.Field()     # 小区介绍
    apartment_description = scrapy.Field()      # 户型介绍
    periphery = scrapy.Field()                  # 周边配套
    decoration_describe = scrapy.Field()        # 装修描述

class LianjiaFangItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()                   # 城市
    building_name = scrapy.Field()          # 楼盘名
    building_name2 = scrapy.Field()         # 楼盘别名
    price_m2 = scrapy.Field()               # 每平方米价格
    price = scrapy.Field()                  # 总价
    sizearea = scrapy.Field()               # 建筑面积
    house_type = scrapy.Field()             # 物业类型
    building_address = scrapy.Field()       # 地址
    news = scrapy.Field()                   # 最新动态
    sales_offices_address = scrapy.Field()  # 售楼处地址
    developers = scrapy.Field()             # 开发商
    property_company = scrapy.Field()       # 物业公司
    phone = scrapy.Field()                  # 电话
    decoration_situation = scrapy.Field()   # 装修状况
    opening_quotation = scrapy.Field()      # 最新开盘时间
    deliver_time = scrapy.Field()           # 最早交房时间
    property_fee = scrapy.Field()           # 物业费用
    water_and_electric = scrapy.Field()     # 水电燃气
    house_num = scrapy.Field()              # 计划户数
    pry = scrapy.Field()                    # 产权年限
    volume_ratio = scrapy.Field()           # 容积率
    greening_rate = scrapy.Field()          # 绿化率
    parking_condition = scrapy.Field()      # 车位情况

class YouxinpaiPicItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    brandname = scrapy.Field()                      # 品牌
    familyname = scrapy.Field()                     # 车系
    city = scrapy.Field()                           # 城市
    # http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=1219997
    essential_information = scrapy.Field()          # 车辆信息
    document_formalities = scrapy.Field()           # 证件手续
    license_plate_number = scrapy.Field()           # 车牌号
    description_violation = scrapy.Field()          # 违章说明
    paint_description = scrapy.Field()              # 漆面说明
    other_requipment = scrapy.Field()               # 其他配置
    complement = scrapy.Field()                     # 补充说明
    lubricant_check = scrapy.Field()                # 机油检查
    smoke_check = scrapy.Field()                    # 排烟检查
    antifreeze_check = scrapy.Field()               # 防冻液检查
    run_check = scrapy.Field()                      # 运转检查
    brake_check = scrapy.Field()                    # 刹车油检查
    engine_check = scrapy.Field()                   # 发动机检查
    booster_oil = scrapy.Field()                    # 助力油检查
    refit_check = scrapy.Field()                    # 改装说明
    battery_check = scrapy.Field()                  # 电池检查
    internally_piloting = scrapy.Field()            # 内控电器
    belt_check = scrapy.Field()                     # 皮带检查
    spare_tire = scrapy.Field()                     # 备胎
    start_machine_check = scrapy.Field()            # 启动机检查
    requipment = scrapy.Field()                     # 工具
    carkey = scrapy.Field()                         # 车钥匙
    gearcheck = scrapy.Field()                      # 变速箱检查
    rotate_booster_check = scrapy.Field()           # 转向助力检查
    apparent_mileage = scrapy.Field()               # 表显里程
    # http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=123420#gInjury
    vehicle_summary = scrapy.Field()                #车况摘要
    vehicle_level = scrapy.Field()                  #车况等级
    date_of_production = scrapy.Field()             #车辆出厂日期
    registration_date = scrapy.Field()              #车辆注册日期
    use_properties = scrapy.Field()                 #使用性质
    owner_nature = scrapy.Field()                   #车辆所有人性质
    new_car_warranty = scrapy.Field()               #新车质保
    validity_period_of_examination = scrapy.Field() #年审有效期
    commercial_insurance = scrapy.Field()           #商业险
    compulsory_insurance = scrapy.Field()           #交强险到期日
    is_one = scrapy.Field()                         #是否一手车
    maintenance_record = scrapy.Field()             #保养手册记录
    vehicle_and_vessel_tax = scrapy.Field()         #车船税到期日
    standard_configuration = scrapy.Field()         #车辆标准配置
    personalized_configuration = scrapy.Field()     #车主个性化配置
    fuel_type = scrapy.Field()                      #燃油类型
    engine_number = scrapy.Field()                  #发动机号
    VIN_num = scrapy.Field()                        #车辆VIN码
    license_plate = scrapy.Field()                  #车牌号码
    color = scrapy.Field()                          #车辆原色
    is_refit = scrapy.Field()                       #车辆是否改装
    registration = scrapy.Field()                   #登记证
    driving_book = scrapy.Field()                   #行驶本
    invoice = scrapy.Field()                        #原始购车发票
    purchase_tax = scrapy.Field()                   #购置税
    key = scrapy.Field()                            #车钥匙
    instructions = scrapy.Field()                   #说明书
    supplementary_notes = scrapy.Field()            #补充说明
    starter_steering = scrapy.Field()               #起动机/转向系统
    body_lamp = scrapy.Field()                      #车身灯具
    engine = scrapy.Field()                         #发动机
    tool_state = scrapy.Field()                     #工具状态
    transmission = scrapy.Field()                   #变速器
    spare_wheel_status = scrapy.Field()             #备胎状态
    shock_absorber = scrapy.Field()                 #避震器
    door_handle = scrapy.Field()                    #门手
    chassis = scrapy.Field()                        #底盘/行驶
    car_keys = scrapy.Field()                       #车钥匙
    brake = scrapy.Field()                          #制动器
    exhaust_system = scrapy.Field()                 #排气系统
    electrical_system = scrapy.Field()              #电器系统
    supplement = scrapy.Field()                     #车辆补充说明

class wuxiplaning_preannouncement(scrapy.Item):
    url=scrapy.Field()
    grabtime = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    posttime = scrapy.Field()
    browser = scrapy.Field()
    shortdesc = scrapy.Field()
    land_information = scrapy.Field()
    publicity = scrapy.Field()
    contact_feedback = scrapy.Field()
    data = scrapy.Field()

class wuxiplaning_afternnouncement(scrapy.Item):
    url=scrapy.Field()
    grabtime = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    posttime = scrapy.Field()
    browser = scrapy.Field()
    shortdesc = scrapy.Field()
    planing_range=scrapy.Field()
    planing_basis=scrapy.Field()
    update_reason=scrapy.Field()
    updateinformation=scrapy.Field()
    data=scrapy.Field()

# class AutohomeUserkoubeiItem(scrapy.Item):
#     url = scrapy.Field()
#     grabtime = scrapy.Field()
#     website = scrapy.Field()
#     status = scrapy.Field()
#     oil_consumption = scrapy.Field()  #油耗
#     travel_distance = scrapy.Field()  #页面购车参数：目前行驶
#     space   #空间
#     power   #动力
#     control #操控
#     oil_consumption_grade #油耗
#     comfortability  #舒适性
#     appearance  #外观
#     interior    #内饰
#     cost_performance    #性价比
#     car_buy_purpose     #购车目的

# class YouxinpaiPicItem(scrapy.Item):
#     grabtime = scrapy.Field()
#     url = scrapy.Field()
#     website = scrapy.Field()
#     status = scrapy.Field()
#     brandname = scrapy.Field()
#     familyname = scrapy.Field()
#     city = scrapy.Field()
#     # http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=1219997
#     essential_information = scrapy.Field()
#     document_formalities = scrapy.Field()
#     license_plate_number = scrapy.Field()
#     description_violation = scrapy.Field()
#     paint_description = scrapy.Field()
#     other_requipment = scrapy.Field()
#     complement = scrapy.Field()
#     lubricant_check = scrapy.Field()
#     smoke_check = scrapy.Field()
#     antifreeze_check = scrapy.Field()
#     run_check = scrapy.Field()
#     brake_check = scrapy.Field()
#     engine_check = scrapy.Field()
#     booster_oil = scrapy.Field()
#     refit_check = scrapy.Field()
#     battery_check = scrapy.Field()
#     internally_piloting = scrapy.Field()
#     belt_check = scrapy.Field()
#     spare_tire = scrapy.Field()
#     start_machine_check = scrapy.Field()
#     requipment = scrapy.Field()
#     carkey = scrapy.Field()
#     gearcheck = scrapy.Field()
#     rotate_booster_check = scrapy.Field()
#     apparent_mileage = scrapy.Field()
#     # http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=123420#gInjury
#     vehicle_summary = scrapy.Field()                    #车况摘要
#     vehicle_level = scrapy.Field()                      #车况等级
#     date_of_production = scrapy.Field()                 #车辆出厂日期
#     registration_date = scrapy.Field()                  #车辆注册日期
#     use_properties = scrapy.Field()                     #使用性质
#     owner_nature = scrapy.Field()                       #车辆所有人性质
#     new_car_warranty = scrapy.Field()                   #新车质保
#     validity_period_of_examination = scrapy.Field()     #年审有效期
#     commercial_insurance = scrapy.Field()               #商业险
#     compulsory_insurance = scrapy.Field()               #交强险到期日
#     is_one = scrapy.Field()                             #是否一手车
#     maintenance_record = scrapy.Field()                 #保养手册记录
#     vehicle_and_vessel_tax = scrapy.Field()             #车船税到期日
#     standard_configuration = scrapy.Field()             #车辆标准配置
#     personalized_configuration = scrapy.Field()         #车主个性化配置
#     fuel_type = scrapy.Field()                          #燃油类型
#     engine_number = scrapy.Field()                      #发动机号
#     VIN_num = scrapy.Field()                            #车辆VIN码
#     license_plate = scrapy.Field()                      #车牌号码
#     color = scrapy.Field()                              #车辆原色
#     is_refit = scrapy.Field()                           #车辆是否改装
#     registration = scrapy.Field()                       #登记证
#     driving_book = scrapy.Field()                       #行驶本
#     invoice = scrapy.Field()                            #原始购车发票
#     purchase_tax = scrapy.Field()                       #购置税
#     key = scrapy.Field()                                #车钥匙
#     instructions = scrapy.Field()                       #说明书
#     supplementary_notes = scrapy.Field()                #补充说明
#     starter_steering = scrapy.Field()                   #起动机/转向系统
#     body_lamp = scrapy.Field()                          #车身灯具
#     engine = scrapy.Field()                             #发动机
#     tool_state = scrapy.Field()                         #工具状态
#     transmission = scrapy.Field()                       #变速器
#     spare_wheel_status = scrapy.Field()                 #备胎状态
#     shock_absorber = scrapy.Field()                     #避震器
#     door_handle = scrapy.Field()                        #门手
#     chassis = scrapy.Field()                            #底盘/行驶
#     car_keys = scrapy.Field()                           #车钥匙
#     brake = scrapy.Field()                              #制动器
#     exhaust_system = scrapy.Field()                     #排气系统
#     electrical_system = scrapy.Field()                  #电器系统
#     supplement = scrapy.Field()                         #车辆补充说明


class BochewangCarItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    modelname = scrapy.Field()
    license_plate_num = scrapy.Field()
    subject_species = scrapy.Field()
    displacement = scrapy.Field()
    frame_number = scrapy.Field()
    date_of_initial_arrival = scrapy.Field()
    engine_number = scrapy.Field()
    effective_annual_inspection = scrapy.Field()
    purchase_price = scrapy.Field()
    secondhand_ticket = scrapy.Field()
    compulsory_insurance = scrapy.Field()
    cause_of_loss = scrapy.Field()
    vehicle_and_vessel_tax = scrapy.Field()
    address = scrapy.Field()
    nature = scrapy.Field()
    mileage = scrapy.Field()
    starting_price = scrapy.Field()
    commission_rate = scrapy.Field()
    supplementary = scrapy.Field()
    sold_date = scrapy.Field()
    price1 = scrapy.Field()
    bid_record = scrapy.Field()

class AutohomeGeneralStore(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    star_level = scrapy.Field()     #所属级别(综合店)
    name = scrapy.Field()           #店名
    phone = scrapy.Field()          #联系电话
    address = scrapy.Field()        #地址
    main_brand = scrapy.Field()     #主营品牌
    city = scrapy.Field()           # 城市

class YicheGeneralStore(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()           # 店名
    star_level = scrapy.Field()     # 级别(4S店或者综合店)
    phone = scrapy.Field()          # 电话
    phone_400 = scrapy.Field()      # 400电话
    official_url = scrapy.Field()   # 官网
    address = scrapy.Field()        # 地址
    main_brand = scrapy.Field()     # 主营品牌
    city = scrapy.Field()           # 城市
    company = scrapy.Field()

class TtpaiCheckItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    damage = scrapy.Field()
    title = scrapy.Field()
    license_plate_address = scrapy.Field()
    mileage = scrapy.Field()
    license_plate_type = scrapy.Field()
    guideprice = scrapy.Field()
    comprehensive_rating = scrapy.Field()
    skeleton = scrapy.Field()
    device = scrapy.Field()
    appearance = scrapy.Field()
    interior = scrapy.Field()
    concise_description = scrapy.Field()
    car_id = scrapy.Field()
    color = scrapy.Field()
    carno = scrapy.Field()
    first_card = scrapy.Field()
    use_properties = scrapy.Field()
    authorized_number_of_passengers = scrapy.Field()
    change_times = scrapy.Field()
    newcar_guideprice = scrapy.Field()
    special_vehicle = scrapy.Field()
    yearchecktime = scrapy.Field()
    carddate = scrapy.Field()
    producedate = scrapy.Field()
    insurance1_date = scrapy.Field()
    color_change = scrapy.Field()
    appearance_color = scrapy.Field()
    interior_color = scrapy.Field()
    output = scrapy.Field()
    gear = scrapy.Field()
    fuel = scrapy.Field()
    memory_seat = scrapy.Field()
    gasbag = scrapy.Field()
    ABS = scrapy.Field()
    electric_keys_num = scrapy.Field()
    manual_keys_num = scrapy.Field()
    air_conditioner = scrapy.Field()
    steering_assist = scrapy.Field()
    electric_door_and_window = scrapy.Field()
    skylight = scrapy.Field()
    chair = scrapy.Field()
    aluminum_alloy_wheel_hub = scrapy.Field()
    cruise = scrapy.Field()
    drive_mode = scrapy.Field()
    navigation = scrapy.Field()
    radar = scrapy.Field()
    film_system = scrapy.Field()
    power_seat = scrapy.Field()
    electric_heating_seat = scrapy.Field()
    spare_tire = scrapy.Field()
    other_original_device = scrapy.Field()
    mounting_device = scrapy.Field()
    changci = scrapy.Field()


class LianjiaVillageItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()               # 城市
    name = scrapy.Field()               # 小区名
    address = scrapy.Field()            # 小区地址
    price = scrapy.Field()              # 挂牌均价
    build_year = scrapy.Field()         # 建筑年代
    build_type = scrapy.Field()         # 建筑类型
    property_type = scrapy.Field()      # 物业类型
    property_fee = scrapy.Field()       # 物业费用
    property_company = scrapy.Field()   # 物业公司
    developers = scrapy.Field()         # 开发商
    floor_num = scrapy.Field()          # 楼栋总数
    house_num = scrapy.Field()          # 房屋总数
    nearby_stores = scrapy.Field()      # 附近门店
    region = scrapy.Field()             # 区域
    loop_line = scrapy.Field()          # 环线
    score = scrapy.Field()              # 评分
    adviser = scrapy.Field()            # 小区顾问 name:顾问姓名, desc:顾问描述,phone:顾问电话




class TTPaiItem(scrapy.Item):
    title = scrapy.Field()
    car_type = scrapy.Field()
    location = scrapy.Field()
    regi_location = scrapy.Field()
    first_regi = scrapy.Field()
    miles = scrapy.Field()
    color = scrapy.Field()
    ex_times = scrapy.Field()
    use_type = scrapy.Field()
    car_level_main = scrapy.Field()
    car_level_device = scrapy.Field()
    car_level_outer = scrapy.Field()
    car_level_inner = scrapy.Field()
    report_url = scrapy.Field()
    price = scrapy.Field()
    desc = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    url = scrapy.Field()


class ZupukItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    store_id = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()
    posttime = scrapy.Field()

class WeatherItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    data = scrapy.Field()
    status = scrapy.Field()
    weather = scrapy.Field()
    temp = scrapy.Field()
    wind = scrapy.Field()
    data_url = scrapy.Field()
    title = scrapy.Field()

class AutohomeLocalDealerPriceItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    autohomeId = scrapy.Field()
    seriesId = scrapy.Field()
    price = scrapy.Field()
    minPrice = scrapy.Field()
    carModelUrl = scrapy.Field()
    dealerId = scrapy.Field()
    cityName = scrapy.Field()
    cityId = scrapy.Field()

class yicheXiaoliangItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    order_type = scrapy.Field()
    order_list = scrapy.Field()
    item_name = scrapy.Field()
    item_url = scrapy.Field()
    item_order = scrapy.Field()
    item_sales = scrapy.Field()

class che300proItem(scrapy.Item):
    is_certified = scrapy.Field()
    is_top = scrapy.Field()
    onsale_brands = scrapy.Field()
    onsale_count = scrapy.Field()
    detail_url = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    dealer_name = scrapy.Field()
    dealer_id = scrapy.Field()
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()

class cheniuShopItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    user_mobile = scrapy.Field()
    user_name = scrapy.Field()
    user_avatar = scrapy.Field()
    user_identity_plate = scrapy.Field()
    shop_code = scrapy.Field()
    shop_name = scrapy.Field()
    shop_identity_plate = scrapy.Field()
    address = scrapy.Field()
    protocol = scrapy.Field()
    for_sale = scrapy.Field()
    shop_identity_status = scrapy.Field()
    shop_tags = scrapy.Field()
    province_code = scrapy.Field()
    sub_area_code = scrapy.Field()
    district_code = scrapy.Field()



class appRankItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    cat = scrapy.Field()
    sub_cat = scrapy.Field()
    appName = scrapy.Field()
    activeChangeRate = scrapy.Field()
    activeRate = scrapy.Field()
    appIconUrl = scrapy.Field()
    appId = scrapy.Field()
    coverageChangeRate = scrapy.Field()
    coverageRate = scrapy.Field()
    newApp = scrapy.Field()
    ranking = scrapy.Field()
    rankingChange = scrapy.Field()

class tuhuBaoYangItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    vehicle = scrapy.Field()
    productID = scrapy.Field()
    brand = scrapy.Field()
    paiLiang = scrapy.Field()
    nian = scrapy.Field()
    accessoryData = scrapy.Field()
    suggestData = scrapy.Field()
    row0 = scrapy.Field()
    row1 = scrapy.Field()
    row2 = scrapy.Field()
    row3 = scrapy.Field()
    row4 = scrapy.Field()
    row5 = scrapy.Field()
    row6 = scrapy.Field()
    row7 = scrapy.Field()
    row8 = scrapy.Field()
    row9 = scrapy.Field()
    row10 = scrapy.Field()
    row11 = scrapy.Field()
    row12 = scrapy.Field()
    row13 = scrapy.Field()
    row14 = scrapy.Field()
    row15 = scrapy.Field()
    row16 = scrapy.Field()
    row17 = scrapy.Field()
    row18 = scrapy.Field()
    row19 = scrapy.Field()
    row20 = scrapy.Field()
    row21 = scrapy.Field()
    row22 = scrapy.Field()
    row23 = scrapy.Field()
    row24 = scrapy.Field()
    row25 = scrapy.Field()
    row26 = scrapy.Field()
    row27 = scrapy.Field()
    row28 = scrapy.Field()
    row29 = scrapy.Field()
    row30 = scrapy.Field()
    row31 = scrapy.Field()


class LechebangItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    cityId = scrapy.Field()
    brandId_brand = scrapy.Field()
    brandName = scrapy.Field()
    brandId_family = scrapy.Field()
    familyName = scrapy.Field()
    brandTypeId = scrapy.Field()
    carName = scrapy.Field()
    carYear = scrapy.Field()
    mileage = scrapy.Field()
    items = scrapy.Field()
    nearItems = scrapy.Field()
    otherItems = scrapy.Field()


class AutohomeLatestOrderItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    createTime = scrapy.Field()
    cityName = scrapy.Field()
    customerName = scrapy.Field()
    customerSex = scrapy.Field()
    orderType = scrapy.Field()
    dateString = scrapy.Field()

class AutohomeNewsConditionItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    autohomeid = scrapy.Field()
    dealerid = scrapy.Field()
    content = scrapy.Field()


class AutohomeMinMaxPriceItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    autohomeid = scrapy.Field()
    provid = scrapy.Field()
    minsellingprice = scrapy.Field()
    maxsellingprice = scrapy.Field()
    minselledprice = scrapy.Field()
    maxselledprice = scrapy.Field()

class AutohomePriceInTaxItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    autohomeid = scrapy.Field()
    price_in_tax = scrapy.Field()

class CheXiangJiaItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    autohomeid = scrapy.Field()
    storeName = scrapy.Field()
    intro = scrapy.Field()
    address = scrapy.Field()
    telephone = scrapy.Field()
    mobile = scrapy.Field()
    businesstime = scrapy.Field()
    storeId = scrapy.Field()
    storeNo = scrapy.Field()
    localX = scrapy.Field()
    localY = scrapy.Field()
    image1 = scrapy.Field()
    baiduCityCode = scrapy.Field()
    areaCode = scrapy.Field()
    areaName = scrapy.Field()
    provinceId = scrapy.Field()
    provinceName = scrapy.Field()
    cityId = scrapy.Field()
    storeName = scrapy.Field()
    distId = scrapy.Field()
    distName = scrapy.Field()
    storeType = scrapy.Field()
    storeScore = scrapy.Field()
    isChat = scrapy.Field()
    isAppointment = scrapy.Field()
    businessTimeType = scrapy.Field()
    workBusinessTime = scrapy.Field()
    weekendBusinessTime = scrapy.Field()
    holidayName = scrapy.Field()
    holidayBusinessTime = scrapy.Field()
    holidayStartDate = scrapy.Field()
    holidayEndDate = scrapy.Field()
    appointmentWashCar = scrapy.Field()
    appointmentBeauty = scrapy.Field()
    appointmentMaintain = scrapy.Field()
    cityNamePrefix = scrapy.Field()
    partnerId = scrapy.Field()
    partnerCode = scrapy.Field()
    outCode = scrapy.Field()
    storeStatus = scrapy.Field()
    storeOwner = scrapy.Field()
    openStoreTime = scrapy.Field()
    ownerType = scrapy.Field()
    manHourPrice = scrapy.Field()
    stationTypeMap = scrapy.Field()
    serviceScopeMap = scrapy.Field()
    operationCode = scrapy.Field()
    bankName = scrapy.Field()
    bankAccount = scrapy.Field()
    ownerTypeName = scrapy.Field()
    storeStatusName = scrapy.Field()
    defaultCity = scrapy.Field()
    additionServiceScopeMap = scrapy.Field()

    score = scrapy.Field()

    type = scrapy.Field()
    typeName = scrapy.Field()

class PostCode138Item(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    regionid = scrapy.Field()
    regionname = scrapy.Field()
    cityid = scrapy.Field()
    cityname = scrapy.Field()
    countyid = scrapy.Field()
    countyname = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()


class BusinessAreaItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    province_name = scrapy.Field()
    province_id = scrapy.Field()
    subarea_name = scrapy.Field()
    subarea_id = scrapy.Field()
    district_name = scrapy.Field()
    district_id = scrapy.Field()
    business_area_name = scrapy.Field()
    business_area_id = scrapy.Field()
    business_geo = scrapy.Field()
    business_type = scrapy.Field()
    geo = scrapy.Field()


class AllLocationItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    province_name = scrapy.Field()
    province_id = scrapy.Field()
    city_name = scrapy.Field()
    city_id = scrapy.Field()
    district_name = scrapy.Field()
    district_id = scrapy.Field()
    street_name = scrapy.Field()
    street_id = scrapy.Field()
    citycode = scrapy.Field()
    center = scrapy.Field()
    level = scrapy.Field()
    polyline = scrapy.Field()

class AutohomeDetailedPriceItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    total_price = scrapy.Field()
    down_payment = scrapy.Field()
    loan = scrapy.Field()
    monthly_payment = scrapy.Field()
    first_payment = scrapy.Field()
    buy_tax = scrapy.Field()
    consume_tax = scrapy.Field()
    on_sign_expanse = scrapy.Field()
    vehicle_ship_use_tax = scrapy.Field()
    compulsory_insurance = scrapy.Field()
    third_party_liability_insurance = scrapy.Field()
    vehicle_loss_insurance = scrapy.Field()
    robbery_theft_insurance = scrapy.Field()
    glass_brakage_insurance = scrapy.Field()
    self_ignition_loss_insurance = scrapy.Field()
    special_insurance = scrapy.Field()
    no_fault_insurance = scrapy.Field()
    passenger_insurance = scrapy.Field()
    body_scratch_insurance = scrapy.Field()

    brandid = scrapy.Field()
    brandname = scrapy.Field()
    dynamicprice = scrapy.Field()
    fctid = scrapy.Field()
    fctname = scrapy.Field()
    levelid = scrapy.Field()
    levelname = scrapy.Field()
    oilboxvolume = scrapy.Field()
    seriesid = scrapy.Field()
    seriesname = scrapy.Field()
    specdisplacement = scrapy.Field()
    specdrivingmodename = scrapy.Field()
    specengineid = scrapy.Field()
    specenginename = scrapy.Field()
    specenginepower = scrapy.Field()
    specflowmodeid = scrapy.Field()
    specflowmodename = scrapy.Field()
    specheight = scrapy.Field()
    specid = scrapy.Field()
    specisbooked = scrapy.Field()
    specisimport = scrapy.Field()
    specispreferential = scrapy.Field()
    specistaxexemption = scrapy.Field()
    specistaxrelief = scrapy.Field()
    speclength = scrapy.Field()
    speclogo = scrapy.Field()
    specmaxprice = scrapy.Field()
    specminprice = scrapy.Field()
    specname = scrapy.Field()
    specoiloffical = scrapy.Field()
    specparamisshow = scrapy.Field()
    specpicount = scrapy.Field()
    specquality = scrapy.Field()
    specstate = scrapy.Field()
    specstructuredoor = scrapy.Field()
    specstructureseat = scrapy.Field()
    specstructuretypename = scrapy.Field()
    spectransmission = scrapy.Field()
    specweight = scrapy.Field()
    specwidth = scrapy.Field()




class ErshoucheShopItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    shopname = scrapy.Field()
    x = scrapy.Field()
    y = scrapy.Field()
    di_tag = scrapy.Field()
    addr = scrapy.Field()

class CheguansuoItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()
    addr = scrapy.Field()
    tel = scrapy.Field()
    x = scrapy.Field()
    y = scrapy.Field()
    city_name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()


class AutohomeCustomPriceItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    username = scrapy.Field()
    autohomeid = scrapy.Field()
    userid = scrapy.Field()
    fapiao = scrapy.Field()
    car_model = scrapy.Field()
    guide_price = scrapy.Field()
    total_price = scrapy.Field()
    naked_price = scrapy.Field()
    tax = scrapy.Field()
    jiaoqiangxian = scrapy.Field()
    chechuanshui = scrapy.Field()
    shangyexian = scrapy.Field()
    shangpaifei = scrapy.Field()
    pay_mode = scrapy.Field()
    promotion_set = scrapy.Field()
    buy_date = scrapy.Field()
    buy_location = scrapy.Field()
    dealer = scrapy.Field()
    dealerid = scrapy.Field()
    tel = scrapy.Field()
    dealer_addr = scrapy.Field()
    star_level = scrapy.Field()
    service_level = scrapy.Field()
    cutting_skill = scrapy.Field()

class AutohomeRegYearItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    reg_year = scrapy.Field()
    autohomeid = scrapy.Field()

class CurrencySupplyItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    date = scrapy.Field()
    m2 = scrapy.Field()
    m2_last_month = scrapy.Field()
    m2_last_year = scrapy.Field()
    m1 = scrapy.Field()
    m1_last_month = scrapy.Field()
    m1_last_year = scrapy.Field()
    m0 = scrapy.Field()
    m0_last_month = scrapy.Field()
    m0_last_year = scrapy.Field()


class FangZuItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    store_id = scrapy.Field()
    status = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    layer = scrapy.Field()
    # posttime = scrapy.Field()

class HaicjItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    level = scrapy.Field()
    zhouju = scrapy.Field()
    changkuangao = scrapy.Field()
    title = scrapy.Field()
    factory = scrapy.Field()
    body = scrapy.Field()
    pailiang = scrapy.Field()
    fuel = scrapy.Field()
    paifang = scrapy.Field()


class TuhuBaoyangItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    brand = scrapy.Field()
    family = scrapy.Field()
    familyID = scrapy.Field()
    pailiang = scrapy.Field()
    nian = scrapy.Field()
    type = scrapy.Field()
    subType = scrapy.Field()
    productType = scrapy.Field()
    product = scrapy.Field()
    productID = scrapy.Field()
    price = scrapy.Field()
    count = scrapy.Field()
    typeName = scrapy.Field()
    subTypeName = scrapy.Field()
    productTypeName = scrapy.Field()


class TuhuProductsItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()
    small_title = scrapy.Field()
    config = scrapy.Field()
    price = scrapy.Field()

class HuashengPriceCompareItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    brand = scrapy.Field()
    family = scrapy.Field()
    year = scrapy.Field()
    model = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    price1 = scrapy.Field()
    price2 = scrapy.Field()
    type= scrapy.Field()


class UsedcarSalesItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    market = scrapy.Field()
    amount = scrapy.Field()
    value = scrapy.Field()
    keche = scrapy.Field()
    huoche = scrapy.Field()
    motuoche = scrapy.Field()
    date = scrapy.Field()


class TeLaiDianItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    slow = scrapy.Field()
    fast = scrapy.Field()


class EChargeItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    address = scrapy.Field()
    areaName = scrapy.Field()
    city = scrapy.Field()
    company = scrapy.Field()
    connectorType = scrapy.Field()
    currentType = scrapy.Field()
    freeNum = scrapy.Field()
    id = scrapy.Field()
    images = scrapy.Field()
    isGs = scrapy.Field()
    lat = scrapy.Field()
    link = scrapy.Field()
    lng = scrapy.Field()
    mapIcon = scrapy.Field()
    maxOutPower = scrapy.Field()
    operatorTypes = scrapy.Field()
    payType = scrapy.Field()
    phone = scrapy.Field()
    plugType = scrapy.Field()
    priceRational = scrapy.Field()
    province = scrapy.Field()
    quantity = scrapy.Field()
    score = scrapy.Field()
    serviceCode = scrapy.Field()
    standard = scrapy.Field()
    statuss = scrapy.Field()
    supportOrder = scrapy.Field()
    businessTime = scrapy.Field()
    electricizePrice = scrapy.Field()
    quantity = scrapy.Field()
    parks = scrapy.Field()
    operatorInfos = scrapy.Field()
    name = scrapy.Field()
    priceParking = scrapy.Field()
    favorite = scrapy.Field()
    chargerTypeNum = scrapy.Field()
    chargerTypeStatusDes = scrapy.Field()
    supportCharge = scrapy.Field()
    servicedesc = scrapy.Field()
    plugnotice = scrapy.Field()
    marketingImage = scrapy.Field()
    images = scrapy.Field()
    payTypeDesc = scrapy.Field()
    numOfComments = scrapy.Field()
    totalFreeChargerNum = scrapy.Field()

class TuhuGongchengdianItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    position = scrapy.Field()

class LianlianItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    payment = scrapy.Field()
    operatorLogo = scrapy.Field()
    operatorId = scrapy.Field()
    operatorName = scrapy.Field()
    stationId = scrapy.Field()
    stationName = scrapy.Field()
    electricityFee = scrapy.Field()
    distance = scrapy.Field()
    directTotal = scrapy.Field()
    directAvaliable = scrapy.Field()
    alternatingTotal = scrapy.Field()
    alternatingAvaliable = scrapy.Field()
    parkFee = scrapy.Field()
    serviceFee = scrapy.Field()
    stationLng = scrapy.Field()
    stationLat = scrapy.Field()
    stationLngBD = scrapy.Field()
    stationLatBD = scrapy.Field()
    stationType = scrapy.Field()
    address = scrapy.Field()
    pictures = scrapy.Field()
    sitePicUrl = scrapy.Field()
    status2 = scrapy.Field()

class AutohomeFamilyConfigItem(scrapy.Item):
    grabtime = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    brand = scrapy.Field()
    brandid = scrapy.Field()
    family = scrapy.Field()
    familyid = scrapy.Field()
    level = scrapy.Field()
    body = scrapy.Field()
    engine = scrapy.Field()
    gear = scrapy.Field()

class JzgModelListItem(scrapy.Item):
    url=scrapy.Field()
    status=scrapy.Field()
    grabtime=scrapy.Field()
    fastest_speed = scrapy.Field()
    factory = scrapy.Field()
    body_structure = scrapy.Field()
    l_w_h = scrapy.Field()
    gear = scrapy.Field()
    offical_oil_consumption = scrapy.Field()
    national_oil_consumption = scrapy.Field()
    engine = scrapy.Field()
    acceleration = scrapy.Field()
    level = scrapy.Field()
    roof_style = scrapy.Field()
    trim_color = scrapy.Field()
    roof_rack = scrapy.Field()
    hood = scrapy.Field()
    number_gears = scrapy.Field()
    shift_dial = scrapy.Field()
    geartype = scrapy.Field()
    front_seat_heating = scrapy.Field()
    back_seat_heating = scrapy.Field()
    elec_seat_memery = scrapy.Field()
    shoulder_support_adjusting = scrapy.Field()
    front_seat_center_handler = scrapy.Field()
    auxiliary_driving_seat_adjusting = scrapy.Field()
    seats_height_adjusting = scrapy.Field()
    back_seat_ventilation = scrapy.Field()
    second_seat_angle_adjusting = scrapy.Field()
    back_seat_center_handler = scrapy.Field()
    driving_seat_adjusting = scrapy.Field()
    back_cup_frame = scrapy.Field()
    front_seat_ventilation = scrapy.Field()
    second_seat_moving = scrapy.Field()
    back_seat_massage = scrapy.Field()
    third_seat = scrapy.Field()
    sport_style_seat = scrapy.Field()
    back_seat_lay_down_type = scrapy.Field()
    front_seat_massage = scrapy.Field()
    genuine_imitation_leather_seat = scrapy.Field()
    waist_support_adjusting = scrapy.Field()
    front_seat_heating = scrapy.Field()
    night_vision_system = scrapy.Field()
    ldws = scrapy.Field()
    engine_start_stop_tech = scrapy.Field()
    adaptive_cruise_control = scrapy.Field()
    panoramic_camera = scrapy.Field()
    automatic_parking = scrapy.Field()
    brake_and_safty_system = scrapy.Field()
    integrated_active_steering_system = scrapy.Field()
    central_control_panel_display = scrapy.Field()
    parallel_auxiliary = scrapy.Field()
    front_seat_heating = scrapy.Field()
    sun_visor = scrapy.Field()
    anti_glare_inner_rearview_mirror = scrapy.Field()
    window_clamping_function = scrapy.Field()
    electric_folding_rearview_mirror = scrapy.Field()
    induction_wiper = scrapy.Field()
    rearview_mirror_heating = scrapy.Field()
    rear_windshield_sunshade_curtain = scrapy.Field()
    rear_electric_window = scrapy.Field()
    rearview_mirror_side_signal = scrapy.Field()
    rear_side_privacy_glass = scrapy.Field()
    rear_wiper = scrapy.Field()
    front_electric_window = scrapy.Field()
    uv_thermal_insulation_glass = scrapy.Field()
    rear_side_sunshade_curtain = scrapy.Field()
    rearview_mirror_memory = scrapy.Field()
    anti_glare_external_rearview_mirror = scrapy.Field()
    engine_position = scrapy.Field()
    fuel_supply_mode = scrapy.Field()
    environmental_protection_standard = scrapy.Field()
    displacement = scrapy.Field()
    intake_mode = scrapy.Field()
    maximum_horsepower = scrapy.Field()
    fuel_labeling = scrapy.Field()
    trip = scrapy.Field()
    maximum_torque_speed = scrapy.Field()
    fuel_form = scrapy.Field()
    engine_specific_tech = scrapy.Field()
    cylinder_head_material = scrapy.Field()
    maximum_torque = scrapy.Field()
    number_cylinders = scrapy.Field()
    engine_type = scrapy.Field()
    cylinder_diameter = scrapy.Field()
    maximum_power_speed = scrapy.Field()
    cylinder_arrangement = scrapy.Field()
    valve_structure = scrapy.Field()
    compression_ratio = scrapy.Field()
    cylinder_material = scrapy.Field()
    maximum_power = scrapy.Field()
    valve_per_cylinder = scrapy.Field()
    number_seats = scrapy.Field()
    luggage_compartment_volume = scrapy.Field()
    height = scrapy.Field()
    width = scrapy.Field()
    length = scrapy.Field()
    tank_volume = scrapy.Field()
    rear_wheelbase = scrapy.Field()
    minimum_ground_clearance = scrapy.Field()
    wheelbase = scrapy.Field()
    maximum_load_weight = scrapy.Field()
    number_doors = scrapy.Field()
    front_wheelbase = scrapy.Field()
    preparation_quality = scrapy.Field()
    electrically_operated_suction_door = scrapy.Field()
    motor_type = scrapy.Field()
    mic_milestone = scrapy.Field()
    motor_total_power = scrapy.Field()
    battery_capacity = scrapy.Field()
    front_motor_maximum_torque = scrapy.Field()
    rear_motor_maximum_torque = scrapy.Field()
    front_motor_maximum_power = scrapy.Field()
    rear_motor_maximum_power = scrapy.Field()
    parking_brake_type = scrapy.Field()
    spare_tire_specification = scrapy.Field()
    rear_tire_specification = scrapy.Field()
    rear_brake_type = scrapy.Field()
    front_tire_specification = scrapy.Field()
    front_brake_type = scrapy.Field()
    sports_appearance_kit = scrapy.Field()
    electric_skylight = scrapy.Field()
    electrically_operated_suction_door = scrapy.Field()
    electric_reserve_compartment = scrapy.Field()
    induction_reserve_compartment = scrapy.Field()
    panoramic_sunroof = scrapy.Field()
    sideslip_door = scrapy.Field()
    loudspeaker_quantity = scrapy.Field()
    speaker_brand = scrapy.Field()
    central_console_color_screen = scrapy.Field()
    location_interaction_service = scrapy.Field()
    gps_navigation_system = scrapy.Field()
    multimedia_system = scrapy.Field()
    car_tv = scrapy.Field()
    mp3_wma_support = scrapy.Field()
    external_audio_interface = scrapy.Field()
    blueteeth_and_car_phone = scrapy.Field()
    rear_lcd_screen = scrapy.Field()
    front_seat_belt_adjustmentw = scrapy.Field()
    front_side_airbag = scrapy.Field()
    keyless_entry_system = scrapy.Field()
    rear_head_airbag = scrapy.Field()
    zero_tire_pressure_driving = scrapy.Field()
    seat_belt_pre_tightening = scrapy.Field()
    keyless_starting_system = scrapy.Field()
    front_head_airbag = scrapy.Field()
    remote_key = scrapy.Field()
    seat_belt_limitation = scrapy.Field()
    children_lock = scrapy.Field()
    seat_belt_warning = scrapy.Field()
    auxiliary_seat_safety_airbag = scrapy.Field()
    vehicle_central_control_lock = scrapy.Field()
    rear_center_seat_belt = scrapy.Field()
    engine_electronic_anti_theft = scrapy.Field()
    driving_seat_safety_airbag = scrapy.Field()
    knee_airbag = scrapy.Field()
    rear_seat_belt = scrapy.Field()
    isofix_children_seat_interface = scrapy.Field()
    rear_side_airbag = scrapy.Field()
    tire_pressure_monitoring_device = scrapy.Field()
    multifunctional_steering_wheel = scrapy.Field()
    full_lcd_dashboard = scrapy.Field()
    steering_wheel_adjusting = scrapy.Field()
    reversing_video = scrapy.Field()
    steering_wheel_memory_settings = scrapy.Field()
    hud_rising_number_display = scrapy.Field()
    steering_wheel_heating = scrapy.Field()
    driving_computer_display_screen = scrapy.Field()
    rear_parking_radar = scrapy.Field()
    cruise_control = scrapy.Field()
    leather_steering_wheel = scrapy.Field()
    front_parking_radar = scrapy.Field()
    steering_auxiliary_lamp = scrapy.Field()
    led_taillights = scrapy.Field()
    drl = scrapy.Field()
    turning_headlights = scrapy.Field()
    front_reading_lamp = scrapy.Field()
    headlamp_height_adjustable = scrapy.Field()
    front_headlamp_automatic_steering = scrapy.Field()
    headlight_cleaning_device = scrapy.Field()
    interior_atmosphere_lamp = scrapy.Field()
    front_fog_lamp = scrapy.Field()
    side_turn_lamp = scrapy.Field()
    automatic_headlamp = scrapy.Field()
    led_headlights = scrapy.Field()
    high_brake_lights = scrapy.Field()
    air_conditioning = scrapy.Field()
    air_conditioning_control_mode = scrapy.Field()
    temperature_zoning_control = scrapy.Field()
    rear_seat_outlet = scrapy.Field()
    vehicle_air_purification_equipment = scrapy.Field()
    rear_independent_air_conditioning = scrapy.Field()
    vehicle_refrigerator = scrapy.Field()
    steering_power = scrapy.Field()
    front_suspension_type = scrapy.Field()
    rear_suspension_type = scrapy.Field()
    driving_mode = scrapy.Field()
    central_differential_structure = scrapy.Field()
    chassis_structure = scrapy.Field()
    minimum_turning_radius = scrapy.Field()
    approach_angle = scrapy.Field()
    departure_angle = scrapy.Field()
    braking_force_distribution = scrapy.Field()
    rear_limited_slip_differential = scrapy.Field()
    hdc = scrapy.Field()
    central_differential_locking = scrapy.Field()
    variable_steering_ratio = scrapy.Field()
    blind_spot_detection = scrapy.Field()
    vehicle_stability_control = scrapy.Field()
    hill_start_assist = scrapy.Field()
    variable_suspension = scrapy.Field()
    automatic_steering_adjusting = scrapy.Field()
    auto_parking = scrapy.Field()
    abs_anti_lock = scrapy.Field()
    front_limited_slip_differential = scrapy.Field()
    air_suspension = scrapy.Field()
    adjustable_suspension = scrapy.Field()
    brake_assist = scrapy.Field()
    traction_control = scrapy.Field()
    instrument_panel_brightness_adjusting = scrapy.Field()
    brandid = scrapy.Field()
    brandname = scrapy.Field()
    familyname = scrapy.Field()
    familyid = scrapy.Field()
    model_full_name = scrapy.Field()
    modelname = scrapy.Field()
    modelid = scrapy.Field()
    make_year = scrapy.Field()
    next_year = scrapy.Field()

class JzgPriceItem(scrapy.Item):
    url=scrapy.Field()
    status=scrapy.Field()
    grabtime=scrapy.Field()
    brandid=scrapy.Field()
    familyid=scrapy.Field()
    modelid=scrapy.Field()
    brandname = scrapy.Field()
    familyname = scrapy.Field()
    model_full_name = scrapy.Field()
    HBBZ = scrapy.Field()
    RegDateTime = scrapy.Field()
    RegDate = scrapy.Field()
    MarketMonthNum = scrapy.Field()
    Mileage = scrapy.Field()
    ProvId = scrapy.Field()
    ProvName = scrapy.Field()
    CityId = scrapy.Field()
    CityName = scrapy.Field()
    NowMsrp = scrapy.Field()
    C2BLowPrice_sell_img = scrapy.Field()
    C2BMidPrice_sell = scrapy.Field()
    C2BUpPrice_sell_img = scrapy.Field()
    B2CLowPrice_buy_img = scrapy.Field()
    B2CMidPrice_buy_img = scrapy.Field()
    B2CUpPrice_buy_img = scrapy.Field()
    # C2BBLowPrice = scrapy.Field()
    # C2BBMidPrice = scrapy.Field()
    # C2BBUpPrice = scrapy.Field()
    # C2BCLowPrice = scrapy.Field()
    # C2BCMidPrice = scrapy.Field()
    # C2BCUpPrice = scrapy.Field()
    C2CLowPrice_sell_img = scrapy.Field()
    C2CMidPrice_sell_img = scrapy.Field()
    C2CUpPrice_sell_img = scrapy.Field()
    C2CLowPrice_buy_img = scrapy.Field()
    C2CMidPrice_buy_img = scrapy.Field()
    C2CUpPrice_buy_img = scrapy.Field()
    # C2CLowPrice = scrapy.Field()
    # C2CMidPrice = scrapy.Field()
    # C2CUpPrice = scrapy.Field()
    PriceLevel = scrapy.Field()
    BaoZhilvRank = scrapy.Field()
    BaoZhilvCityId = scrapy.Field()
    BaoZhilvCityName = scrapy.Field()
    BaoZhilvLevel = scrapy.Field()
    BaoZhilvLevelName = scrapy.Field()
    BaoZhilvPercentage = scrapy.Field()
    maxPrice = scrapy.Field()
    minLoanRate = scrapy.Field()
    ShareUrl = scrapy.Field()
    PlatNumber = scrapy.Field()
    type = scrapy.Field()

class GpjModelListItem(scrapy.Item):
    url=scrapy.Field()
    status=scrapy.Field()
    grabtime=scrapy.Field()
    displacement = scrapy.Field()
    body_structure = scrapy.Field()
    sell_year = scrapy.Field()
    salesdesc = scrapy.Field()
    family = scrapy.Field()
    brand = scrapy.Field()
    guide_price = scrapy.Field()
    produce_year = scrapy.Field()
    sell_month = scrapy.Field()
    produce_status = scrapy.Field()
    sell_status = scrapy.Field()
    model = scrapy.Field()
    suburban_fuel_consumption = scrapy.Field()
    urban_fuel_consumption = scrapy.Field()
    national_oil_consumption = scrapy.Field()
    level = scrapy.Field()
    make_year = scrapy.Field()
    factory = scrapy.Field()
    country = scrapy.Field()
    acceleration = scrapy.Field()
    type = scrapy.Field()
    property = scrapy.Field()
    brake_assist = scrapy.Field()
    vehicle_stability_control = scrapy.Field()
    air_suspension = scrapy.Field()
    braking_force_distribution = scrapy.Field()
    auto_parking_and_hill_start_assist = scrapy.Field()
    traction_control = scrapy.Field()
    abs_anti_lock = scrapy.Field()
    variable_suspension = scrapy.Field()
    front_tire_specification = scrapy.Field()
    rear_brake_type = scrapy.Field()
    rear_tire_specification = scrapy.Field()
    front_brake_type = scrapy.Field()
    auxiliary_driving_seat_adjusting = scrapy.Field()
    seat_massage = scrapy.Field()
    genuine_leather_seat = scrapy.Field()
    seats_height_adjusting = scrapy.Field()
    front_seat_heating = scrapy.Field()
    driving_seat_adjusting = scrapy.Field()
    back_seat_heating = scrapy.Field()
    back_cup_frame = scrapy.Field()
    back_seat_center_handler = scrapy.Field()
    seat_ventilation = scrapy.Field()
    elec_seat_memery = scrapy.Field()
    waist_support_adjusting = scrapy.Field()
    front_seat_center_handler = scrapy.Field()
    length = scrapy.Field()
    front_wheelbase = scrapy.Field()
    preparation_quality = scrapy.Field()
    height = scrapy.Field()
    wheelbase = scrapy.Field()
    number_seats = scrapy.Field()
    rear_wheelbase = scrapy.Field()
    width = scrapy.Field()
    maximum_load_weight = scrapy.Field()
    tank_volume = scrapy.Field()
    number_doors = scrapy.Field()
    temperature_zoning_control = scrapy.Field()
    air_conditioning = scrapy.Field()
    auto_air_conditioning = scrapy.Field()
    rear_independent_air_conditioning = scrapy.Field()
    rear_seat_outlet = scrapy.Field()
    air_conditioner = scrapy.Field()
    led_headlights = scrapy.Field()
    interior_atmosphere_lamp = scrapy.Field()
    headlamp_height_adjustable = scrapy.Field()
    headlight_cleaning_device = scrapy.Field()
    drl = scrapy.Field()
    automatic_headlamp = scrapy.Field()
    number_gears = scrapy.Field()
    gear_description = scrapy.Field()
    gear_type = scrapy.Field()
    driving_computer_display_screen = scrapy.Field()
    steering_wheel_gearing = scrapy.Field()
    leather_steering_wheel = scrapy.Field()
    reversing_video = scrapy.Field()
    steering_wheel_elec_adjusting = scrapy.Field()
    steering_wheel_height_adjusting = scrapy.Field()
    cruise_control = scrapy.Field()
    parking_assist = scrapy.Field()
    reversing_radar = scrapy.Field()
    multifunctional_steering_wheel = scrapy.Field()
    steering_wheel_distance_adjusting = scrapy.Field()
    hud_rising_number_display = scrapy.Field()
    loudspeaker_quantity = scrapy.Field()
    multi_disk_dvd = scrapy.Field()
    blueteeth_and_car_phone = scrapy.Field()
    mp3_support = scrapy.Field()
    telematics = scrapy.Field()
    single_dish_dvd = scrapy.Field()
    external_audio_interface = scrapy.Field()
    car_tv = scrapy.Field()
    gps_navigation_system = scrapy.Field()
    man_machine_interaction_system = scrapy.Field()
    location_interaction_service = scrapy.Field()
    central_console_color_screen = scrapy.Field()
    front_electric_window = scrapy.Field()
    electric_folding_rearview_mirror = scrapy.Field()
    rearview_mirror_memory = scrapy.Field()
    window_clamping_function = scrapy.Field()
    rearview_mirror_elec_adjusting = scrapy.Field()
    sun_visor = scrapy.Field()
    rear_electric_window = scrapy.Field()
    thermal_insulation_glass = scrapy.Field()
    rear_windshield_sunshade_curtain = scrapy.Field()
    induction_wiper = scrapy.Field()
    rear_side_sunshade_curtain = scrapy.Field()
    anti_glare_inner_rearview_mirror = scrapy.Field()
    rearview_mirror_heating = scrapy.Field()
    fuel_supply_mode = scrapy.Field()
    maximum_torque_speed = scrapy.Field()
    maximum_power_speed = scrapy.Field()
    fuel_labeling = scrapy.Field()
    number_cylinders = scrapy.Field()
    cylinder_volume = scrapy.Field()
    engine_position = scrapy.Field()
    emission_standard = scrapy.Field()
    maximum_power = scrapy.Field()
    cylinder_arrangement = scrapy.Field()
    intake_mode = scrapy.Field()
    maximum_torque = scrapy.Field()
    fuel_type = scrapy.Field()
    minimum_ground_clearance = scrapy.Field()
    steering_gear_form = scrapy.Field()
    driving_mode = scrapy.Field()
    driving_type = scrapy.Field()
    front_suspension_type = scrapy.Field()
    support_type = scrapy.Field()
    minimum_turning_radius = scrapy.Field()
    rear_suspension_type = scrapy.Field()
    rear_head_airbag = scrapy.Field()
    keyless_starting_system = scrapy.Field()
    seat_belt_warning = scrapy.Field()
    auxiliary_seat_safety_airbag = scrapy.Field()
    engine_electronic_anti_theft = scrapy.Field()
    central_control_lock = scrapy.Field()
    remote_key = scrapy.Field()
    front_side_airbag = scrapy.Field()
    rear_side_airbag = scrapy.Field()
    isofix_children_seat_interface = scrapy.Field()
    driving_seat_safety_airbag = scrapy.Field()
    front_head_airbag = scrapy.Field()
    tire_pressure_monitoring_device = scrapy.Field()
    rear_seats_resize = scrapy.Field()
    max_speed = scrapy.Field()
    discontinuation_year = scrapy.Field()
    front_fog_lamp = scrapy.Field()
    luggage_compartment_volume = scrapy.Field()
    compression_ratio = scrapy.Field()
    hdc = scrapy.Field()
    single_dish_cd = scrapy.Field()
    rear_seat_overall_reversion = scrapy.Field()
    second_row_backrest_angle_adjustment = scrapy.Field()
    rear_wiper = scrapy.Field()
    third_row_seats = scrapy.Field()
    second_row_seat_movement = scrapy.Field()
    sports_seat = scrapy.Field()
    multi_disk_d = scrapy.Field()
    turn_to_headlights = scrapy.Field()
    built_in_hard_disk = scrapy.Field()
    variable_steering_ratio = scrapy.Field()
    xenon_headlamp = scrapy.Field()
    zero_tire_pressure_driving = scrapy.Field()
    latch_seat_interface = scrapy.Field()
    vehicle_refrigerator = scrapy.Field()
    knee_airbag = scrapy.Field()
    rear_seat_adjusting = scrapy.Field()
    rear_lcd_screen = scrapy.Field()
    virtual_multi_disc_cd = scrapy.Field()
    shoulder_support_adjusting = scrapy.Field()

    brandcode = scrapy.Field()
    brandname = scrapy.Field()
    familyname = scrapy.Field()
    familycode = scrapy.Field()
    factoryname = scrapy.Field()
    model_detail = scrapy.Field()
    emission_standard = scrapy.Field()
    transmission = scrapy.Field()
    max_reg_year = scrapy.Field()
    volume = scrapy.Field()
    min_reg_year = scrapy.Field()
    detail_model_slug = scrapy.Field()
    year = scrapy.Field()
    price_bn = scrapy.Field()


class GpjPriceItem(scrapy.Item):
    good1 = scrapy.Field()
    good2 = scrapy.Field()
    good3 = scrapy.Field()
    good4 = scrapy.Field()

    fair1 = scrapy.Field()
    fair2 = scrapy.Field()
    fair3 = scrapy.Field()
    fair4 = scrapy.Field()

    excellent1 = scrapy.Field()
    excellent2 = scrapy.Field()
    excellent3 = scrapy.Field()
    excellent4 = scrapy.Field()

    url=scrapy.Field()
    status=scrapy.Field()
    grabtime=scrapy.Field()
    month = scrapy.Field()
    mile = scrapy.Field()
    model_detail = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    city = scrapy.Field()
    year = scrapy.Field()
    sell_good = scrapy.Field()
    sell_fair = scrapy.Field()
    sell_excellent = scrapy.Field()
    private_good = scrapy.Field()
    private_fair = scrapy.Field()
    private_excellent = scrapy.Field()
    replace_good = scrapy.Field()
    replace_fair = scrapy.Field()
    replace_excellent = scrapy.Field()
    buy_good = scrapy.Field()
    buy_fair = scrapy.Field()
    buy_excellent = scrapy.Field()
    model_detail_zh = scrapy.Field()
    price_bn = scrapy.Field()
    emission_standard = scrapy.Field()


class CheHang168Item(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    priceid = scrapy.Field()
    title = scrapy.Field()
    mode = scrapy.Field()
    title2 = scrapy.Field()
    name = scrapy.Field()
    uid = scrapy.Field()
    price = scrapy.Field()
    pdate = scrapy.Field()
    guideprice = scrapy.Field()
    discount = scrapy.Field()


class AutohomeUsersItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    userid = scrapy.Field()
    username = scrapy.Field()
    nickname = scrapy.Field()
    sex = scrapy.Field()
    validation = scrapy.Field()
    location = scrapy.Field()
    birthday = scrapy.Field()
    grabtime = scrapy.Field()



class AutohomeErrorItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    waiguan1 = scrapy.Field()
    xingshi1 = scrapy.Field()
    caozuo1 = scrapy.Field()
    dianzi1 = scrapy.Field()
    zuoyi1 = scrapy.Field()
    kongtiao1 = scrapy.Field()
    neishi1 = scrapy.Field()
    fadongji1 = scrapy.Field()
    waiguan2 = scrapy.Field()
    xingshi2 = scrapy.Field()
    caozuo2 = scrapy.Field()
    dianzi2 = scrapy.Field()
    zuoyi2 = scrapy.Field()
    kongtiao2 = scrapy.Field()
    neishi2 = scrapy.Field()
    fadongji2 = scrapy.Field()
    familyid = scrapy.Field()
    category_id = scrapy.Field()
    json = scrapy.Field()
    biansuxitong1 = scrapy.Field()
    sum = scrapy.Field()

class HangzhouEChong(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    operId = scrapy.Field()
    stationNo = scrapy.Field()
    carModelList = scrapy.Field()
    remark = scrapy.Field()
    cityName = scrapy.Field()
    stationId = scrapy.Field()
    operTel = scrapy.Field()
    city = scrapy.Field()
    countyName = scrapy.Field()
    busiTime = scrapy.Field()
    parkPrice = scrapy.Field()
    stationName = scrapy.Field()
    freeNums = scrapy.Field()
    servicePrice = scrapy.Field()
    chargePrice = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    payment = scrapy.Field()
    storeFlag = scrapy.Field()
    evaNum = scrapy.Field()
    dcNums = scrapy.Field()
    evaScore = scrapy.Field()
    imgList = scrapy.Field()
    stationAddr = scrapy.Field()
    county = scrapy.Field()
    operName = scrapy.Field()
    acNums = scrapy.Field()
    acFreeNums = scrapy.Field()
    parkNo = scrapy.Field()
    gunName = scrapy.Field()
    pileNo = scrapy.Field()
    qrCodes = scrapy.Field()
    powerRating = scrapy.Field()
    gunSn = scrapy.Field()
    gunType = scrapy.Field()
    pileName = scrapy.Field()
    elecMode = scrapy.Field()
    currentRated = scrapy.Field()
    pileId = scrapy.Field()
    gunStatus = scrapy.Field()


class DiandongGuizhouItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    distance = scrapy.Field()
    staType = scrapy.Field()
    facConf = scrapy.Field()
    conPerson = scrapy.Field()
    telephone = scrapy.Field()
    addr = scrapy.Field()
    status3 = scrapy.Field()
    orgName = scrapy.Field()
    staIcon = scrapy.Field()
    message = scrapy.Field()
    success = scrapy.Field()
    id2 = scrapy.Field()
    name2 = scrapy.Field()
    poleType = scrapy.Field()
    installSite = scrapy.Field()
    powerRating = scrapy.Field()
    nomVol = scrapy.Field()
    nomCurrent = scrapy.Field()
    lon2 = scrapy.Field()
    lat2 = scrapy.Field()
    status2 = scrapy.Field()
    isBesp = scrapy.Field()

class ChezhiwangTousuItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    bianhao = scrapy.Field()
    time = scrapy.Field()
    brand = scrapy.Field()
    family = scrapy.Field()
    model = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    satisfied = scrapy.Field()


class QicheTousuItem(scrapy.Item):
    url = scrapy.Field()
    grabtime = scrapy.Field()
    status = scrapy.Field()
    bianhao = scrapy.Field()
    time = scrapy.Field()
    brand = scrapy.Field()
    family = scrapy.Field()
    model = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    satisfied = scrapy.Field()
    user = scrapy.Field()
    location = scrapy.Field()
    car_status = scrapy.Field()
    miles = scrapy.Field()
    buy_date = scrapy.Field()
    car_type = scrapy.Field()
    sstore = scrapy.Field()
    sstore_contact = scrapy.Field()
    sstore_tel = scrapy.Field()
    requirements = scrapy.Field()
    result = scrapy.Field()


class YouchekuItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    price = scrapy.Field()


class WeixinItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    title = scrapy.Field()
    digest = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()

class ChezhiwangRankItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    rank = scrapy.Field()
    brand = scrapy.Field()
    familyname = scrapy.Field()
    familyid = scrapy.Field()
    type = scrapy.Field()
    brandtype = scrapy.Field()
    country = scrapy.Field()
    problems = scrapy.Field()
    number = scrapy.Field()
    stime = scrapy.Field()
    etime = scrapy.Field()

class ChezhiwangReportItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()