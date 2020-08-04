from scrapy.cmdline import execute

import sys
import os


website = "ershouche_trade_cangzhou"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


