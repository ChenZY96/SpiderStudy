from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import sys

qq_number = sys.argv[1]

url = 'https://user.qzone.qq.com/'+qq_number+'/311'
browser = webdriver.Chrome()
browser.get(url)
#print('done')
wait = WebDriverWait(browser,200)
#next_num = 0

username = 'username'
pwd = 'password'

time.sleep(5)

# browser.switch_to.frame('login_frame')
# button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#switcher_plogin.link')))
# button.click()
# user_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#uinArea>div>input#u.inputstyle')))
# pwd_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pwdArea>div>input#p.inputstyle.password')))
# submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginform>div>a>input#login_button.btn')))
# user_input.send_keys(username)
# pwd_input.send_keys(pwd)
# submit_button.click()
# browser.switch_to.default_content()


browser.switch_to.frame('app_canvas_frame')
doc = pq(browser.page_source)


if doc.find('div#pager.mod_pagenav.tbor.js_error_display').attr('style') == 'display: none;':
    total_page=1
else:
    total_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pager>#_pager_content_0>p>#pager_last_0>span'))).text  # 最后一页
    total_page = int(total_page)
print('Total page:',total_page)
browser.switch_to.default_content()

for next_num in range(0,total_page+1):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

    browser.switch_to.frame('app_canvas_frame')
    doc = pq(browser.page_source)
    items = doc('#msgList li.feed').items()
    for item in items:
        shuoshuo_dic = {}
        shuoshuo_dic['time'] = item.find('div.box.bgr3>div.ft>div.info>.c_tx3>.c_tx.c_tx3.goDetail').attr('title'),
        shuoshuo_dic['source'] = item.find('div.box.bgr3>div.ft>div.info>.c_tx3>.custom-tail').attr('title')
        shuoshuo_dic['content'] = item.find('.content').text()
        with open('qzone.txt','a+') as f:
            f.write(str(shuoshuo_dic)+'\n')
    if next_num > 0:
        print('Page {0} has done'.format(next_num))

    if total_page != 1:
        CSS_sel = '#pager>#_pager_content_'+str(next_num)+'>p>span>input#pager_go_'+str(next_num)+'.textinput'
        next_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,CSS_sel)))
        next_input.send_keys(int(next_num+1))
        next_input.send_keys(Keys.ENTER)
                                        
    #next_page.click()
    browser.switch_to.default_content()
print('Done')





