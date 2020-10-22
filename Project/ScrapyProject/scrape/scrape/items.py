# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cover = scrapy.Field()
    name = scrapy.Field()
    categories = scrapy.Field()
    location = scrapy.Field()
    published_at = scrapy.Field()
    drama = scrapy.Field()


