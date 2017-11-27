from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json

#解析页面
total_num = 0

def parsePage(html,f):
    global total_num
    html = BeautifulSoup(html,'lxml')
    room_li = html.select('ul#live-new-show-content-box li,ul#live-list-contentbox li')
    for room in room_li:
        roomname = room.select('h3')[0].text.strip()
        typename = room.select('span[class*="tag ellipsis"]')[0].text.strip()
        nick = room.select('span[class*="dy-name ellipsis fl"]')[0].text.strip()
        online = room.select('span[class*="dy-num fr"]')
        if online:
            online = online[0].text.strip()
            if '万' in online:
                online = online.replace('万','')
                online = int(float(online) * 10000)
        else:
            online = 0

        total_num += int(online)
        item = {
            'roomname' : roomname,
            'typename' : typename,
            'nick' : nick,
            'online' : online,
        }
        f.write(json.dumps(item,ensure_ascii=False) + '\n')

def getPage():
    browser = webdriver.PhantomJS()
    browser.get('https://www.douyu.com/directory/all')
    time.sleep(1)
    html = browser.page_source
    parsePage(html,f)

    #循环点击下一页
    while True:
        browser.find_element_by_class_name('shark-pager-next').click()
        html = browser.page_source
        parsePage(html,f)
        # 如果没有下一页则跳出循环
        if 'shark-pager-disable-next' in browser.page_source:
            break

if __name__ == '__main__':
    f = open('douyu.json', 'w',encoding='utf-8')
    getPage()
    f.close()
    print('观看直播总人数:%d' % total_num)