from scrapy.cmdline import execute

import sys
import os


website = "sunning_mobile_phone"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


