from scrapy.cmdline import execute

import sys
import os


website = "postcode138"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


