# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class ImageSoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'images'
    image_urls = Field()
    name = Field()

