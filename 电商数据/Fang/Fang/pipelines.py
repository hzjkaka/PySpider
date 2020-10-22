# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
class FangPipeline(object):
    def __init__(self):
        # 最好使用wb写入
        self.newhouse = open('newhouse.json', 'wb')
        self.esfhouse = open('esf.json', 'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse, ensure_ascii=False, encoding='utf-8')
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        # 一定记着返回给其他的pipline使用
        return item

    def close_spider(self, spider):
        self.newhouse.close()
        self.esfhouse.close()


