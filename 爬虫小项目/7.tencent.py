from bs4 import BeautifulSoup
import requests
import json

headers = {
    "Host": "hr.tencent.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding" : "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 解析详情页
def parse_detail(item):
    print(item['href'])
    response = requests.get(item['href'],headers=headers)

    html = BeautifulSoup(response.text,'lxml')
    info_ul = html.select('ul.squareli')

    # 获取工作职责
    li_list = info_ul[0].select('li')
    # 列表生成式
    li_list = [li.text for li in li_list]
    rb = ''.join(li_list)

    # 获取工作要求
    li_list = info_ul[1].select('li')
    # 列表生成式
    li_list = [li.text for li in li_list]
    require = ''.join(li_list)

    item['rb'] = rb
    item['require'] = require

    with open('position.json','a', encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False) + '\n')


def getPage():
    # 获取最大页数
    base_url = 'http://hr.tencent.com/position.php?keywords=python&lid=2156&start=%d'
    response = requests.get(base_url % 0, headers=headers)
    html = BeautifulSoup(response.text,'lxml')
    total = html.select('div.pagenav a')[-2].text

    for i in range(1, int(total)):

        base_url = 'http://hr.tencent.com/position.php?keywords=python&lid=2156&start=%d'
        print('列表页%d' % ((i -1) * 10,))
        response = requests.get(base_url % (i - 1) * 10,headers=headers)
        html = BeautifulSoup(response.text,'lxml')
        # position_list = html.find_all('tr',attrs={'class':['even','odd']})
        position_list = html.select('tr.even ,tr.odd')
        for position in position_list:
            info = position.select('td')

            # 构建数据项
            position_name = info[0].text
            position_type = info[1].text
            number = info[2].text
            location = info[3].text
            date_pub = info[4].text

            # 获取职位链接
            href = info[0].a['href']

            item = {
                'position_name' : position_name,
                'position_type' : position_type,
                'number' : number,
                'location' : location,
                'date_time' : date_pub,
                'href' : 'http://hr.tencent.com/' + href,
            }
            parse_detail(item)
            #print(position_name,position_type,number,location,date_time)

if __name__ == '__main__':
    getPage()
