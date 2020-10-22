# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#类别数据类：用于存储类别信息（category）-字段
class CategoryItem(scrapy.Item):
    #大，中，小分类的name和url
    b_c_name = scrapy.Field()
    b_c_url = scrapy.Field()
    m_c_name = scrapy.Field()
    m_c_url = scrapy.Field()
    s_c_name = scrapy.Field()
    s_c_url = scrapy.Field()

#商品的数据模型
class ProductItem(scrapy.Item):
    p_category = scrapy.Field()
    p_url = scrapy.Field()
    p_sku_id  = scrapy.Field()
    p_name = scrapy.Field()
    p_img_url = scrapy.Field()
    #图书信息，作者，出版社
    p_book_info = scrapy.Field()
    #商品选项
    p_option = scrapy.Field()
    p_price = scrapy.Field()

#店铺的数据模型
class ShopItem(scrapy.Item):
    p_sku_id = scrapy.Field()
    p_category_id = scrapy.Field()
    p_shop_id = scrapy.Field()
    p_shop_name = scrapy.Field()
    p_shop_url = scrapy.Field()
    
#促销信息的数据模型
class ProductAdItem(scrapy.Item):
    p_sku_id = scrapy.Field()
    ad_url = scrapy.Field()
    ad_text = scrapy.Field()

#商品促销信息的数据模型
class ProductCommentsItem(scrapy.Item):
    p_sku_id = scrapy.Field()
    commentCount = scrapy.Field()
    goodCount = scrapy.Field()
    poorCount = scrapy.Field()
    goodRate = scrapy.Field()
#商品价格信息
class ProductPriceItem(scrapy.Item):
    p_sku_id = scrapy.Field()
    price = scrapy.Field()











