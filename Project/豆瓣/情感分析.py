# -*- coding: utf-8 -*-
"""
@File    : 情感分析.py
@Time    : 2020/9/26 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import pandas as pd
from snownlp import SnowNLP
#将评论进行情感分析
def convert(title):
    snow = SnowNLP(str(title))
    sen = snow.sentiments
    return sen

if __name__ == '__main__':
    data = pd.read_table('babai.csv',sep='\t')
    print(data.head(10))
    print(data.tail(10))
    r = data.title
    print(r)
    # data['情感评分'] = data.title.apply(convert)
    # data.sort_values(by='情感评分',ascending =False,inplace=True)
    # #保存
    # data.to_csv('./snowNLP.csv',sep='\t',index=False)

