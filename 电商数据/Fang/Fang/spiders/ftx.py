# -*- coding: utf-8 -*-
import re

import scrapy
from Fang.items import NewhouseItem
from Fang.items import EsfHouseItem


class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            td_province = tds[0]
            province_text = td_province.xpath('.//text()').get()
            province_text = re.sub(r'\s', '', province_text)
            # 有省份标签就保存当前的，没有就是用前面的
            if province_text:
                province = province_text
            # 不爬取海外
            if province == '其它':
                continue
            td_city = tds[1]
            city_links = td_city.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                # 构建新房的URL
                urls = city_url.split('.', 1)
                s1 = urls[0]
                s2 = urls[1]
                if 'bj' in s1:
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com/'
                else:
                    newhouse_url = s1 + '.newhouse.' + s2 + 'house/s/'
                    # 构建二手房URL
                    esf_url = s1 + '.esf.' + s2
                # print('新房：%s'%newhouse_url)
                # print('二手房：%s'%esf_url)
                yield scrapy.Request(url=newhouse_url, callback=self.newhouse, meta={'info': (province, city)})
                yield scrapy.Request(url=esf_url,callback=self.esf,meta={'info':(province,city)})


    def newhouse(self, response):
        # 传递加上元组解包
        province, city = response.meta.get('info')
        lis = response.xpath('//div[contains(@class,"nl_con")]/ul/li')
        for li in lis:
            name = ''.join(
                li.xpath(".//div[@class='nlcd_name']/a/text()").getall()).strip()
            print(name)
            house_type = li.xpath(
                ".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type = list(map(lambda x: re.sub(r'\s', '', x), house_type))
            rooms = list(filter(lambda x: x.endswith('居'), house_type))
            area = ''.join(
                li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall())
            area = re.sub(r'\s|-|/', '', area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district_ = ''.join(
                li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.sub(r'\s', '', district_)
            sale = li.xpath(
                ".//div[contains(@class,'fangyuan')]/span/text()").get()
            price = ''.join(
                li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r'\s|广告', '', price)
            detail_url = response.urljoin(
                li.xpath('.//div[@class="nlcd_name"]/a/@href').get())
            item = NewhouseItem(
                province=province,
                city=city,
                name=name,
                rooms=rooms,
                area=area,
                address=address,
                district=district,
                sale=sale,
                price=price,
                detail_url=detail_url)
            print(item)
            yield item
            next_url = response.xpath(
                '//a[contains(text(),"下一页")]/@href').get()
            if next_url:
                yield scrapy.Request(url=response.urljoin(next_url), callback=self.newhouse, meta={'info': (province, city)})

    def esf(self, response):
        province, city = response.meta.get('info')
        item = EsfHouseItem(province=province, city=city)
        dls = response.xpath('//div[@class="shop_list shop_list_4"]/dl')
        for dl in dls:
            name = dl.xpath(
                './/p[@class="add_shop"]/a/text()').get('未显示名称').replace('\n', '').replace('\t', '')
            infos = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
            infos = list(map(lambda x: re.sub(r'\s', '', x), infos))
            item['name'] = name
            for info in infos:
                if '厅' in info:
                    item['rooms'] = info
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                elif '建' in info:
                    item['year'] = info.replace('建', '')
                elif '㎡' in info:
                    item['area'] = info

            address = dl.xpath(
                './/p[@class="add_shop"]/span/text()').get('无地址')
            item['address'] = address
            item['unit'] = dl.xpath('//dd/span[2]/text()').get('0')
            item['price'] = ''.join(
                dl.xpath('.//dd/span[1]//text()').getall()[1:])
            item['detail_url'] = response.urljoin(
                dl.xpath('.//dd/h4/a/@href').get())
            # print(item)
            # print('=' * 30)
            yield item
        next_url = response.xpath('//p/a[contains(text(),"下一页")]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.esf, meta={'info': (province, city)})
