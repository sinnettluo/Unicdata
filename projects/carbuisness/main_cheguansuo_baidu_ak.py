from scrapy.cmdline import execute

import sys
import os


website = "cheguansuo_baidu_ak_new"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


