# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from WxApp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback='parse_detail' ,follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').extract_first()
        author = response.xpath('//p[@class="authors"]/a/text()').extract_first()
        date = response.xpath('//p[@class="authors"]/span/text()').extract_first()
        contents = response.xpath('//td[@id="article_content"]//text()').extract()
        content =''.join(contents).strip()
        item = WxappItem(title=title,author=author,date=date,content=content)
        yield  item
