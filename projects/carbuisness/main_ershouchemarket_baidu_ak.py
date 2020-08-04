from scrapy.cmdline import execute

import sys
import os


website = "ershouchemarket_baidu_ak"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


