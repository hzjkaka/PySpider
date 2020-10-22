# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''
    保存分类的pipeline类


'''
from JD.spiders.category_spider import CategorySpider
import pymongo
from JD.settings import MONGODB_URL
class CategoryPipeline(object):
    def open_spider(self,spider):
        ''':param
                当爬虫是分类爬虫时启动
                '''
        if isinstance(spider, CategorySpider):
            #链接MongoDB
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.col = self.client['JD']['category']

    def process_item(self, item, spider):
        #向Mongodb中插入数据
        if isinstance(spider,CategorySpider):
           self.col.insert_one(dict(item))
        #注意别忘了返回item
        return item

    def close_spider(self,spider):
        if isinstance(spider,CategorySpider):
            self.client.close()

from JD.spiders.product_spider import ProductSpider
from JD.items import ProductItem,ProductAdItem,ShopItem,ProductCommentsItem
class ProductPipeline(object):
    def  open_spider(self,spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider,ProductSpider):
            #1.open_spider方法中，链接mongodb数据库，获取要操作的集合
            self.client = pymongo.MongoClient(MONGODB_URL)
            self.db = self.client['JD']
            self.collection1 = self.db['product']
            self.collection2 = self.db['ad']
            self.collection3 = self.db['shop']
            self.collection4 = self.db['comments']
            self.collection5 = self.db['price']

    def process_item(self, item, spider):
        #2.process_item : mongodb中插入数据
        if isinstance(item,ProductItem):
            self.collection1.insert_one(dict(item))
        elif isinstance(item,ProductAdItem):
            self.collection2.insert_one(dict(item))
        elif isinstance(item, ShopItem):
            self.collection3.insert_one(dict(item))
        elif isinstance(item, ProductCommentsItem):
            self.collection4.insert_one(dict(item))
        else:
            self.collection5.insert_one(dict(item))
            print("插入成功")
        return item

    def close_spider(self,spider):
        #3.close_spider:关闭mongodb
        if isinstance(spider,ProductSpider):
            self.client.close()