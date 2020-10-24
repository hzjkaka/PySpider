# -*- coding: utf-8 -*-
import json

import scrapy
from jsonpath import jsonpath
from JD.items import ProductItem,ShopItem,ProductAdItem,ProductCommentsItem,ProductPriceItem

import logging
class ProductSpider(scrapy.Spider):
    redis_key = None
    name = 'product_spider'
    allowed_domains = ['jd.com','3.cn']
    start_urls = ['https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar']
#     def start_requests(self):
#         #重写start_requests方法,使用分类信息来构造列表页
#         p_category =   { "b_c_name": "家用电器",
#                         "b_c_url": "https://jiadian.jd.com",
#                         "m_c_name": "电视",
#                         "m_c_url": "https://list.jd.com/list.html?cat=737,794,798",
#                         "s_c_name": "超薄电视",
#                         "s_c_url": "https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar"
#     }
#         yield scrapy.Request(url=p_category['s_c_url'],callback=self.parse,meta={'p_category':p_category})

    #解析列表页信息，获取详情页的URL和实现翻页
    def parse(self, response):
        p_category = response.meta['p_category']
        #各个商品的id号
        p_sku_ids = response.xpath("//li[contains(@class,'gl-item')]/@data-sku").getall()
        # logging.debug(p_sku_ids)
        # 构造各个商品详情页的URL
        for p_sku_id in p_sku_ids:
            item = ProductItem()
            item["p_category"] = p_category
            item["p_sku_id"] = p_sku_id
            p_base_url = 'https://cdnware.m.jd.com/c1/skuDetail/apple/7.3.0/{}.json'.format(p_sku_id)
            item["p_url"] = p_base_url
            yield scrapy.Request(url=p_base_url,callback=self.parse_product_info,meta={"item":item,'p_sku_id':p_sku_id})
        # 实现翻页
        for i in range(1, 101):
            next_url = 'https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&page={}'.format(i * 2 - 1)
            if next_url:
                yield scrapy.Request(url=next_url, callback=self.parse, meta={'p_category': p_category})

    #解析商品的基本信息
    def parse_product_info(self,response):
        #取出数据
        item = response.meta['item']
        p_sku_id = response.meta['p_sku_id']
        item['p_sku_id'] = p_sku_id
        # logging.debug(item)
        '''
        scrapy中response.body 与 response.text区别
        body http响应正文， byte类型
        text 文本形式的http正文，str类型，它是response.body经过response.encoding
        经过解码得到:
        response.text = response.body.decode(response.encoding)
        '''
        result = json.loads(response.text)
        # 提取相关数据信息
        if 'wareInfo' in result:
            # 商品名称:p_name：
            item['p_name'] = result['wareInfo']['basicInfo']['name']
            # 商品图片url:p_img_url：
            item['p_img_url'] = result['wareInfo']['basicInfo']['wareImage'][0]['small']

            # 图书信息，作者，出版社:p_book_info
            item['p_book_info'] = result['wareInfo']['basicInfo']['bookInfo']
            #商品选项p_option
            color_size = jsonpath(result, '$..colorSize')
            if color_size:
                # 注意：coloe_size 是list of list
                color_size = color_size[0]
                product_option = {}
                for option in color_size:
                    title = option['title']
                    value = jsonpath(option, '$..text')
                    product_option[title] = value
                item['p_option'] = product_option
                # logging.debug(item)
                yield item
        item = ShopItem()
        p_sku_id = response.meta['p_sku_id']
        item['p_sku_id'] = p_sku_id
        result = json.loads(response.text)
        if  'wareInfo' in result:
            shop = jsonpath(result, '$..shop')
            if shop:
                shop = shop[0]
                if  shop:
                    item['p_shop_id'] = shop['shopId']
                    item['p_shop_name'] =  shop['name']
                    item['p_shop_url'] = shop['url']
                else:
                    item['p_shop_name'] = {'shop_name': '京东自营'}
            #  商品类别id:p_category_id
            item['p_category_id'] = result['wareInfo']['basicInfo']['category']
            # 需要把Category里面的数据进行相应的修改
            item['p_category_id'] = item['p_category_id'].replace(';', ",")
            # logging.debug(item)
        #商品促销信息的URL构建
            ad_url = "https://item-soa.jd.com/getWareBusiness?skuId={}&cat={}".format(p_sku_id,item['p_category_id'])
            yield scrapy.Request(url=ad_url,callback=self.parse_ad,meta={'ad_url':ad_url,'p_sku_id':p_sku_id})
            yield item
    # 商品促销广告的解析
    def parse_ad(self,response):
        ad_url = response.meta['ad_url']
        item = ProductAdItem()
        p_sku_id = response.meta['p_sku_id']
        item['p_sku_id'] = p_sku_id
        item['ad_url'] = ad_url
        # 把数据转换为字典
        result = json.loads(response.text)
        # 商品促销
        item['ad_text'] = jsonpath(result, '$..ad')
        # logging.debug(item)
        # 构建评价信息的请求URL
        comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(
           p_sku_id)
        yield scrapy.Request(comments_url, callback=self.parse_comments,meta={'p_sku_id':p_sku_id})
        yield item
    # 解析商品评价信息
    def parse_comments(self,response):
        result = json.loads(response.text)
        item = ProductCommentsItem()
        item['p_sku_id'] = response.meta['p_sku_id']
        p_sku_id = item['p_sku_id']
        item['commentCount']=jsonpath(result, '$..CommentCount')
        item['goodCount']= jsonpath(result, '$..GoodCount')
        item['poorCount']= jsonpath(result, '$..PoorCount')
        item['goodRate']= jsonpath(result, '$..GoodRate')
        # logging.debug(item)
        price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item["p_sku_id"])
        yield scrapy.Request(url=price_url,callback=self.parse_price,meta={'p_sku_id':p_sku_id})
        yield item
    # 解析商品的价格信息
    def  parse_price(self,response):
        result = json.loads(response.text)
        item = ProductPriceItem()
        p_sku_id = response.meta['p_sku_id']
        item['p_sku_id'] = p_sku_id
        price = jsonpath(result,'$..p')
        item['price'] = price
        # logging.debug(item)
        yield item
