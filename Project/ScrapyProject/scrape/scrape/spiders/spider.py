# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrape.items import ScrapeItem

class SpiderSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['static1.scrape.cuiqingcai.com']
    start_urls = ['https://static1.scrape.cuiqingcai.com/page/1']
    rules = (
        Rule(LinkExtractor(allow=r'.+\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+detail/\d'), callback='parse_detail', follow=False),
    )
    def parse_detail(self, response):
        cover = response.xpath("//img[@class='cover']/@src").get()
        name = response.xpath("//h2[@class='m-b-sm']/text()").get()
        categories ="".join(response.xpath("//div[@class='categories']//text()").getall()).replace(' ','').replace('\n','')
        location = response.xpath("//div[@class='m-v-sm info']/span/text()").getall()[0]
        published_at = response.xpath("//div[@class='m-v-sm info']/span/text()").getall()[3].strip("上映")
        drama = response.xpath("//div[@class='drama']/p/text()").get().replace("\n",'').strip()
        item = ScrapeItem(cover=cover,name=name,categories=categories,location=location,published_at=published_at,drama=drama)
        print("="*40)
        print(item)
        yield item
