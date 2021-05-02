#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/4/30 7:53
# @name: multiPro
# @author：XPR
from selenium import webdriver
from multiprocessing import Process, Queue, Manager
import uuid
from dataSet.GrabUtils import *
num_set = 2000
category = '房产'
path = 'E:\\NNcode\\final\\data\\1\\'
webUrlSet = set()
urls = Queue()


def getImage(urlsq, webset, pro_id):
    pro_set = webset
    driver = initDriver()
    file = 'urlList_{}.txt'.format(pro_id)
    time.sleep(3)
    tt = 0
    seq = 1
    base_path = path + str(pro_id) + '_'
    need_parse = True
    while tt < 20:
        if urlsq.empty():
            time.sleep(60)
            tt += 1
            print("waitTime:", tt)
            print("队列长度：", urlsq.qsize())
        else:
            tt = 0
            url = urlsq.get()
            print("---work in ", pro_id)
            # print("---working number", seq)
            print("-----image get url------")
            driver = tryAndGet(driver, url, pro_id, urlsq)
            driver.implicitly_wait(3)
            if alert_is_present(driver):
                driver.switch_to.alert.accept()
            filepath = base_path + str(uuid.uuid1()) + '.png'
            res = driver.save_screenshot(filepath)
            driver.implicitly_wait(1)
            print("screen shoot success:", seq)
            seq += 1
            if need_parse and pro_id == 1 and urlsq.qsize() < num_set:
                parse_target = parseUrl(driver)
                pro_set = updateUrls(parse_target, pro_set, urlsq)
            else:
                need_parse = False
                if pro_id == 2:
                    print("************* Working in 2*************")
                else:
                    print("************* Parse Enough*************  long:", urlsq.qsize())
            f = open(file, 'a+')
            f.write(driver.current_url + '\n')
            f.close()
            print("-----------写入文件url  working by-", pro_id)
            driver.execute_script("window.scrollBy(0,3000)")
            driver.implicitly_wait(3)
            time.sleep(1)
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            if check_height < 3000:
                continue
            else:
                filepath = base_path + str(uuid.uuid1()) + '.png'
                res = driver.save_screenshot(filepath)
                driver.implicitly_wait(1)
                print("screen shoot success:", seq)
                seq += 1
    driver.close()
    print('done')


def loadSet(file):
    with open(file, 'r') as f:
        s = f.readline()
        while len(s) > 0:
            url = s[:-1]
            # print(url)
            webUrlSet.add(url)
            s = f.readline()
        f.close()


def initSet():
    loadSet("urlset.txt")
    loadSet("urlList_1.txt")
    loadSet("urlList_2.txt")
    print("已加载url条数：", len(webUrlSet))


def runDoubleProcess():
    p1 = Process(target=getImage, args=(urls, webUrlSet, 1,))
    p2 = Process(target=getImage, args=(urls, webUrlSet, 2,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':

    initSet()
    target = search_by_Category(category)
    webUrlSet = updateUrls(target, webUrlSet, urls)
    runDoubleProcess()



