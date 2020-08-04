from scrapy.cmdline import execute

import sys
import os


website = "newhouse_fang_2018"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


