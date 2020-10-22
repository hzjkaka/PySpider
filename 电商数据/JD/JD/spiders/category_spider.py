# -*- coding: utf-8 -*-
import scrapy
import json
# import jsonpath
from JD.items import CategoryItem
import logging



class CategorySpider(scrapy.Spider):
    name = 'category_spider'
    #1.修改域名
    allowed_domains = ['3.cn']
    #2.指定起始URL
    start_urls = ['https://dc.3.cn/category/get']

    def parse(self, response):
        # print(response.body.decode("GBK"))
        res = json.loads(response.body.decode("GBK"))
        datas = res["data"]
        item = CategoryItem()
        #遍历数据列表
        for data in datas:
            #大分类
            b_category = data['s'][0]
            #大分类的信息
            b_category_inf = b_category['n']
            # print('大分类：{}'.format(b_category_inf))
            item['b_c_name'],item['b_c_url']= self.get_catrgory_url(b_category_inf)
            #中分类
            m_categories = b_category['s']
            for m_category in m_categories:
                #中分类信息
                m_category_inf = m_category['n']
                item['m_c_name'], item['m_c_url'] = self.get_catrgory_url(m_category_inf)

                # print('中分类：{}'.format(m_category_inf))
                #小分类
                s_categories = m_category['s']
                for s_category in s_categories:
                    #小分类信息
                    s_category_inf = s_category['n']
                    item['s_c_name'],item['s_c_url'] = self.get_catrgory_url(s_category_inf)
                    logging.debug(item)
                    # print(item)
                    yield item
                    # print('小分类：{}'.format(s_category_inf))
    def get_catrgory_url(self,category_inf):
        '''
        根据分类信息，提取并凭借URL和对应的名称
        :param category_inf :各种分类的信息
        :return 分类的名称和URL
        '''
        category_list = category_inf.split('|')
        #URL
        category_url = category_list[0]
        #名称
        category_name = category_list[1]
        # URL处理1：第一类URL
        if category_url.count("jd.com")==1:
            # 拼接URL
            category_url = 'https://'+category_url
        elif category_url.count('-')==1:
            #处理2：
            ca = category_url
            category_url = f'https://channel.jd.com/{ca}.html'
        else:
            #处理3：
            #替换URL的‘-’为‘,’
            category_url = 'https://list.jd.com/list.html?cat={}'.format(category_url)
        return category_name,category_url



