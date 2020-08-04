from scrapy.cmdline import execute

import sys
import os


website = "jzg_price_test_img_2019_for_cities2"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


