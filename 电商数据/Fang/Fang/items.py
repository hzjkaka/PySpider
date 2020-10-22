# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #省份
    province = scrapy.Field()
    #城市
    city = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    #小区名称
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #面积
    area = scrapy.Field()
    #地址
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #在售情况
    sale = scrapy.Field()
    #详情页url
    detail_url = scrapy.Field()

class EsfHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名称
    name = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 面积
    area = scrapy.Field()
    #总价
    price = scrapy.Field()
    #单价
    unit = scrapy.Field()
    # 详情页url
    detail_url = scrapy.Field()