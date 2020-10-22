# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # '房屋名称':
    name = scrapy.Field()
    # '价格':
    price = scrapy.Field()
    # '发布时间':
    maintain_time = scrapy.Field()
    #'租赁方式'：
    rent = scrapy.Field()
    # '户型':
    house = scrapy.Field()
    #'位置':
    location = scrapy.Field()
    #'基本信息':
    basic_inf = scrapy.Field()
    #'基本配置':
    basic_con = scrapy.Field()
    #'房源描述':
    house_des = scrapy.Field()

    # '户型':
    # architecture = scrapy.Field()
    # # '面积': \
    # area = scrapy.Field()
    # # '朝向': \
    # orientation = scrapy.Field()
    # # '入住': \
    # ru_zhu = scrapy.Field()
    # # '租期': \
    # zu_qi = scrapy.Field()
    # # '看房': \
    # kan_fang = scrapy.Field()
    # # '楼层': \
    # floor = scrapy.Field()
    # # '电梯':\
    # lift = scrapy.Field()
    # # '车位': \
    # car = scrapy.Field()
    # # '用水':\
    # water = scrapy.Field()
    # # '用电': \
    # electric = scrapy.Field()
    # # '燃气': \
    # gas = scrapy.Field()
    # # '采暖': \
    # warm = scrapy.Field()
    # # '电视': \
    # television = scrapy.Field()
    # # '冰箱': \
    # refrigerator = scrapy.Field()
    # # '洗衣机': \
    # washing_machine = scrapy.Field()
    # # '空调': \
    # air_conditioner = scrapy.Field()
    # # '热水器': \
    # water_heater = scrapy.Field()
    # # '床': \
    # bed = scrapy.Field()
    # # '暖气': \
    # heating = scrapy.Field()
    # # '宽带': \
    # wifi = scrapy.Field()
    # # '衣柜': \
    # wardrobe =  scrapy.Field()
    # # '天然气':
    # natural_gas = scrapy.Field()
