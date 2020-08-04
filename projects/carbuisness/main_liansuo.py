from scrapy.cmdline import execute

import sys
import os


website = "liansuo_%s_baidu_ak" % "jinuochewu2019"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


