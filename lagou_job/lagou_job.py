import requests
import json
import os
import pandas as pd
import math
from fake_useragent import UserAgent
import time

import sys
# city = sys.argv[1]
# position = sys.argv[2]

def get_json_data(city,position,page):
    url ='https://www.lagou.com/jobs/positionAjax.json?px=default&city={0}&needAddtionalResult=false'.format(city)
    datas = {
        'first': 'true',
        'pn': page,
        'kd': position,
    }

    cookie = 'write your cookie here'
    headers = {'cookie': cookie,
               'origin': "https://www.lagou.com",
               'x-anit-forge-code': "0",
               'accept-encoding': "gzip, deflate, br",
               'accept-language': "zh-CN,zh;q=0.8,",
               'user-agent': UserAgent().random,
               'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
               'accept': "application/json, text/javascript, */*; q=0.01",
               'referer': "https://www.lagou.com/jobs/list_Pyhon?labelWords=&fromSearch=true&suginput=",
               'x-requested-with': "XMLHttpRequest",
               'connection': "keep-alive",
               'x-anit-forge-token': "None"}
    #
    # headers = {
    #     'Host': 'www.lagou.com',
    #     'Referer': 'https://www.lagou.com/',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    #     'Cookie':'JSESSIONID=ABAAABAAAFCAAEGB66B21895547EE55CA0FC5785C29C800; _ga=GA1.2.1744928834.1544610941; _gid=GA1.2.1570864122.1544610941; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544610942; user_trace_token=20181212183541-ac8f0f2a-fdf9-11e8-9076-525400f775ce; LGUID=20181212183541-ac8f1238-fdf9-11e8-9076-525400f775ce; X_HTTP_TOKEN=d816c5284c6a234f5b7b2eab0638602a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167a26887636aa-01485791dabfb8-163c6656-2073600-167a2688764a89%22%2C%22%24device_id%22%3A%22167a26887636aa-01485791dabfb8-163c6656-2073600-167a2688764a89%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ab_test_random_num=0; _putrc=490C4FE94B966151123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B79509; hasDeliver=0; TG-TRACK-CODE=index_navigation; index_location_city=%E5%8C%97%E4%BA%AC; _gat=1; LGSID=20181213192312-7a02e77e-fec9-11e8-8cef-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=9eb8593b295cd0c99740e54d1e59982df4c5198bb3e465d8e0719b70a0dfeca3; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544700197; LGRID=20181213192316-7caffdc3-fec9-11e8-8cef-5254005c3644; SEARCH_ID=251c694967ec49838a2afdbebe0fb7f7'
    # }
    response = requests.post(url,headers=headers,data=datas)
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
