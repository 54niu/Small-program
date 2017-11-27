from urllib import request
import json
import mydownloader
import jsonpath
import requests

# 引入代理ip
proxies = mydownloader.getProxy('proxy1')

# 获取json
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,en;q=0.8,zh;q=0.6,ja;q=0.4",
    "cache-control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "s=f6126m94cu; device_id=9e362c1dc7a3cca1aa474d5029d69a8a; webp=0; xq_a_token=469ea9edce5537d5d8297aaffcd3474cc8d12273; xq_a_token.sig=8D0Nrw6wLkoY9wJS5_6N_eORSOY; xq_r_token=819ae94ba56378cc0665670983c2afafc34c275b; xq_r_token.sig=6N6ZkaHvfEfPz1FgHKEsoQ_rhaA; u=121509788780309; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1508598672,1509695401,1509768339,1509788782; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1509788802; __utma=1.67144076.1509718906.1509718906.1509788785.2; __utmb=1.2.10.1509788785; __utmc=1; __utmz=1.1509718906.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "Host": "xueqiu.com",
    "Referer": "https://xueqiu.com/hq",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def xueqiu(page_num):
    base_url = 'https://xueqiu.com/stock/cata/stocklist.json?page=%d' % page_num + '&size=30&order=desc&orderby=percent&type=11%2C12&_=1509790735407'

    # 使用requests和jsonpath
    response = requests.get(base_url, headers=headers)
    data = response.text
    print(data)

    # 使用代理
    # response = request.Request(base_url, headers=headers)
    # opener = mydownloader.getOpener(proxies)
    # html = mydownloader.downloader(opener, response, proxies).decode('utf-8')
    # data = json.loads(html)
    #
    # stockdata = data['stocks']
    # print(stockdata)
    # for i in range(len(stockdata)):
    #     gupiao = stockdata[i]
    #     gup = {
    #             '股票代码': gupiao['symbol'],
    #             '股票名称': gupiao['name'],
    #             '当前价': gupiao['current'],
    #             '涨跌额': gupiao['change'],
    #             '涨跌幅': gupiao['percent'],
    #             '市值': gupiao['marketcapital'],
    #             '市盈利 ': gupiao['pettm'],
    #             '成交量': gupiao['volume'],
    #             '成交额': gupiao['amount']
    #            }
    #
    #     with open('xueqiu/'+'niu', 'a', encoding='utf-8') as f:
    #         f.write(str(gup) + '\n')


if __name__ == '__main__':
    # page_num = input('请输入想要获得的页数:')
    # for page_num in range(1, int(page_num)+1):
    #     xueqiu(page_num)

    xueqiu(1)
