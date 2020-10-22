# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db,mongo_col):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_CONNECTION'),
                   mongo_db=crawler.settings.get('MONGO_DB_NAME'),
                   mongo_col=crawler.settings.get('MONGO_COLLECTION_NAME')
                   )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.col = self.db[self.mongo_col]

    def process_item(self, item, spider):
        self.col.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()