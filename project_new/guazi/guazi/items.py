# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    grab_time = scrapy.Field()
    brandname = scrapy.Field()
    brand_id = scrapy.Field()
    familyname = scrapy.Field()
    family_id = scrapy.Field()
    vehicle = scrapy.Field()
    vehicle_id = scrapy.Field()
    years = scrapy.Field()
    transmission = scrapy.Field()
    emission_standard = scrapy.Field()
    seats = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()

