# -*- coding: utf-8 -*-

# Scrapy settings for chesupai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chesupai'

SPIDER_MODULES = ['chesupai.spiders']
NEWSPIDER_MODULE = 'chesupai.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'chesupai (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

""" mongodb 配置 """
# MONGODB 主机环回地址127.0.0.1
MONGODB_SERVER = '192.168.1.94'
# MONGODB_SERVER = '127.0.0.1'
# 端口号，默认是27017
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DB = 'usedcar'
# 存放本次数据的表名称
MONGODB_COLLECTION = 'chesupai_2019_9'
CRAWL_NUM = 2000000

""" mysql 配置"""
MYSQL_DB = 'usedcar_update'
MYSQL_TABLE = 'chesupai_online'
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.1.94'
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"
# MYSQL_SERVER = '127.0.0.1'
# MYSQL_USER = "dataUser94"
# MYSQL_PWD = 'yangkaiqi'


""" log """
LOG_LEVEL = "INFO"
#LOG_LEVEL="DEBUG"
#LOG_FILE ="scrapy.log"


BLM_PATH = "/root/blm/chesupai"
PHANTOMJS_PATH = "/usr/local/phantomjs/bin/phantomjs"
CHROME_PATH = "/root/chromedriver"
FIREFOX_PATH = "/home/firefox/geckodriver"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'chesupai.middlewares.ChesupaiSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'chesupai.middlewares.RotateUserAgentMiddleware': 543,
   # 'chesupai.middlewares.ProxyMiddleware': 500,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'chesupai.pipelines.ChesupaiPipeline': 300,
   # 'scrapy_redis.pipelines.RedisPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# SCHEDULER = 'chesupai.scrapy_redis.scheduler.Scheduler'
# SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = 'chesupai.scrapy_redis.queue.SpiderPriorityQueue'
# # SCHEDULER_QUEUE_CLASS = 'chesupai.scrapy_redis.queue.SpiderSimpleQueue'
#
""" scrapy-redis配置 """
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# REDIS_URL = 'redis://root:redis@127.0.0.1:6379'
REDIS_URL = 'redis://127.0.0.1:6379'
REDIS_HOST = "127.0.0.1"
# REDIS_URL = 'redis://192.168.1.92:6379'
# REDIS_HOST = "192.168.1.92"
#
# SCHEDULER_PERSIST = True


""" 爬取深度与爬取方式 """
#1、爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
# DEPTH_LIMIT = 3

#2、爬取时，0表示深度优先Lifo(默认)；1表示广度优先FiFo

# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'

# 先进先出，广度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'