import re
import requests
from fontTools.ttLib import TTFont
from lxml import etree
from pymongo import MongoClient
def decrypt_font(url, headers):
    '''
    输入：链接和头部信息
    输出：返回解决字体反爬后的页面源码

    '''

    font1 = TTFont('./fonts/base.woff')
    # 使用百度的FontEditor找到本地字体文件name和数字之间的对应关系, 保存到字典中
    base_dict = {'uniE18E': '3', 'uniE585': '2', 'uniE194': '9', 'uniF439': '4', 'uniE7DB': '7', 'uniF115': '0',
                 'uniF0A4': '5', 'uniE311': '1', 'uniF7EF': '8', 'uniEACB': '6'}
    name_list1 = font1.getGlyphNames()[1:-1]
    response = requests.get(url, headers).text
    # 正则匹配字体woff文件
    font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', response)[0]
    url2 = 'http://vfile.meituan.net/colorstone/' + font_file
    new_file = requests.get(url2, headers)
    with open('./fonts/' + font_file, 'wb') as f:
        f.write(new_file.content)
    font2 = TTFont('./fonts/' + font_file)
    # font2.saveXML('font_2.xml')
    name_list2 = font2.getGlyphNames()[1:-1]
    # 构造新映射
    new_dict = {}
    for name2 in name_list2:
        number_diff = {}
        obj2 = font2['glyf'][name2].coordinates
        for name1 in name_list1:
            obj1 = font1['glyf'][name1].coordinates
            # 对象相等则说明对应的数字相同​
            diff = 0
            # 猫眼电影每次刷新，形状是不一样的
            # glyph这个属性记录的是字体的坐标
            # 求坐标的最小差值就可以了--k近邻思想
            # diff = 0
            # for coor1,coor2 in zip(glyph.coordinates,currentGlyph.coordinates):
            #     diff += abs(coor1[0]-coor2[0])+abs(coor1[1]-coor2[1])
            for coor2 in obj2:
                coor_diff = []
                for coor1 in obj1:
                    coor_diff.append(abs(coor2[0] - coor1[0]) + abs(coor2[1] - coor1[1]))
                    # print(coor_diff)
                diff += min(coor_diff)
            number_diff["number"] = diff
            if  min(number_diff,key=number_diff.get):
                new_dict[name2] = base_dict[name1]

    for i in name_list2:
        pattern = '&#x' + i[3:].lower() + ';'
        response = re.sub(pattern, new_dict[i], response)
    return response

def get_info(response):
    '''
    输入：页面源码
    输出：包含电影票房等信息的字典列表
    '''
    # Mongo配置
    conn = MongoClient('localhost', 27017)
    db = conn.maoyan  # 连接maoyan数据库，没有则自动创建
    col = db.film  # 使用film集合，没有则自动创建
    items = []
    html = etree.HTML(response)
    film_name = html.xpath('//div[@class="movie-item-info"]/p/a/text()')
    booking_office_today = html.xpath(
        '//div[@class="movie-item-number boxoffice"]/p[@class="realtime"]/span/span/text()')
    booking_office_total = html.xpath(
        '//div[@class="movie-item-number boxoffice"]/p[@class="total-boxoffice"]/span/span/text()')
    a = html.xpath('//div[@class="movie-item-number boxoffice"]/p[@class="realtime"]/text()')[1::2]
    b = html.xpath('//div[@class="movie-item-number boxoffice"]/p[@class="total-boxoffice"]/text()')[1::2]
    for i in range(len(film_name)):
        item = {'film_name': film_name[i],
                'booking_office_today': booking_office_today[i] + a[i].replace('\n', ''),
                'booking_office_total': booking_office_total[i] + b[i].replace('\n', ''),
                }
        items.append(item)
        col.insert_one(item)
    return items

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    url = 'https://maoyan.com/board/1'
    r = decrypt_font(url, headers)
    info = get_info(r)
    print(info)