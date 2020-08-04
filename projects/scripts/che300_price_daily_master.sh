#!/bin/bash
project="che300_new"
spider="push_che300_pricedaily_url2redis"
source /root/anaconda3/bin/activate base
cd /home/scrapy_projects/${project}/tools
nohup python -u ${spider}.py > /home/logs/${spider}.log 2>&1 &
