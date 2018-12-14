import requests
import json
import os
import pandas as pd
import math
from fake_useragent import UserAgent
import time

import random
import sys


# city = sys.argv[1]
# position = sys.argv[2]

# 运行本代码前，先去获得自己的登录cookie，以及x-anti-forge-code和x-anti-forge-token的值

# 获取x-anti-forge-code和x-anti-forge-token的值

# r1 = requests.get('https://passport.lagou.com/login/login.html',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',},)
# X_Anti_Forge_Token = re.findall("X_Anti_Forge_Token = '(.*?)'", r1.text, re.S)[0]
# X_Anti_Forge_Code = re.findall("X_Anti_Forge_Code = '(.*?)'", r1.text, re.S)[0]
# print(X_Anti_Forge_Token,X_Anti_Forge_Code)



def get_json_data(city,position,page):
    url ='https://www.lagou.com/jobs/positionAjax.json?px=default&city={0}&needAddtionalResult=false'.format(city)
    datas = {
        'first': 'true',
        'pn': page,
        'kd': position,
    }

    cookie = 'please write your cookie here'
    headers = {'cookie': cookie,
               'origin': "https://www.lagou.com",
               'x-anit-forge-code': "96133506",
               'accept-encoding': "gzip, deflate, br",
               'accept-language': "zh-CN,zh;q=0.8,",
               'user-agent': UserAgent().random,
               'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
               'accept': "application/json, text/javascript, */*; q=0.01",
               'referer': "https://www.lagou.com/jobs/list_Pyhon?labelWords=&fromSearch=true&suginput=",
               'x-requested-with': "XMLHttpRequest",
               'connection': "keep-alive",
               'x-anit-forge-token': "e3336034-825a-4a43-8bd3-98443eaa9378"}

    response = requests.post(url,headers=headers,data=datas)
    print(response.json())
    return response.json()

def totalPage(city,position):
    json = get_json_data(city,position,'1')
    #print(response.text)
    #print('done')
    #print(json)
    total_info = json['content']['positionResult']['totalCount']
    print('total job:{0}'.format(int(total_info)))
    total_page = math.ceil(int(total_info)/15)
    return total_page

def parse_json(json):
    # 状态是成功的再处理

    tmp_jobs = []
    job_info = json.get('content').get('positionResult').get('result')
    for item in job_info:
        results = {}
        companyShortName = item.get('companyShortName')
        companyFullName = item.get('companyFullName')
        companySize = item.get('companySize')
        positionName = item.get('positionName')
        workYear = item.get('workYear')
        salary = item.get('salary')
        industryField = item.get('industryField')
        financeStage = item.get('financeStage')
        createTime = item.get('createTime')
        education = item.get('education')
        district = item.get('district')
        positionId = item.get('positionId')
        jobNature = item.get('jobNature')
        positionAdvantage = item.get('positionAdvantage')
        positionUrl = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'

        results = {
            '公司名称':companyFullName,
            '职位名称':positionName,
            '工作年限':workYear,
            '薪资范围':salary,
            '行业':industryField,
            '融资情况':financeStage,
            '公司简称':companyShortName,
            '公司规模':companySize,
            '发布时间':createTime,
            '学历要求':education,
            '地区':district,
            '工作性质':jobNature,
            '职位优势':positionAdvantage,
            '职位ID':positionId,
            '职位链接':positionUrl
        }
        tmp_jobs.append(results)
    return tmp_jobs


def save_to_csv(position,city,job_list):
    file_dir = "{0}/{1}".format(os.getcwd(), position)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    path = os.path.join(file_dir,city+".csv")
    dataframe = pd.DataFrame(job_list)
    # 设置保存的列顺序，否则pandas会重新排序
    #columns = ['公司名称', '职位名称', '工作年限', '薪资范围', '行业', '融资情况','公司简称', '公司规模', '发布时间', '学历要求', '地区', '工作性质', '职位优势', '职位ID', '职位链接']
    dataframe.to_csv(path,mode='a',encoding="utf_8_sig")

def main(city,position):

    total_page = totalPage(city,position)
    print('total_page:{}'.format(total_page))
    time.sleep(10)
    job_list = []
    for page in range(1,total_page+1):
        page_json = get_json_data(city,position,page)
        if page_json['success'] == True:
            page_result = parse_json(page_json)
            job_list.extend(page_result)
            print('page {} has done'.format(page))
            time.sleep(5)
        else:
            print("数据出错")
            break
    save_to_csv(position, city, job_list)

if __name__ == '__main__':
    city = '杭州'
    position = 'Python'
    main(city,position)
