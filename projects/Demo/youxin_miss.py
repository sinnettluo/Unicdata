from scrapy.cmdline import execute

import sys
import os

website = 'youxin_miss'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])