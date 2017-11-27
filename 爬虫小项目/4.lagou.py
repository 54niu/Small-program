from Mydb import Mydb
from selenium import webdriver
import time
from lxml import etree

def parsePage(html,mydb):
    html = etree.HTML(html)
    position_li = html.xpath('//ul[@class="item_con_list"]/li')
    for position in position_li:
        name = position.xpath('.//h3/text()')[0]
        money = position.xpath('.//span[@class="money"]/text()')[0]
        start_money = money.split('-')[0].lower().replace('k','000').strip().replace('\n','')
        end_money = money.split('-')[1].lower().replace('k','000').strip().replace('\n','')

        print(money)
        print(start_money)
        print(end_money)

        require = position.xpath('.//div[@class="li_b_l"]/text()')[2].strip().replace('\n','').replace('/','')
        company = position.xpath('.//div[@class="company_name"]/a/text()')[0].strip().replace('\n','')
        industry = position.xpath('.//div[@class="industry"]/text()')[0].strip().replace('/','')

        fuli = position.xpath('.//div[@class="li_b_r"]/text()')[0]
        # 存入mysql
        sql = 'insert into lagou(pname,smoney,emoney,company,industry,requirement,fuli) ' \
              'values("%s",%s,%s,"%s","%s","%s","%s")' % (name, start_money, end_money,company,industry,require,fuli)
        mydb.exe(sql)

def getPage():
    # 加headers
    dc = {
        'phantomjs.page.customHeaders.User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    }

    browser = webdriver.PhantomJS(desired_capabilities=dc)
    browser.get('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=')
    time.sleep(1)
    # browser.save_screenshot('lagou.png')
    parsePage(browser.page_source,mydb)

    while True:
        browser.find_element_by_class_name('pager_next ').click()
        time.sleep(0.5)
        parsePage(browser.page_source,mydb)
        if 'pager_next_disabled' in browser.page_source:
            break
    browser.quit()

if __name__ == '__main__':
    mydb = Mydb('127.0.0.1','root','123456','temp')
    getPage()