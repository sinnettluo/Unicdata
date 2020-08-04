# -*- coding: utf-8 -*-

# Scrapy settings for koubei project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'koubei'
SPIDER_MODULES = ['koubei.spiders']
NEWSPIDER_MODULE = 'koubei.spiders'

RETRY_ENABLED = True
RETRY_TIMES = 8
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'koubei (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# RANDOM_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'koubei.middlewares.KoubeiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'koubei.middlewares.KoubeiDownloaderMiddleware': 543,
   'koubei.proxy.ProxyMiddleware': 500,
   'koubei.proxy.SeleniumMiddleware' : 400,
   'koubei.proxy.LechebangMiddleware': 600,
   'koubei.proxy.GangMiddleware': 700,
   # 'koubei.middlewares.RandomUserAgentMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'koubei.pipelines.KoubeiPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MONGODB_SERVER = "192.168.1.92"
MONGODB_PORT = 27017
MONGODB_DB = ""
MONGODB_COLLECTION = ""
CrawlCar_Num = 2000000

WEIXIN = "qichezhijia"

BLM_PATH = "blm/"
PHANTOMJS_PATH = "D:/phantomjs.exe"
CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# FIREFOX_PATH = "C:\Users\Admin\Downloads\IDA_Pro_v7.0_Portable\python27\geckodriver.exe"

# BLM_PATH = "/home/usedcar/blm/"
# PHANTOMJS_PATH = "/root/phantomjs/bin/phantomjs"
# CHROME_PATH = "/root/chromedriver"
# FIREFOX_PATH = "D:/geckodriver.exe"
# HRTTPERROR_ALLOWED_CODES = [302]
REDIS_SERVER ="192.168.1.248"
REDIS_PORT =6379

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

