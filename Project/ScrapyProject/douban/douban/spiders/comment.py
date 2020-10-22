# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban.items import DoubanItem

class CommentSpider(CrawlSpider):
    name = 'comment'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/review/best/?start=10']

    rules = (
        Rule(LinkExtractor(allow=r'.+\?start=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+\d+/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath("//header[@class='main-hd']/a[2]/text()").get()
        summary = response.xpath("//div[@class='article']/h1/span/text()").get()
        author = response.xpath("//div/@data-author").get()
        rank = response.xpath("//header[@class='main-hd']/span[2]/text()").get()
        date = response.xpath("//header[@class='main-hd']/span[3]/text()").get()
        item = DoubanItem(title=title,summary=summary,author=author,rank=rank,date=date)
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield  item
