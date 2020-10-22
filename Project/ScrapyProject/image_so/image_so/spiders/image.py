# -*- coding: utf-8 -*-
import scrapy
from image_so.items import ImageSoItem

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.so.com']
    start_urls = ['https://image.so.com/z?ch=beauty']

    def parse(self, response):
        name = response.xpath("//h2[@class='title']/a/@title").get()
        image_urls = response.xpath("//a[@class='image']/img/@src").get()
        item = ImageSoItem(name=name,image_urls=image_urls)
        print(item)
        yield item
