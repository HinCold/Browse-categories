#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/4/29 14:21
# @name: downloadDataSet
# @author：XPR
import re
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException


# 判断是否有弹出框
def alert_is_present(driver):
    try:
        alert = driver.switch_to.alert
        return alert
    except:
        return False


def parseUrl(driver):
    # url = parseQue.get()
    print("***parse url to get link:***")

    if driver.current_url == 'https://www.hao123.com':
        print("I want not to parse baidu or hao123")
        return []
    parse_page = driver.page_source
    # parse_data = requests.get(url, allow_redirects=False)
    # parse_soup = BeautifulSoup(parse_data.text, 'lxml')
    href_match = re.compile('<a.+?href="(http.+?)"')
    parse_target = href_match.findall(parse_page)
    print("*******find link:{}********".format(len(parse_target)))

    return parse_target


def updateUrls(targets, webset, urls):
    print("========update urls queue=========")
    # time1 = time.time()
    for ta in targets:
        if ta not in webset:
            urls.put(ta)
            # print("put url:", ta)
            # parseQue.put(ta)
            webset.add(ta)
            # f.write(ta + '\n')
            # time.sleep(1)

    # time2 = time.time()
    # print("update time:", time2-time1)
    print("=========queue long:", urls.qsize())
    return webset


def initDriver():
    brose = webdriver.Chrome()
    # 设置浏览器窗口的位置和大小
    time.sleep(3)
    brose.set_page_load_timeout(30)
    # brose.set_window_position(0, 0)
    # brose.set_window_size(1920, 1080)
    brose.maximize_window()
    return brose


def search_by_Category(category):
    driver = initDriver()
    driver.get('https://www.baidu.com/')
    time.sleep(1)
    search_input = driver.find_element_by_id('kw')
    try:
        # 输入内容：selenium
        search_input.send_keys(category)
        print('搜索关键词：', category)
    except Exception as e:
        print('fail')
    search_but = driver.find_element_by_id('su')
    try:
        # 点击搜索按钮
        search_but.click()
        print('成功搜索')
    except Exception as e:
        print('fail搜索')
    time.sleep(5)
    target = parseUrl(driver)
    num_parse = len(target)
    print("找到链接条数：", num_parse)
    time.sleep(1)
    driver.close()
    return target


def tryAndGet(driver, url, pro_id, urls):
    try:
        driver.get(url)
        driver.implicitly_wait(30)
    except TimeoutException:
        print('---timeout work in', pro_id)
        driver.quit()
        driver = initDriver()
        url = urls.get()
        driver.implicitly_wait(30)
        driver = tryAndGet(driver, url, pro_id, urls)
    return driver
