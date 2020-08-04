# -*- coding: utf-8 -*-

# Scrapy settings for che300 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'che300'

SPIDER_MODULES = ['che300.spiders']
NEWSPIDER_MODULE = 'che300.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2050.400 QQBrowser/9.5.10169.400'
#
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# RANDOMIZE_DOWNLOAD_DELAY=True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 100
# DOWNLOAD_TIMEOUT = 3
RETRY_ENABLED = True
RETRY_TIMES = 8
# CONCURRENT_REQUESTS_PER_DOMAIN=100
# CONCURRENT_REQUESTS_PER_IP=100
# ##downcontrol
# #CONCURRENT_ITEMS = 1000
# REACTOR_THREADPOOL_MAXSIZE = 20
# REDIRECT_ENABLED = False

# The download delay setting will honor only one of:


# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'che300.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'che300.middlewares.MyCustomDownloaderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    # 'che300.rotate_useragent.RotateUserAgentMiddleware': 100,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'che300.rotate_useragent.ProxyMiddleware': 200,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'che300.pipelines.che300Pipeline': 300,
}

# MONGODB_SERVER = "121.43.181.59"
# MONGODB_SERVER = "localhost"
# MONGODB_SERVER = "121.196.222.206"
MONGODB_SERVER = "192.168.1.94"

MONGODB_PORT = 27017
MONGODB_DB = "usedcar_evaluation"
MONGODB_COLLECTION = "aika_detail"
CrawlCar_Num = 200000000
MYSQLIP = '192.168.1.94'
MYSQLPORT = 3306
MYSQLUSER = 'root'
MYSQLPASS = 'Datauser@2017'
DATABASE = 'for_android'
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Mail settings
MAIL_FROM = "hzhy_1@163.com"
MAIL_HOST = "smtp.163.com"
MAIL_PORT = 25
MAIL_USER = "hzhy_1@163.com"
MAIL_PASS = "Hzhy@7115240"

# log
LOG_LEVEL = "INFO"

UPDATE_CODE = '201912_01'

RETRY_HTTP_CODES = [403]

# BLM_PATH = "blm/"
# PHANTOMJS_PATH = "D:/phantomjs.exe"
# CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# FIREFOX_PATH = "C:\Users\Admin\Downloads\IDA_Pro_v7.0_Portable\python27\geckodriver.exe"

BLM_PATH = "/home/usedcar/blm/"
PHANTOMJS_PATH = "/root/phantomjs/bin/phantomjs"
CHROME_PATH = "/root/chromedriver"
FIREFOX_PATH = "D:/geckodriver.exe"
REDIS_SERVER ="192.168.1.249"
REDIS_DB=2