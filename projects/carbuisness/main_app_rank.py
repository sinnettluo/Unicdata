from scrapy.cmdline import execute

import sys
import os


website = "app_rank"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


