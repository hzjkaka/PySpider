# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.request import urlretrieve
from scrapy.pipelines.images import ImagesPipeline

from bmw import settings


class BmwPipeline(object):
    def __init__(self):
        #os.path.join()拼接路径
        #或者使用os.path.dirname(__file__)获取相对路径
        self.path = 'images'
        if not  os.path.exists(self.path):
            os.mkdir(self.path)
        else:
            print('文件夹已存在！')

    def process_item(self, item, spider):
        category = item['category']
        ims_urls = item['img_urls']
        category_path = os.path.join(self.path,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for img_url in ims_urls:
            img_name = img_url.split('_')[-1]
            urlretrieve(img_url,os.path.join(category_path,img_name))
        return item

class BMWImagesPiplines(ImagesPipeline):
    def get_media_requests(self, item, info):
        #这个方法是在下载请求之前被调用
        request_objs = super().get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        #该方法在图片采集存储的时候被调用，来获取图片的存储路径
        path = super().file_path(request,response,info)
        category = request.item.get('category')
        images_stores = settings.IMAGES_STORE
        category_path = os.path.join(images_stores,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/",'')
        image_path = os.path.join(category_path,image_name)
        return image_path
