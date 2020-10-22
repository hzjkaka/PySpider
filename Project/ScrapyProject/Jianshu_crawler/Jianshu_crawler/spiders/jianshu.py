# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Jianshu_crawler.items import JianshuCrawlerItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(
            LinkExtractor(
                allow=r'.*/p/[0-9a-z]{12}.*'),
            callback='parse_detail',
            follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        avatar = response.xpath(
            "//a[@class='_1OhGeD']/img[@class='_13D2Eh']/@src").get()
        content = response.xpath("//article[@class='_2rhmJa']").get()
        author = response.xpath("//span[@class='FxYr8x']/a/text()").get()
        date1 = response.xpath("//span[@class='FxYr8x']/a/text()")
        date = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        print(date1)
        word_count = response.xpath(
            "//div[@class='s-dsoj']/span[2]/text()").get().replace("字数",'').strip()
        read_count = response.xpath(
            "//div[@class='s-dsoj']/span[3]/text()").get().replace("阅读",'').strip()
        like_count = response.xpath(
            "//span[@class='_1GPnWJ']/text()").get().replace('赞','').strip()
        subjects = ','.join(response.xpath(
            "//div/a/span[@class='_2-Djqu']/text()").getall())
        url1 = response.url
        url1 = url1.split('?')[0]
        article_id = url1.split('/')[-1]
        item = JianshuCrawlerItem(
            title=title,
            avatar=avatar,
            content=content,
            author=author,
            date=date,
            origin_url=response.url,
            article_id=article_id,
            word_count=word_count,
            read_count=read_count,
            like_count=like_count,
            subjects=subjects
        )
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
