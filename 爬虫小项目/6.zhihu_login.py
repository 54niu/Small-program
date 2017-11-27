import requests
from bs4 import BeautifulSoup
import time
import json

#构建个回话
sess = requests.session()

headers = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.9",
    "Cache-Control" : "max-age=0",
    "Connection" : "keep-alive",
    "Host" : "www.zhihu.com",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
}
response = sess.get('https://www.zhihu.com/#signin',headers=headers)
html = response.text
html = BeautifulSoup(html,'lxml')

# 获取xsrf 验证 token
xsrf = html.select('input[name="_xsrf"]')[0]['value']

# 下载一个验证码图片
response = sess.get('https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=en' % (time.time() * 1000),headers=headers)
with open('zhihu.gif','wb') as f:
    f.write(response.content)

code = input('输入验证码：')

data = {
    'captcha' : code,
    'phone_num' : '18600672750',
    'password' : '1234qwer',
    'captcha_type' : 'en',
    '_xsrf' : xsrf,
}

response = sess.post('https://www.zhihu.com/login/phone_num',data=data,headers=headers)
print(json.loads(response.text)['msg'])