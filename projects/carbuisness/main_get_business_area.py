from scrapy.cmdline import execute

import sys
import os


website = "get_business_area_for_geo"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


