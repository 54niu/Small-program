import threading
import queue
import requests
from lxml import etree
import time
import random
import json

concurrent = 3
conparse = 3

# 解析线程类
class Parse(threading.Thread):
    def __init__(self,number,data_list,req_thread,f):
        super(Parse ,self).__init__()
        self.number = number
        self.data_list = data_list
        self.req_thread = req_thread
        self.f = f
        self.is_parse = True # 判断是否从数据队列里提取数据

    def run(self):
        print('启动%d号解析线程' % self.number)
        while True:
            # 如何判断解析线程的结束条件
            for t in self.req_thread:
                if t.is_alive():
                    break
            else:
                if self.data_list.qsize() == 0:
                    self.is_parse = False

            if self.is_parse: # 解析
                try:
                    data = self.data_list.get(timeout=3)
                except Exception as e:
                    data = None
                if data is not None:
                    self.parse(data)
            else:
                break
        print('退出%d号解析线程' % self.number)
    # 页面解析函数
    def parse(self,data):
        html = etree.HTML(data)
        # 获取所有段子div
        duanzi_div = html.xpath('//div[@id="content-left"]/div')

        for duanzi in duanzi_div:
            # 获取昵称
            nick = duanzi.xpath('./div//h2/text()')[0]
            nick = nick.replace('\n', '')
            # 获取年龄
            age = duanzi.xpath('.//div[@class="author clearfix"]/div/text()')
            if len(age) > 0:
                age = age[0]
            else:
                age = 0
            # 获取性别
            gender = duanzi.xpath('.//div[@class="author clearfix"]/div/@class')
            if len(gender) > 0:
                if 'women' in gender[0]:
                    gender = '女'
                else:
                    gender = '男'
            else:
                gender = '中'

            # 获取段子内容
            content = duanzi.xpath('.//div[@class="content"]/span[1]/text()')[0].strip()

            # 获取好笑数
            good_num = duanzi.xpath('./div//span[@class="stats-vote"]/i/text()')[0]

            # 获取评论
            common_num = duanzi.xpath('./div//span[@class="stats-comments"]//i/text()')[0]

            item = {
                'nick': nick,
                'age': age,
                'gender': gender,
                'content': content,
                'good_num': good_num,
                'common_num': common_num,
            }

            self.f.write(json.dumps(item,ensure_ascii=False) + '\n')


# 采集线程类
class Crawl(threading.Thread):
    def __init__(self,number,req_list,data_list):
        super(Crawl,self).__init__()
        self.number = number
        self.req_list = req_list
        self.data_list = data_list
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }

    def run(self):
        print('启动采集线程%d号' % self.number)
        while self.req_list.qsize() > 0:
            url = self.req_list.get()
            print('%d号线程采集：%s' % (self.number,url))
            time.sleep(random.randint(1,3))
            response = requests.get(url,headers=self.headers)
            if response.status_code == 200:
                self.data_list.put(response.text) # 向数据队列里追加

def main():
    # 生成请求队列
    req_list = queue.Queue()
    # 生成数据队列
    data_list = queue.Queue()

    # 创建文件对象
    f = open('duanzi.json','w',encoding='utf-8')

    for i in range(1,13 + 1):
        base_url = 'https://www.qiushibaike.com/8hr/page/%d/' % i
        req_list.put(base_url)

    # 生成N个采集线程
    req_thread = []
    for i in range(concurrent):
        t = Crawl(i + 1,req_list,data_list) # 创造线程
        t.start()
        req_thread.append(t)

    # 生成N个解析线程
    parse_thread = []
    for i in range(conparse):
        t = Parse(i + 1,data_list,req_thread,f) # 创造解析线程
        t.start()
        parse_thread.append(t)

    for t in req_thread:
        t.join()
    for t in parse_thread:
        t.join()

    # 关闭文件对象
    f.close()

if __name__ == '__main__':
    main()