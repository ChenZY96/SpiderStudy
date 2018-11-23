
import requests
import random
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import re
import json
import os
import hashlib
from multiprocessing.pool import Pool
import sys

keyword = sys.argv[1]
page_start = sys.argv[2]
page_end = sys.argv[3]

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

def get_page(keyword,offset):
    #https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E5%9B%BD%E5%BA%86&autoload=true&count=20&cur_tab=1&from=search_ta
    params = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'aotoload':'true',
        'count':'20',
        'cur_tab':'3',
        'from':'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(params)
    try:
        response = requests.get(url,headers=random.choice(headers))
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)

def get_url(Ajax_json):
    if Ajax_json.get('data'):
        items = Ajax_json.get('data')
        for item in items:
            group_id = item.get('group_id')
            page_url = 'https://www.toutiao.com/a'+str(group_id)
            yield page_url

def parse_page(page_url):
    page_dict = {} #存放标题和图片链接
    response = requests.get(page_url,headers = random.choice(headers))
    doc = pq(response.text)
    #获取文章标题
    title = doc('title').text()
    pattern = re.compile('gallery: JSON.parse\("(.*?)"\)',re.S)
    results = re.findall(pattern,response.text)
    if results:
        results = results[0].replace(r'\"','"').replace(r'\\', '\\')
        data = json.loads(results, )
        url_list = data.get("sub_images")
        #print(url_list)

        page_dict['title'] = title
        page_dict['images'] = [each.get('url')for each in url_list]
        return page_dict

def download_images(keyword,title,image_url):
    response = requests.get(image_url,headers=random.choice(headers))
    if response.status_code == 200:
        file_dir = "{0}/{1}/{2}/{3}".format(os.getcwd(), "images",keyword,title)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        path = os.path.join(file_dir,hashlib.md5(response.content).hexdigest()+".jpg")

        if not os.path.exists(path):
            with open(path,'wb') as f:
                f.write(response.content)
            #print('Download image:', image_url)
        #else:
            #print('Already existed')


def main(offset):
    Ajax_json = get_page(keyword,offset)
    urls = get_url(Ajax_json)
    for page_url in urls:
        page_dict = parse_page(page_url)
        if not page_dict:
            continue
        image_url = page_dict['images']
        title = page_dict['title']
        print(title)
        for each in image_url:
            download_images(keyword,title,each)



if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[x*20 for x in range(int(page_start)-1,int(page_end))])
    pool.close()
    pool.join()


