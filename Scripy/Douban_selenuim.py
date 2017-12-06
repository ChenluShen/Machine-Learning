#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup as bs
from pandas import DataFrame as df
import pandas as pd
import re
import sys

# 设置自己的文件路径
project_loc = "*****************"

os.chdir(project_loc)
if not os.path.exists('./output'):
    os.makedirs('./output')

url = "https://movie.douban.com/"
# keyword = '鹿晗'

keyword = sys.argv[1]

movie_results = {'name':[],
                 'year':[],
                 'rate':[],
                 'rate_people':[]}
movie_results = df(movie_results)
# 打开谷歌浏览器
browser = webdriver.Chrome()
# 输入网址
browser.get(url)

time.sleep(5)

browser.find_element_by_name('search_text').send_keys(keyword)

browser.find_element_by_name('search_text').send_keys(Keys.ENTER)

movielists = browser.find_elements_by_class_name('sc-bZQynM')

def MovieDataFunc(movielists):
    for i in range(len(movielists))
        movie = movielists[i]
        
        # 解析网页
        movie_parse = bs(movie.get_attribute("outerHTML"),"lxml")
        
        movie_name_year = movie_parse.find(class_='title-text').get_text()
        movie_name_year = re.split('‎\s',movie_name_year)
        movie_name = movie_name_year[0]
        movie_year = re.sub('\(|\)',"",movie_name_year[1])
        
        try:
            movie_rate = movie_parse.find(class_='rating_nums').get_text()
        except:
            movie_rate = 'NA'
            movie_rate_people = 'NA'
        else:
            movie_rate = movie_rate
            movie_rate_people = movie_parse.find(class_='pl').get_text()
            movie_rate_people = re.search(r'\d+',movie_rate_people).group()
        
        temp_movie_results = {'name':[movie_name],
                              'year':[movie_year],
                              'rate':[movie_rate],
                              'rate_people':[movie_rate_people]}
        temp_movie_results = df(temp_movie_results)
        
        global movie_results
        movie_results = pd.concat([movie_results,temp_movie_results])
        
    return;

MovieDataFunc(movielists)

remain_page_num = len(browser.find_elements_by_css_selector('a.num'))-1

for i in range(remain_page_num):
    
    browser.find_element_by_css_selector('a.next').click()
    
    time.sleep(5)
    movielists = browser.find_elements_by_class_name('sc-bZQynM')
    MovieDataFunc(movielists)

# 关闭浏览器    
browser.close()
# 导出结果文件
movie_results.to_csv(project_loc+'output/'+keyword+'_movie.results.csv',index=False)


