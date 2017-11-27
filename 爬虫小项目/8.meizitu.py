from urllib import request
import re
import os
import mydownloader


# 图片下载函数
def getpic(base_url):
    proxies = mydownloader.getProxy('proxy1')
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,en;q=0.8,zh;q=0.6,ja;q=0.4",
        "Cache-Control": "max-age=0",
        "Cookie": "Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1509629725,1509694548,1509799309,1509864108; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1509864482",
        "Host": "www.mzitu.com",
        "If-Modified-Since": "Fri, 03 Nov 2017 19:21:39 GMT",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://www.mzitu.com/104854",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    }

    # base_url = 'http://www.mzitu.com/104854'
    base_url = base_url
    req = request.Request(base_url, headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')

    # 获取最大页
    page_pattern = re.compile(r'<div class="pagenavi">.*?</div>', re.S)
    page_list = page_pattern.findall(html)
    for page in page_list:
        page_big = re.compile(r'<span>(.*?)</span>')
        pagebig = page_big.findall(page)
        pagebig = int(pagebig[-2])

    # 获取标题
    title_pattern = re.compile(r'<h2 class="main-title">(.*?)</h2>')
    title = title_pattern.findall(html)[0]

    # 创建文件夹
    try:
        os.makedirs('meizi/' + title)
    except:
        pass

    # 获取图片连接
    pic_pattern = re.compile(r'<img src="(.*?)" alt="%s" />' % title, re.S)
    pic_url = pic_pattern.findall(html)[0]
    pic_name = pic_url.split('/')[-1]  # 获取图片名称

    # 取出本专题图片的前缀
    year = pic_url.split('/')[3]
    month = pic_url.split('/')[4]

    meizi_url = 'http://i.meizitu.net/'+year + '/' + month + '/' + pic_name[:3]

    for i in range(1, pagebig+1):
        if i < 10:
            i = '0' + str(i)
        houzhui = pic_url.split('/')[-1].split('.')[-1]  # 获取图片后缀
        picurl = meizi_url + str(i) + '.' + houzhui
        picname = picurl.split('/')[-1]  # 获取图片名称

        # 下载图片
        headers = {
            "Host": "i.meizitu.net",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": 'http://www.mzitu.com/95318',
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        req = request.Request(picurl, headers=headers)
        opener = mydownloader.getOpener(proxies)
        content = mydownloader.downloader(opener, req, proxies)
        with open('meizi/%s/' % title + picname, 'wb') as f:
            f.write(content)


# 获取某个分类下的妹子图
def getmei():
    base_url = 'http://www.mzitu.com/taiwan/'
    reponse = request.urlopen(base_url, timeout=10)
    html = reponse.read().decode('utf-8')

    # 获取本主题下有多少页
    page_pattern = re.compile(r'<span class="meta-nav screen-reader-text"></span>(.*?)'
                              r'<span class="meta-nav screen-reader-text"></span>', re.S)
    page_list = int(page_pattern.findall(html)[-1])
    for page in range(1, page_list+1):
        base_url = 'http://www.mzitu.com/taiwan/page/%d/' %page
        reponse = request.urlopen(base_url, timeout=10)
        html = reponse.read().decode('utf-8')

        # 获取每个妹子的url地址
        mei_pattern = re.compile(r'<ul id="pins">(.*?)</ul>', re.S)
        mei_list = mei_pattern.findall(html)
        for a_list in mei_list:
            a_pattern = re.compile(r'<a href="(.*?)" target="_blank">')
            a_url = a_pattern.findall(a_list)
            # 列表去重
            a_url = set(a_url)
            a_url = list(a_url)

        for i in a_url:
            getpic(i)


# 获取所有妹子图
def meiall():
    base_url = 'http://www.mzitu.com/all/'
    reponse = request.urlopen(base_url, timeout=10)
    html = reponse.read().decode('utf-8')

    # 获取每个妹子的url地址
    mei_pattern = re.compile(r'<a href="(.*?)" target="_blank">', re.S)
    mei_list = mei_pattern.findall(html)[1:]
    # 列表去重
    mei_list = set(mei_list)
    mei_list = list(mei_list)

    for i in mei_list:
        print(i)
        getpic(i)




meiall()

