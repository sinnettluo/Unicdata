from scrapy.cmdline import execute

import sys
import os


website = "huasheng_price_compare"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


