import requests
import json
from pyquery import PyQuery as pq
import time
import hmac
from hashlib import sha1
from copyheaders import headers_raw_to_dict
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_timestamp():
    return int(time.time())*1000

def get_sig(key, client_id, time_stamp):
    h = hmac.new(key, digestmod=sha1)
    h.update(b'password')
    h.update(client_id)
    h.update(b'com.zhihu.web')
    h.update(time_stamp)
    return h.hexdigest()

def checkcapthca(s, headers, cn=True):
    '检查是否需要验证码,无论需不需要，必须要发一个请求'
    if cn:
        url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
    else:
        url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    headers.pop('X-Xsrftoken')
    z = s.get(url, headers=headers)
    print(z.json())
    return z.json()



url = "https://www.zhihu.com/#signin"

headers = {
    "Host":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
}

s = requests.session()
s.headers = headers

post_headers_raw = b'''
accept:application/json, text/plain, */*
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9,zh-TW;q=0.8
authorization:oauth c3cef7c66a1843f8b3a9e6a1e3160e20
Connection:keep-alive
DNT:1
Host:www.zhihu.com
Origin:https://www.zhihu.com
Referer:https://www.zhihu.com/signup?next=%2F
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
'''

def getheaders():
    req = s.get(url)
    # print(req)
    doc = pq(req.text)

    d = doc('div').filter('#data').attr("data-state")
    data = json.loads(d)

    xsrf = data['token']['xsrf']
    xUDID = data['token']['xUDID']
    #print("xsrf:",xsrf, "xUDID:", xUDID)

    headers = headers_raw_to_dict(post_headers_raw)
    headers['X-UDID'] = xUDID
    headers['X-Xsrftoken'] = xsrf

    return headers

def getdata(username, passowrd, captcha=''):
    client_id = b'c3cef7c66a1843f8b3a9e6a1e3160e20'
    timestamp = get_timestamp()
    signature = get_sig(b"d1b964811afb40118a12068ff74a12f4",
                        client_id, bytes(str(timestamp),'utf8'))
    data = {
        'client_id': client_id, 'grant_type': 'password',
        'timestamp': str(timestamp), 'source': 'com.zhihu.web',
        'signature': signature, 'username': username,
        'password': password, 'captcha': captcha,
        'lang': 'en', 'ref_source': 'homepage', 'utm_source': ''
    }

    return data

def login(username, password):
    url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    headers = getheaders()
    checkcapthca(s, headers)
    data = getdata(username, password)
    encoder = MultipartEncoder(data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
    headers['Content-Type'] = encoder.content_type
    z2 = s.post(url, headers=headers, data=encoder.to_string())
    print(z2.json())

if __name__ == '__main__':
    username = ''
    password = ''
    login(username, password)
    
