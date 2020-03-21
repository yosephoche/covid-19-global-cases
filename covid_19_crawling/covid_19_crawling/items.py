# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Covid19CrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    country_region = scrapy.Field()
    province_state = scrapy.Field()
    confirmed = scrapy.Field()
    deaths = scrapy.Field()
    recovered = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    last_updated = scrapy.Field()