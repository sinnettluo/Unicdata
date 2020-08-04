from scrapy.cmdline import execute

import sys
import os


website = "weather_tianqihoubao_ry"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


