from scrapy.cmdline import execute

import sys
import os
# from scrapy.conf import settings

weixinname = "wanchejiaoshou"
website = "weixin_%s" % weixinname
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


