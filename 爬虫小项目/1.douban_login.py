from urllib import request,parse
from http import cookiejar # 管理cookie的模块 存储cookie的

cookie = cookiejar.CookieJar() # 做个cookie对象
cookie_handler = request.HTTPCookieProcessor(cookie) # cookie管理器
https_handler = request.HTTPSHandler() # https请求 管理器
http_handler = request.HTTPSHandler()# http 请求 管理器

opener = request.build_opener(cookie_handler,https_handler,http_handler) # 请求管理器

login_url = 'https://accounts.douban.com/login'
# 获取登录页面
def getLoginPage():
    login_url = 'https://accounts.douban.com/login'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }
    req = request.Request(login_url,headers=headers)
    response = opener.open(req)
    login_page = response.read().decode('utf-8')
    print(login_page)
    return login_page
# 构建post请求，提交账户密码 验证码
def login(login_page):
    data = {
        'form_email': '1752570559@qq.com',
        'form_password': '1234qwer',
        'source': 'index_nav',
    }
    if 'captcha_image' in login_page:
        code = input('输入验证码：')
        captcha_id = input('输入catpcha-id：')

        data['captcha-solution'] = code
        data['captcha-id'] = captcha_id

    data = parse.urlencode(data)
    headers = {
        "Host": "accounts.douban.com",
        "Connection": "keep-alive",
        "Content-Length": str(len(data)),
        "Cache-Control": "max-age=0",
        "Origin": "https://accounts.douban.com",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://accounts.douban.com/login?alias=1752570559%40qq.com&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1013",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    req = request.Request(login_url,headers=headers,data=bytes(data,encoding='utf-8'))
    response = opener.open(req)
    return response.read().decode('utf-8')

if __name__ == '__main__':
    login_page = getLoginPage()
    html = login(login_page)
    print(html)