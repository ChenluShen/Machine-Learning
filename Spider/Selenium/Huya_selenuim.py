#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver  # 模拟浏览器行为
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup as bs  # 解析网页
from pandas import DataFrame as df
import pandas as pd
import re  # 正则表达式
import sys  # 命令行中传入参数
from itertools import groupby

# 设置自己的文件路径
project_loc = "C:/Users/clshe/Documents/Python Scripts"

os.chdir(project_loc)
if not os.path.exists('./output'):
    os.makedirs('./output')

url = "http://www.huya.com/g/lol/"

chromedriver = "C:/Users/clshe/AppData/Local/Google/Chrome/Application/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

live_results = {'room_name': [],
                 'broadcaster_name': [],
                 'online_users': []}
live_results = df(live_results)
# 打开谷歌浏览器
browser = webdriver.Chrome()
# 输入网址
browser.get(url)
time.sleep(3)  # 延迟时间，避免过快

livelists = browser.find_elements_by_class_name('game-live-item')

global remain_page_num
remain_page_num=10

def liveDataFunc(livelists):
    for i in range(len(livelists)):
        live = livelists[i]

        # 解析网页
        live_parse = bs(live.get_attribute("outerHTML"), "lxml")
        # 得到各项信息
        live_name=live_parse.find(class_='title new-clickstat').get_text()
        live_broadcaster=live_parse.find(class_='nick').get_text()
        live_online=live_parse.find(class_='js-num').get_text()
        if not live_online.isdigit():
            v = [''.join(g) for _, g in groupby(live_online, key=lambda x: x.isdigit() * 'd' or x.isalpha() * 'a')] #拆分数字和单位“万”
            live_online = int(v[0]) * 10000 + int(v[2]) * 1000  

        temp_live_results = {'room_name': [live_name],
                              'broadcaster_name': [live_broadcaster],
                              'online_users': [live_online]}
        temp_live_results = df(temp_live_results)
        global live_results
        live_results = pd.concat([live_results, temp_live_results]) #与之前的数字连接

    return;

page_num=1
liveDataFunc(livelists)

# 得到剩余爬取页数
while(1):
    # 模拟“跳转下一页”行为
    browser.find_element_by_class_name('laypage_next').click()
    time.sleep(3)
    livelists = browser.find_elements_by_class_name('game-live-item')
    page_num += 1
    liveDataFunc(livelists)
    if browser.page_source.find('laypage_next') == -1:   #最后一页没有下一页按钮
        break

# 关闭浏览器
browser.close()
# 导出结果文件
live_results.to_csv(project_loc + '/output/' + 'huya_lol.results.csv', index=False)
print('总共'+str(page_num)+'页')

# 以QQ空间为例其他操作
# # 浏览器窗口最大化
# driver.maximize_window()
# # 浏览器地址定向为qq登陆页面
# driver.get("http://i.qq.com")
# # 很多时候网页由多个<frame>或<iframe>组成，webdriver默认定位的是最外层的frame，
# # 所以这里需要选中一下frame，否则找不到下面需要的网页元素
# driver.switch_to.frame("login_frame")
# # 自动点击账号登陆方式
# driver.find_element_by_id("switcher_plogin").click()
# # 账号输入框输入已知qq账号
# driver.find_element_by_id("u").send_keys(self.user)
# # 密码框输入已知密码
# driver.find_element_by_id("p").send_keys(self.pw)
# # 自动点击登陆按钮
# driver.find_element_by_id("login_button").click()
