# -*- coding: utf-8 -*-

# Scrapy settings for carbuisness project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'carbuisness'

SPIDER_MODULES = ['carbuisness.spiders']
NEWSPIDER_MODULE = 'carbuisness.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'carbuisness (+http://www.yourdomain.com)'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# RANDOMIZE_DOWNLOAD_DELAY=True
# DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'carbuisness.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'carbuisness.middlewares.MyCustomDownloaderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    # 'carbuisness.rotate_useragent.RotateUserAgentMiddleware': 543,  #543
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'carbuisness.rotate_useragent.ProxyMiddleware': 300,  #300
    'carbuisness.rotate_useragent.SeleniumMiddleware': 400,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,
    # 'carbuisness.middlewares.MyproxiesSpiderMiddleware':None,
    'carbuisness.rotate_useragent.TTPaiMiddleware': 500,
    'carbuisness.rotate_useragent.LechebangMiddleware': 600,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


HTTPERROR_ALLOWED_CODES=[]
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'carbuisness.pipelines.CarbuisnessPipeline': 300,

}

MONGODB_SERVER = "192.168.1.94"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"
CrawlCar_Num = 2000000


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

MAIL_FROM ="hzhy_1@163.com"
MAIL_HOST="smtp.163.com"
MAIL_PORT=25
MAIL_USER="hzhy_1@163.com"
MAIL_PASS="Hzhy@7115240"

#log
# LOG_LEVEL="INFO"
LOG_LEVEL="DEBUG"
#LOG_FILE ="scrapy.log"

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# RETRY_ENABLED = True
RETRY_TIMES = 8
# DOWNLOAD_TIMEOUT = 6

# BLM_PATH = "blm/"
# PHANTOMJS_PATH = "D:/phantomjs.exe"
# CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# FIREFOX_PATH = "C:\Users\Admin\Downloads\IDA_Pro_v7.0_Portable\python27\geckodriver.exe"

BLM_PATH = "/home/usedcar/blm/"
PHANTOMJS_PATH = "/root/phantomjs/bin/phantomjs"
CHROME_PATH = "/root/chromedriver"
FIREFOX_PATH = "D:/geckodriver.exe"

RETRY_HTTP_CODES = [403, 503]
# REDIRECT_ENABLED = False

WEIXIN = "neshidai"