CITY = {'北京': 'bj', '上海': 'sh', '成都': 'cd', '重庆': 'cq', '广州': 'gz', '安顺': 'anshun', '鞍山': 'anshan', '安阳': 'anyang', '安庆': 'anqing', '安康': 'ankang', '巴中': 'bazhong', '毕节': 'bijie', '保定': 'baoding', '滨州': 'binzhoozhou', '包头': 'baotou', '宝鸡': 'baoji', '朝阳市': 'chaoyang', '常州': 'changzhou', '承德': 'chengde', '沧州': 'cangzhou', '长春': 'cc', '滁州': 'chuzhou', '赤峰': 'chifeng', '长治': 'changzhi', '长沙': 'cs', '常德': 'changde', '东莞': 'dg', '德阳': 'deyang', '达州': 'dazhou', '大连': 'dl', '丹东': 'dandong', '大庆': 'daqing', '东营': 'dongying', '德州': 'dezhou', '大同': 'datong', '大理': 'dali', '鄂尔多斯': 'eerduosi', '鄂州': 'ezhou', '恩施':'enshi', '抚顺': 'fushun', '福州': 'fz', '阜阳': 'fuyang', '抚州': 'jxfuzhou', '广元': 'guangyuan', '广安': 'guangan', '贵阳': 'gy', '桂林': 'gl', '赣州': 'ganzhou', '惠州': 'huizhou', '河源': 'heyuan', '杭州': 'hz', '湖州': 'huzhou', '淮安': 'huaian','邯郸': 'handan', '衡水': 'hengshui', '哈尔滨': 'hrb', '菏泽': 'heze', '合肥': 'hf', '淮南': 'huainan', '淮北': 'huaibei', '海口': 'hn', '呼和浩特': 'nmg', '汉中': 'hanzhong', '黄石': 'huangshi', '黄冈': 'huanggang', '衡阳': 'hengyangiangmen', '揭阳': 'jieyang', '嘉兴': 'jiaxing', '金华': 'jinhua', '锦州': 'jinzhou', '焦作': 'jiaozuo', '吉林': 'jilin', '佳木斯': 'jiamusi', '济南': 'jn', '济宁': 'jining', '晋城': 'jincheng', '晋中': 'jinzhong', '荆州': 'jingzhou', '九江': 'jiujiang', '吉安': 'jian', '开封': 'kaifeng', '昆明': 'km', '泸州': 'luzhou', '乐山': 'leshan', '丽水': 'lishui', '六盘水': 'liupanshui', '辽阳': 'liaoyang', '连云港': 'lianyungang', '龙岩': 'longyan', '廊坊':'langfang', '漯河': 'luohe', '临沂': 'linyi', '聊城': 'liaocheng', '六安': 'luan', '柳州': 'liuzhou', '临汾': 'linfen', '兰州': 'lz', '娄底': 'loudi', '茂名': 'maoming', '梅州': 'meizhou', '绵阳': 'mianyang', '眉山': 'meishan', '牡丹江':'mudanjiang' , '南充': 'nanchong', '内江': 'neijiang', '宁波': 'nb', '南京': 'nj', '南通': 'nantong', '南平': 'nanping', '宁德': 'ningde', '南阳': 'nanyang', '南宁': 'nn', '南昌': 'nc', '攀枝花': 'panzhihua', '盘锦': 'panjin', '莆田': 'an', '濮阳': 'puyang', '萍乡': 'pingxiang', '清远': 'qingyuan', '衢州': 'quzhou', '泉州': 'quanzhou', '秦皇岛': 'qinhuangdao', '齐齐哈尔': 'qiqihaer', '青岛': 'qd', '钦州': 'qinzhou', '潜江': 'qianjiang', '曲靖': 'qujing', '日照':  'shantou', '汕尾': 'shanwei', '遂宁': 'suining', '绍兴': 'shaoxing', '沈阳': 'sy', '苏州': 'su', '宿迁': 'suqian', '三明': 'sanming', '石家庄': 'sjz', '三门峡': 'sanmenxia', '商丘': 'shangqiu', '四平': 'siping', '松原': 'songyuan' 'ahsuzhou', '榆林': 'sxyulin', '十堰': 'shiyan', '随州': 'suizhou', '邵阳': 'shaoyang', '上饶': 'shangrao', '天津': 'tj', '台州': 'zjtaizhou', '铁岭': 'tieling', '泰州': 'jstaizhou', '唐山': 'tangshan', '泰安': 'taian', '铜陵':'tongling', '温州': 'wenzhou', '无锡': 'wx', '威海': 'wei', '潍坊': 'weifang', '芜湖': 'wuhu', '梧州': 'wuzhou', '渭南': 'weinan', '武汉': 'wh', '乌鲁木齐': 'xj', '徐州': 'xuzhou', '厦门': 'xm', '邢台': 'xingtai', '新乡': 'xinxiang', '许昌': 'xuchang', '西安': 'xa', '西宁': 'xn', '襄阳': 'xiangyang', '孝感': 'xiaogan', '咸宁': 'xianning', '湘潭': 'xiangtan', '新余': 'xinyu', '阳江': 'yangjiang', '云浮': 'yunfu', '宜宾': 'yibin', '雅安': 'yaan', '营口': 'yingkou', '烟台': 'yantai', '玉林': 'yulin', '阳泉': 'yangquan', '运城': 'yuncheng', '银川': 'yc', '延安': 'yanan', '宜昌': 'yichang', '岳阳': 'yueyang', '永州': 'yongzhou', '益阳': 'yiyang', '宜春': 'jxyichun', '玉溪': 'yuxi', '': 'zhongshan', '湛江': 'zhanjiang', '肇庆': 'zhaoqing', '自贡': 'zigong', '资阳': 'ziyang', '遵义': 'zunyi', '镇江': 'zhenjiang', '漳州': 'zhangzhou', '郑州': 'zz', '周口': 'zhoukou', '驻马店': 'zhumadian', '淄博': 'zibo', '枣庄': 'zaozhuang', '昭通': 'zhaotong'}
