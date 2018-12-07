import requests
from pyquery import PyQuery as pq
from selenium import webdriver
import time
import sys
import os
import pandas as pd

keyword = sys.argv[1]

def get_cookies():
    driver = webdriver.Chrome()
    driver.get("http://weixin.sogou.com/")

    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    time.sleep(10)

    cookies = driver.get_cookies()
    cookie = {}
    for items in cookies:
        cookie[items.get('name')] = items.get('value')
    return cookie

def parse_url(url,cookie):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    response = requests.get(url,headers = header,cookies=cookie)
    if response.status_code == 200:
        response = response.text
        return response

def total_page():
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + keyword + '&page=100'
    response = parse_url(url,cookie)
    doc = pq(response)
    print(doc)
    totalPage = doc.find('#pagebar_container.p-fy span').text()
    return totalPage

def parse_page(page):
    url = 'https://weixin.sogou.com/weixin?type=2&query=' + keyword + '&page=' + str(page)
    response = parse_url(url,cookie)
    doc = pq(response)
    items = doc.find('.news-list li').items()
    #print(doc.find('.news-list li'))
    for item in items:
        source = item.find('.s-p .account').text()
        href = item.find('.txt-box h3 a').attr('href')
        #print(href)
        response = requests.get(href).text
        doc1 = pq(response)
        title = doc1.find('.rich_media_title').text()
        yield  {
            'title':title,
            'source':source,
            'url':href
        }
        #print(href)

def save_to_csv(info):
    file_dir = "{0}".format(os.getcwd())
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    path = os.path.join(file_dir,keyword+".csv")
    dataframe = pd.DataFrame(info)
    # 设置保存的列顺序，否则pandas会重新排序
    columns = ['title','source','url']
    dataframe.to_csv(path,mode='a',encoding="utf_8_sig",columns=columns)
    return path


def main(keyword):
    #cookie = get_cookies()
    #print(cookie)
    totalPage = total_page()
    print('total page is {0}'.format(totalPage))
    totalPage=5
    content = []
    for page in range(1,int(totalPage)+1):
        items = parse_page(page)
        for item in items:
            content.append(item)
        print('Page {0} has Done'.format(page))
    path=save_to_csv(content)
    print(path)

if __name__ == '__main__':
    cookie = {'please input your cookie ,you can use the get_cookie() to get it'}
    main(keyword)
