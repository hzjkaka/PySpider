# -*- coding: utf-8 -*-
"""
@File    : T1.py
@Time    : 2020/9/1 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
from lxml import etree

'''
大众点评是：不同文件中的同一个字，它们的字形坐标完全相同，但`Unicode`可能不同。
'''
import hashlib
import requests
import re
from parsel import Selector
from urllib import parse
from fontTools.ttLib import TTFont

old_font = TTFont('../大众点评/review.woff')
base_font = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '店', '中', '美', '家', '馆', '小', '车', '大', '市', '公',
             '酒', '行', '国', '品', '发', '电', '金', '心', '业', '商', '司', '超', '生', '装', '园', '场', '食', '有', '新', '限',
             '天', '面', '工', '服', '海', '华', '水', '房', '饰', '城', '乐', '汽', '香', '部', '利', '子', '老', '艺', '花', '专',
             '东', '肉', '菜', '学', '福', '饭', '人', '百', '餐', '茶', '务', '通', '味', '所', '山', '区', '门', '药', '银', '农',
             '龙', '停', '尚', '安', '广', '鑫', '一', '容', '动', '南', '具', '源', '兴', '鲜', '记', '时', '机', '烤', '文', '康',
             '信', '果', '阳', '理', '锅', '宝', '达', '地', '儿', '衣', '特', '产', '西', '批', '坊', '州', '牛', '佳', '化', '五',
             '米', '修', '爱', '北', '养', '卖', '建', '材', '三', '会', '鸡', '室', '红', '站', '德', '王', '光', '名', '丽', '油',
             '院', '堂', '烧', '江', '社', '合', '星', '货', '型', '村', '自', '科', '快', '便', '日', '民', '营', '和', '活', '童',
             '明', '器', '烟', '育', '宾', '精', '屋', '经', '居', '庄', '石', '顺', '林', '尔', '县', '手', '厅', '销', '用', '好',
             '客', '火', '雅', '盛', '体', '旅', '之', '鞋', '辣', '作', '粉', '包', '楼', '校', '鱼', '平', '彩', '上', '吧', '保',
             '永', '万', '物', '教', '吃', '设', '医', '正', '造', '丰', '健', '点', '汤', '网', '庆', '技', '斯', '洗', '料', '配',
             '汇', '木', '缘', '加', '麻', '联', '卫', '川', '泰', '色', '世', '方', '寓', '风', '幼', '羊', '烫', '来', '高', '厂',
             '兰', '阿', '贝', '皮', '全', '女', '拉', '成', '云', '维', '贸', '道', '术', '运', '都', '口', '博', '河', '瑞', '宏',
             '京', '际', '路', '祥', '青', '镇', '厨', '培', '力', '惠', '连', '马', '鸿', '钢', '训', '影', '甲', '助', '窗', '布',
             '富', '牌', '头', '四', '多', '妆', '吉', '苑', '沙', '恒', '隆', '春', '干', '饼', '氏', '里', '二', '管', '诚', '制',
             '售', '嘉', '长', '轩', '杂', '副', '清', '计', '黄', '讯', '太', '鸭', '号', '街', '交', '与', '叉', '附', '近', '层',
             '旁', '对', '巷', '栋', '环', '省', '桥', '湖', '段', '乡', '厦', '府', '铺', '内', '侧', '元', '购', '前', '幢', '滨',
             '处', '向', '座', '下', '県', '凤', '港', '开', '关', '景', '泉', '塘', '放', '昌', '线', '湾', '政', '步', '宁', '解',
             '白', '田', '町', '溪', '十', '八', '古', '双', '胜', '本', '单', '同', '九', '迎', '第', '台', '玉', '锦', '底', '后',
             '七', '斜', '期', '武', '岭', '松', '角', '纪', '朝', '峰', '六', '振', '珠', '局', '岗', '洲', '横', '边', '济', '井',
             '办', '汉', '代', '临', '弄', '团', '外', '塔', '杨', '铁', '浦', '字', '年', '岛', '陵', '原', '梅', '进', '荣', '友',
             '虹', '央', '桂', '沿', '事', '津', '凯', '莲', '丁', '秀', '柳', '集', '紫', '旗', '张', '谷', '的', '是', '不', '了',
             '很', '还', '个', '也', '这', '我', '就', '在', '以', '可', '到', '错', '没', '去', '过', '感', '次', '要', '比', '觉',
             '看', '得', '说', '常', '真', '们', '但', '最', '喜', '哈', '么', '别', '位', '能', '较', '境', '非', '为', '欢', '然',
             '他', '挺', '着', '价', '那', '意', '种', '想', '出', '员', '两', '推', '做', '排', '实', '分', '间', '甜', '度', '起',
             '满', '给', '热', '完', '格', '荐', '喝', '等', '其', '再', '几', '只', '现', '朋', '候', '样', '直', '而', '买', '于',
             '般', '豆', '量', '选', '奶', '打', '每', '评', '少', '算', '又', '因', '情', '找', '些', '份', '置', '适', '什', '蛋',
             '师', '气', '你', '姐', '棒', '试', '总', '定', '啊', '足', '级', '整', '带', '虾', '如', '态', '且', '尝', '主', '话',
             '强', '当', '更', '板', '知', '己', '无', '酸', '让', '入', '啦', '式', '笑', '赞', '片', '酱', '差', '像', '提', '队',
             '走', '嫩', '才', '刚', '午', '接', '重', '串', '回', '晚', '微', '周', '值', '费', '性', '桌', '拍', '跟', '块', '调',
             '糕']

base_uniname = old_font['cmap'].tables[0].ttFont.getGlyphOrder()[2:]
# 使用百度的FontEditor找到本地字体文件name和数字之间的对应关系, 保存到字典中
base_dict = dict(zip(base_uniname, base_font))
# print(base_dict)
# name_list1 = font1.getGlyphNames()[1:-1]
# print(name_list1)
base_glyph = []
for unicode in base_dict.keys():
    # 取字形坐标的字节流
    contour = bytes(str(old_font['glyf'][unicode].coordinates), encoding='utf-8')
    # 取字形坐标的md5值
    contour_md5 = hashlib.md5(contour).hexdigest()
    # 保存到新的基准参照字典
    # new_base_glyph['hex']=contour_md5
    base_dict1 = {'name': unicode,'value': base_dict[unicode],'hex':contour_md5}
    base_glyph.append(base_dict1)
print(base_glyph)
#爬取数据的URL
url = 'http://www.porters.vip/confusion/movie.html'
resp = requests.get(url)
sel = Selector(resp.text)
# 提取页面加载的所有css文件路径
css_path = sel.css('link[rel=stylesheet]::attr(href)').extract()
woffs = []
for i in css_path:
    # 拼接正确的css文件路径
    css_url = parse.urljoin(url, i)
    # 向css文件发起请求
    css_resp = requests.get(css_url)
    # 匹配css文件中的woff文件路径
    woff_path = re.findall("src:url\('..(.*.woff)'\) format\('woff'\);", css_resp.text)
    if woff_path:
        # 如故路径存在则添加到woffs列表中
        woffs += woff_path
#弹出一个字体的url
woff_url = 'http://www.porters.vip/confusion' + woffs.pop()
woff = requests.get(woff_url)
filename = 'target.woff'
with open(filename, 'wb') as f:
    # 将文件保存到本地
    f.write(woff.content)
# 使用TTFont库打开刚才下载的woff文件
new_font = TTFont(filename)

# 取新字体文件中unicode
new_unicodes = new_font.getGlyphOrder()
new_glyph = []
# 遍历基准字典
for new_unicode in new_unicodes:
    # 取新字体文件字的 md5值
    contour = bytes(str(new_font['glyf'][new_unicode].coordinates),encoding='utf-8')
    new_contour_md5 = hashlib.md5(contour).hexdigest()
    for base in base_glyph:
        # 遍历新字体文件的unicode
        # 与基准字形中的md5值进行对比，如果相同则取出该字形描述的文字
        if base['hex'] ==new_contour_md5:
           base_glyph[0]['name']= new_unicode
        new_glyph.append(base_glyph)
# 打印映射结果
print(new_glyph)
html = ''
for value in base_glyph:
    old = '&#x' + value['name'] + ';'
    new = value['value']
    html = html.replace(old,new)
    xp_html = etree.HTML(html)
    shop_list = xp_html.xpath('//*[@id="shop-all-list"]/ul/li')
    for shop in shop_list:
        shop_name = shop.xpath('./div[2]/div[1]/a/h4/text()')[0]
        comment_list = shop.xpath('./div[2]/span//text()')
        comment = shop.xpath('./div[2]/div[2]/a[1]//text()')
        per_capita_price = shop.xpath('./div[2]/div[2]/a[2]//text()')
        tag = shop.xpath('./div[2]/div[3]/a[1]/span//text()')
        area = shop.xpath('./div[2]/div[3]/a[2]/span//text()')
        address = shop.xpath('./div[2]/div[3]/span//text()')
        recommend = ''.join(shop.xpath('./div[2]/div[4]//text()')).replace('\n', '').replace('\n', '').strip()
print(html)
