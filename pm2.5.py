# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import sys

import pandas
from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Please input the year')
        exit(0)

    year = int(sys.argv[1])

    # Chrome Driver 设置
    chromeOptions = webdriver.ChromeOptions()
    # 关闭 “Chrome 正在受到自动化软件控制” 的显示
    chromeOptions._arguments = ['disable-infobars']
    # 启动 Chrome 浏览器
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    wait = WebDriverWait(browser, 10)

    result = []

    for month in range(1, 13):

        print('Page %s-%s' % (year, month))

        browser.get('https://www.aqistudy.cn/historydata/daydata.php?city=%E5%8C%97%E4%BA%AC&month={0}-{1}'.format(year, '%02d' % month))

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#piecontainer .highcharts-container svg')))
        
        table_pq = pq(browser.find_element_by_css_selector('.container table').get_attribute('innerHTML'))

        for tr in table_pq.find('tr').items():

            if tr == table_pq.find('tr').eq(0):
                continue

            result.append({
                'date': tr.find('td:nth-child(1)').text(),
                'AQI': tr.find('td:nth-child(2)').text(),
                'rank': tr.find('td:nth-child(3)').text(),
                'PM2.5': tr.find('td:nth-child(4)').text(),
                'PM10': tr.find('td:nth-child(5)').text(),
                'SO2': tr.find('td:nth-child(6)').text(),
                'CO': tr.find('td:nth-child(7)').text(),
                'NO2': tr.find('td:nth-child(8)').text(),
                'O3_8h': tr.find('td:nth-child(9)').text()
            })

    df = pandas.DataFrame(result)
    df.to_excel('%s.xls' % year, columns=['date', 'AQI', 'rank', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3_8h'])
    print(result)
    browser.close()




