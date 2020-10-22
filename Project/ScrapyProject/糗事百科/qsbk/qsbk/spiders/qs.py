# -*- coding: utf-8 -*-
import scrapy
class QsSpider(scrapy.Spider):
    name = 'qs'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        print(type(response))
        divs  = response.xpath('//div[@id="content-left"]/div')
        print(divs)
        for div in divs:
            # selector
            author = div.xpath('.//h2/text()').extract_first().strip()
            content =div.xpath()
            content =''.join(content).strip() #列表变成一个字符串
            print(author)