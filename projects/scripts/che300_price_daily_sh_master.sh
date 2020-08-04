#!/bin/bash
project="che300_new"
spider="che300_price_daily_sh_city_master"
source /root/anaconda3/bin/activate base
cd /home/scrapy_projects/${project}/tools
nohup python -u ${spider}.py > /home/logs/${spider}.log 2>&1 &
