# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XinlangItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    screen_name = scrapy.Field()
    gender = scrapy.Field()
    user_id = scrapy.Field()
    create_time = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    brand = scrapy.Field()
    grabtime = scrapy.Field()



