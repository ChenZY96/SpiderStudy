import requests
from pyquery import PyQuery as pq
import random
import os
import sys
#url = 'https://mp.weixin.qq.com/s/QAwrisNuu1dThFbs__wF_Q'
#url = 'https://mp.weixin.qq.com/s/WBBGOT_GGliFAdiLMQSEGg'
url = sys.argv[1]

def download_pic(title,url):
    print(url)
    pic_name = url.split('/')[4]
    pic_type = url.split('=')[1]
    response = requests.get(url,headers=random.choice(headers))
    try:
        if response.status_code == 200:
            file_dir = "{0}/{1}".format(os.getcwd(), title)
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            path = os.path.join(file_dir,pic_name+'.'+pic_type)
            if not os.path.exists(path):
                with open(path,'wb') as f:
                    f.write(response.content)
    except:
        pass

if __name__ == '__main__':
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]

    response = requests.get(url,headers=random.choice(headers))
    if response.status_code != 200:
        print('ERROR')
        exit(0)
    doc = pq(response.text)

    # 文章标题
    title = doc.find('.rich_media_title').text()
    # 微信公众号
    author = doc.find('#meta_content .rich_media_meta_text').text()
    source = doc.find('#js_name').text()
    source_info = doc.find('.profile_meta_value').text()

    print(title,author,source)
    print(source_info)

    # 正文内容
    content = doc.find('.rich_media_content')

    pic = []
    # 所有图片链接
    pics_src = content.find('img').items()
    for each in pics_src:
        if '=' in each.attr('data-src'):
            pic.append(each.attr('data-src'))
    print(pic)

    #下载所有图片
    for each in pic:
        download_pic(title,each)

    # 改写图片链接
    for item in content.find('img').items():
        pic_url = item.attr('data-src')
        if '=' in pic_url:
            pic_name = pic_url.split('/')[4]
            pic_type = pic_url.split('=')[1]
            image = pic_name + '.' + pic_type
            item.add_class('src')
            item.attr('src',image)

    content = content.html()
    # html存放路径
    file_dir = "{0}/{1}".format(os.getcwd(), title)
    path = os.path.join(file_dir,'index.html')

    index = '<h2>'+title+'</h2><br>'
    index += '<span>'+author+''+source+'</span><br>'
    index += '<span>'+source_info+'</span><br>'
    index += content
    with open(path, 'wb') as f:
        f.write(index.encode('utf-8'))
    print('Done')
    print('see the html in:{0}'.format(path))


