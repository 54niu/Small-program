from urllib import request,parse
import time
import random
import hashlib
import json

def getSign(salt,key):
    md5 = hashlib.md5()
    sign = "fanyideskweb" + key + str(salt) + "rY0D^0'nM0}g5Mm1z%1G4"
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()  # 返回加密以后的md5字符串
    return sign


def fanyi(key):
    base_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
    headers = {
        "Host": "fanyi.youdao.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "http://fanyi.youdao.com",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "http://fanyi.youdao.com/",
        # "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    data = {
        "i": key,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION",
        "typoResult": "false",
    }
    salt = int(time.time() * 1000) + random.randint(0,10)
    sign = getSign(salt,key)
    data['salt'] = salt
    data['sign'] = sign
    data = parse.urlencode(data)
    # data 构造完毕，指定data长度
    headers["Content-Length"] = str(len(data))

    req = request.Request(base_url,data=bytes(data,encoding='utf-8'),headers=headers)
    response = request.urlopen(req)
    data = response.read().decode('utf-8')
    data = json.loads(data)
    print(json.dumps(data,ensure_ascii=False,indent=4))

if __name__ == '__main__':
    while True:
        key = input('输入要翻译的单词：')
        if key == 'q':
            break
        fanyi(key)