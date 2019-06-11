# coding=utf
"""
author=Hui_T
"""
import time
import requests
from selenium import webdriver
# 驱动器
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

import csv
if __name__ == '__main__':
    # url = "https://www.basketball-reference.com/leagues/NBA_2019.html"
    # headers = {"user - agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.121Safari / 537.36"}
    # res = requests.get(url,headers=headers)
    # ----------------------------------
    # 查找元素 等待十秒 隐式等待(所有的都要等待)
    # driver = webdriver.Firefox(executable_path="F:/火狐/geckodriver")
    # driver.implicitly_wait(10)
    # wait = WebDriverWait(driver, 20) # 显示等待 10秒元素加载
    # driver.implicitly_wait(10)

    # driver.get(url)
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    # time.sleep(2)
    # time.sleep(10)
    # res = driver.page_source
    # ----------------------------------
    with open("Nba.html",'r',encoding="utf8") as f:
        doc = f.read()
    tree = etree.HTML(doc)
    # tree = etree.HTML(res)
    div_list = tree.xpath('// *[ @ id = "content"] / div[contains(@class,"table_wrapper")]')
    div_list = div_list[1:]
    table_lst= []
    for ele in div_list:
        table = ele.xpath('.//div[3]/div/table')[0]
        table_lst.append(table)
    # print(table_lst,len(table_lst))
    # table_last_lst = table_lst[-2:]
    # table_lst = table_lst[:-2]
    num = 1

    for ele in table_lst:
        csvFile = open("表" + str(num) + ".csv", 'w',newline='')
        # 头
        title_th = ele.xpath(".//thead/tr")
        title_th = title_th[-1]
        t_l= []
        for title in title_th:
            text = title.xpath('text()')[0]
            t_l.append(text)

        writer = csv.writer(csvFile)
        writer.writerow(t_l)
        csvFile.close()
        num += 1

    num = 1
    for ele in table_lst:

        b_t = []
        # 身体的第一个
        tbody_title = ele.xpath(".//tbody/tr/th")
        print(tbody_title)
        for i in tbody_title:
            tbody_title = i.xpath("text()")
            b_t.append(tbody_title)

        # 身体的第二个a标签
        tbody_td_a = ele.xpath(".//tbody/tr/td/a")
        for j in range(len(b_t)):
            tbody_td_a_text = tbody_td_a[j].xpath("text()")
            b_t[j].extend(tbody_td_a_text)

        # 前2个特殊处理完后的数据
        tbody_tr__lst = ele.xpath(".//tbody/tr")
        for i in range(len(tbody_tr__lst)):
            li = []
            td_list = tbody_tr__lst[i].xpath(".//td")
            td_list = td_list[1:]
            for td in td_list:
                td_text = td.xpath("text()")[0]
                li.append(td_text)
            b_t[i].extend(li)
        print(b_t)

        csvFile = open("表"+str(num)+".csv",'a',newline='')
        writer= csv.writer(csvFile)
        writer.writerows(b_t)
        num += 1
        csvFile.close()

    num = 1
    for ele in table_lst:
        csvFile = open("表"+str(num)+".csv",'a',newline='')
        writer = csv.writer(csvFile)
        tfoot = ele.xpath(".//tfoot")
        tfoot_td_lst = []
        if tfoot:
            tfoot = tfoot[0]
            td_list = tfoot.xpath(".//tr/td")
            for td in td_list:
                text = td.xpath(".//text()")
                if text:
                    text = text[0]
                else:
                    text = " "
                print(text)
                tfoot_td_lst.append(text)
        writer.writerow(tfoot_td_lst)
        csvFile.close()
        num += 1

    # print(res.text)
    # with open("Nba.html","w",encoding="utf8") as f :
    #     f.write(res)