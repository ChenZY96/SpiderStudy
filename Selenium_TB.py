#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from pyquery import PyQuery as pq
import os
import pandas as pd
import sys

keyword = sys.argv[1]
start_page = sys.argv[2]
end_page = sys.argv[3]

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
wait = WebDriverWait(browser,10)


def total_page(keyword):
    inputbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm>div.search-button>button.btn-search.tb-bg')))
    inputbox.clear()
    inputbox.send_keys(keyword)
    button.click()

    totalPages = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager>div.m-page.g-clearfix>div.wraper>div.inner.clearfix>div.total'))).text
    totalPages = re.search('(\d+)',totalPages).group(1)
    return totalPages

def next_page(currentPage):
    inputbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div> input.input.J_Input')))
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div>span.btn.J_Submit')))
    inputbox.clear()
    inputbox.send_keys(int(currentPage))
    button.click()

def product_info(keyword):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    #获取页面源代码
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    product_list = []
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text().replace('\n',''),
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text().replace('\n',' '),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        product_list.append(product)
    #print(product_list)
    path = save_to_csv(keyword,product_list)
    #save_to_mongo(product)
    return path
def save_to_csv(keyword,product_list):
    file_dir = "{0}/{1}".format(os.getcwd(), "product")
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    path = os.path.join(file_dir,keyword+".csv")
    dataframe = pd.DataFrame(product_list)
    # 设置保存的列顺序，否则pandas会重新排序
    columns = ['image','price','deal','title','shop','location']
    dataframe.to_csv(path,mode='a',encoding="utf_8_sig",columns=columns)
    return path


def main(keyword,start_page,end_page):
    totalPages = total_page(keyword)
    if 1<=int(start_page) and int(end_page)<=int(totalPages) and int(start_page)<int(end_page):
        for page in range(int(start_page),int(end_page)+1):
            next_page(page)
            path = product_info(keyword)
        print('Done')
        print('please see the csv in :{0}'.format(path))

    else:
        print('ERROR,out of range!')

if __name__ == '__main__':
    main(keyword, start_page, end_page)
    browser.close()


