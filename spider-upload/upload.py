import requests

sess = requests.Session()
sess.headers.update({
    "Host": "spider.geilizhizhu.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "http://spider.geilizhizhu.com",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,mr;q=0.6"
})

sess.get("http://spider.geilizhizhu.com")
login_resp = sess.post("http://spider.geilizhizhu.com/spider/login/newdologin.html", headers={
    "Referer": "http://spider.geilizhizhu.com/",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}, data={
    "username": "Round",
    "password": "geili123"
})
print("login got response: " + login_resp.text)

upload_resp = sess.post("http://spider.geilizhizhu.com/spider/index/upload.html", headers={
    "Referer": "http://spider.geilizhizhu.com/spider/",
}, data={
    "PHP_SESSION_UPLOAD_PROGRESS": "dingcheng",
    "act": "addTo"
}, files={
    "file": ("urls.txt", open("./xunguagua/urls.txt", "rb"), "text/plain")
})
print("upload urls got response: " + upload_resp.text)
