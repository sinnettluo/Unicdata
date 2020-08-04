from scrapy.cmdline import execute

import sys
import os


website = "4sdian_baidu_ak_2019"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


