# -*- coding: utf-8 -*-
import scrapy
from LianJia.items import LianjiaItem

class LjSpider(scrapy.Spider):
    name = 'lj'
    allowed_domains = ['lianjia.com']
    start_urls = [f'https://sh.lianjia.com/zufang/pg{i}/' for i in range(1,11)]


    def parse(self,response):
        BASE_URL = 'https://hz.lianjia.com'
        urls = response.xpath('//p/a[@class="twoline"]/@href').extract()
        location1 = response.xpath('//p[@class="content__list--item--des"]/a/text()').extract()
        location2 = []
        # result = '-'.join(location2[i:i+3:])
        for i in range(0, len(location1), 3):
            b = '-'.join(location1[i:i + 3])
            location2.append(b)
        # step = 3
        # for j in range(0,len(location1)):
        #     location2 = [location1[i:i+step] for i in range(0,len(location1),step)]
        for key,vlaue in enumerate(urls):
            yield scrapy.Request(BASE_URL+ vlaue ,meta={'location':location2[key]},callback=self.parse_detail)

    def parse_detail(self, response):
        location = response.meta['location']
        name = response.xpath('//p[@class="content__title"]/text()').extract_first()
        price = response.xpath('//div[@class="content__aside--title"]/span/text()').extract_first()
        maintain_time = response.xpath('//div[@class="content__subtitle"]/text()').extract_first().strip()
        rent = response.xpath('//ul[@class="content__aside__list"]/li[1]/text()').extract_first()
        house = response.xpath('//ul[@class="content__aside__list"]/li[2]/text()').extract_first()
        # '基本信息':
        basic_inf = ','.join(response.xpath('//div[@id ="info"]/ul[1]//text()').extract()).replace(' ','').replace('\\n','').replace('\xa0','')
        # '基本配置':注意有个空格
        basic_con = ','.join(response.xpath('//ul[@class="content__article__info2"]/li[@class="fl oneline  "]//text()').extract()).replace(' ','')
        # basic_con ={}
        # '房源描述':
        house_des = ' '.join(response.xpath('//p[@data-el="houseComment"]/text()').extract())


        item = LianjiaItem(name=name, price=price, maintain_time=maintain_time, location=location, rent=rent,
                           house=house, basic_inf=basic_inf, basic_con=basic_con, house_des=house_des)
        yield item