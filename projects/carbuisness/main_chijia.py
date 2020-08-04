from scrapy.cmdline import execute

import sys
import os


website = "chijia_fixed_2019_add_location"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


