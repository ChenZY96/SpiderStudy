# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
import random
import re
import base64
from fontTools.ttLib import TTFont
import io
import csv
import os
import time
import pandas as pd
import codecs
from selenium import webdriver

def getrealValue(newmap,fakevalue):
    # 用FontCreatro打开微软雅黑的ttf，获取文字对应的编码
    font58 = {
        '闰': '0x958f',
        '閏': '0x958f',
        '鸺': '0x9e3a',
        '鵂': '0x9e3a',
        '麣': '0x9ea3',
        '饩': '0x993c',
        '餼': '0x993c',
        '鑶': '0x9476',
        '龤': '0x9fa4',
        '齤': '0x9f64',
        '龥': '0x9fa5',
        '龒': '0x9f92',
        '驋': '0x9a4b'
    }
    fake_array = [each for each in fakevalue]

    length = len(fake_array)
    for i in range(0,length):
        if fake_array[i] in font58.keys():
            fake_array[i] = str(newmap[font58[fake_array[i]]])
        realValue = ''.join(fake_array)
    return realValue

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]

url  = 'https://bj.58.com/haidian/pinpaigongyu/pn/{0}/?minprice=2000_3000'
page = 0

file_dir = "{0}".format(os.getcwd())
path = os.path.join(file_dir,"BJ_haidian_2000_3000.csv")
columns = ['name','location','price','url']
house_data = []
while True:
    page += 1
    resp = requests.get(url.format(page),headers=random.choice(headers))

    if resp:
        base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*?)\'\) format\(\'truetype\'\)}',resp.text)
        #print(base64_str)
        bin_data = base64.b64decode(base64_str[0])
        fonts = TTFont(io.BytesIO(bin_data))
        bestcmap = fonts.getBestCmap()
        newmap = {}
        for key in bestcmap.keys():
            #print(key)
            #print(re.findall(r'(\d+)', bestcmap[key]))
            value = int(re.findall(r'(\d+)', bestcmap[key])[0]) - 1
            key = hex(key)
            newmap[key] = value

        print('==========', newmap)
        resp_ = resp.text
    doc = pq(resp_)
    house_list = doc.find('.list li')

    if not house_list:
        break
    #print(doc.find('.page a').eq(-2).text())
    for each in house_list.items():
        house_url = each.find('a').eq(0).attr('href')

        house_name = each.find('.des.strongbox h2').text()
        house_name= getrealValue(newmap,str(house_name))

        house_room = each.find('.des.strongbox .room').text()
        house_room = getrealValue(newmap,str(house_room))

        house_price = each.find('.money .strongbox').text()
        house_price = getrealValue(newmap,str(house_price))

        #house_location = re.findall('\s+(.*?)\s+',house_name)
        house = re.findall('】(.*?)\s+(.*?)\s+', house_name)

        if not house:
            house_location == 'Unknow'
        else:
            if "公寓" in house[0][0] or "青年社区" in house[0][0]:
                house_location = house[0][0]
            else:
                house_location = house[0][1]

        house_info = {
            'name':house_name,
            'location':house_location,
            'room':house_room,
            'price':house_price,
            'url':house_url
        }
        house_data.append(house_info)
    print('page {0} has done'.format(page))
    if page != 1 and doc.find('.page a').eq(-2).text() != '下一页':
        print('All done')
        break
    time.sleep(3)

dataframe = pd.DataFrame(house_data)
dataframe.to_csv(path, mode='a', encoding="utf_8_sig", columns=columns)





