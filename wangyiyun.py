# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import math

url = 'http://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0'
# 用PhantomJS接口创建一个selemium的webDriver
# driver = webdriver.PhantomJS(executable_path="D:\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)


# 准备好存储歌单的csv文件
csv_file = open('/Users/mc/playlist.csv', 'w', newline='', encoding='gb18030')
writer = csv.writer(csv_file)
writer.writerow(('标题', '播放数', '链接'))
# 分析每一页直到下一页为空
while url != 'javascript:void(0)':
    driver.get(url)
    driver.switch_to.frame("contentFrame")
    data = driver.find_element_by_id("m-pl-container").find_elements_by_tag_name("li")
    for i in range(len(data)):
        nb = data[i].find_element_by_class_name("nb").text
        if "万" in nb and int(nb.split("万")[0]) > 500:
            msk = data[i].find_element_by_css_selector("a.msk")
            writer.writerow([msk.get_attribute("title"), nb, msk.get_attribute("href")])

    url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute('href')
csv_file.close()
