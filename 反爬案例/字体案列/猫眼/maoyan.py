# -*- coding: utf-8 -*-
"""
@File    : maoyan.py
@Time    : 2020/8/26 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
'''
猫眼电影:不同文件中的同一个字，它们的字形坐标不一定相同，且`Unicode`也可能不同.
1.接收新字体文件的字形
2.生成一个数组，长度为150，并往里面从索引0开始填充字形坐标
3.获取数据集的数据和标签
	3.1.数据集的这里为50个字形信息（即5套字体文件
	3.2.生成一个数组，长宽分别为(50,150),并从索引0开始填充数据集的字形坐标（因为数据集长度为50
	3.3.这个数组即为数据集字形坐标的数据组。用于和2.做比较
4.算出新字体字形坐标与 3.3数据集字形坐标中各个字形的距离（算5次，即K=5
5.算出来的值放到字典里，最后取出现次数最高的一个。
'''
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph
import re

def analysis_font():
    basefont = TTFont('maoyan2.woff')
    with open('2.html','r',encoding='utf-8') as f:
        html = f.read()
    # basefont.saveXML('maoyan2.xml')
    # 1.找到code和name之间的关系
    # 返回code和name之间的关系
    # baseCodeCamp = basefont.getBestCmap()
    #foot['glyf'],可以返回字体的所用形状,字典对象，可以通过name来获取对应的形状
    baseGlyphMap = basefont['glyf']
    baseNumberGlyphMap = {
        0: baseGlyphMap['uniEF2B'],
        1: baseGlyphMap['uniE507'],
        2: baseGlyphMap['uniF52D'],
        3: baseGlyphMap['uniE3EA'],
        4: baseGlyphMap['uniE29B'],
        5: baseGlyphMap['uniEB6C'],
        6: baseGlyphMap['uniF40B'],
        7: baseGlyphMap['uniE81C'],
        8: baseGlyphMap['uniED81'],
        9: baseGlyphMap['uniE9EF']
    }
    newfont = TTFont('1.woff')
    newNameCamp = newfont.getBestCmap()
    # print(newNameCamp)
    # foot['glyf'],可以返回字体的所用形状,字典对象，可以通过name来获取对应的形状
    newGlyphMap = newfont['glyf']
    for code,name in newNameCamp.items():
        if name == 'x':
            continue
        # 10进制转16进制用hex
        # print(hex(code),name)
        #2.name和glyph(形状)之间的关系
        currentGlyph = newGlyphMap[name]
        number_diff = {}
        for number,baseGlyph in baseNumberGlyphMap.items():
            diff = 0
            #猫眼电影每次刷新，形状是不一样的
            #glyph这个属性记录的是字体的坐标
            #求坐标的最小差值就可以了--k近邻思想
            # diff = 0
            # for coor1,coor2 in zip(glyph.coordinates,currentGlyph.coordinates):
            #     diff += abs(coor1[0]-coor2[0])+abs(coor1[1]-coor2[1])
            for coor1 in currentGlyph.coordinates:
                coor_diff = []
                for coor2 in baseGlyph.coordinates:
                    coor_diff.append(abs(coor1[0]-coor2[0])+abs(coor1[1]-coor2[1]))
                    # print(coor_diff)
                diff += min(coor_diff)
                # print(diff)
            number_diff[number] = diff
            print(number_diff)
        number = min(number_diff,key=number_diff.get)

        # print(hex(code),number)
            # if glyph==currentGlyph:
        code = str(hex(code)).replace('0','&#',1)+';'
        html = re.sub(code,str(number),html)
        #         break
        # with open('更新的文件2.html','w',encoding='utf-8') as f:
        #     f.write(html)

if __name__ == '__main__':
    analysis_font()