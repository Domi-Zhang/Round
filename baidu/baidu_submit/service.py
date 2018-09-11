import json
import os
import queue
import random
import sys
import threading
import time

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from baidu_submit.url_logger import UrlLogger
import app_env
import requests

_COOKIE_FILE = app_env.get_app_root() + "/baidu_submit/cookie.txt"
_COOKIE_EXPIRE_COUNT = 50
_THREAD_SIZE = 2
_PROXY_CONF = json.load(open(app_env.get_app_root() + "/baidu_submit/proxy.json", encoding="UTF-8"))


class BaiduSubmit:
    def __init__(self):
        cookies = [line.strip() for line in open(_COOKIE_FILE, encoding="UTF-8")] * _COOKIE_EXPIRE_COUNT
        random.shuffle(cookies)
        self._cookies = cookies
        self._change_proxy()
        self._change_cookie()
        self._url_buffer = queue.Queue()
        self.start_buffer_consumer()

    def _change_proxy(self):
        while True:
            try:
                proxy_resp = requests.get("http://api3.xiguadaili.com/ip/?tid={}&num=1".format(_PROXY_CONF["no"]))
                print("got next proxy: " + proxy_resp.text)
                ip, port = proxy_resp.text.split(":")
                proxy = {"http": ip + ":" + port, "https": ip + ":" + port}
                try:
                    resp = requests.get(url="http://fankui.help.sogou.com/wap/fb.php", timeout=10, proxies=proxy)
                    resp.encoding = "UTF-8"
                    if resp.text.find("用户反馈") > 0:
                        self._proxy = proxy
                        print("change proxy.")
                        break
                except Exception as e:
                    pass
                print("proxy not available, try next")
            except Exception as e:
                print("try get proxy failed: {}".format(repr(e)))
            time.sleep(5)

    def _change_cookie(self):
        if not self._cookies:
            print("cookies has exhausted.")
            return
        self._cookie = self._cookies.pop()
        print("change cookie.")

    def append_buffer(self, url):
        self._url_buffer.put(url)
        return self._url_buffer.qsize()

    def start_buffer_consumer(self):
        threading.Thread(target=self._consume_buffer)

    def _consume_buffer(self):
        while True:
            self.submit(self._url_buffer.get())

    def submit(self, url):
        retry_times = 0
        while True:
            try:
                resp, url = self._do_submit(url)
                if resp.status_code != 200:
                    print("[retry {}]post error with code: {}".format(retry_times, resp.status_code))
                    retry_times += 1
                    self._change_cookie()
                else:
                    resp_entity = json.loads(resp.text)
                    if "status" not in resp_entity or resp_entity["status"] != 0:
                        print("[retry {}]post error with response: {}".format(retry_times, resp.text))
                        retry_times += 1
                        self._change_cookie()
                    else:
                        UrlLogger.get_instance("success").info(url)
                        print("url " + url + " done.")
                        return True
            except Exception as e:
                print("[retry {}]post error with exception: {}".format(retry_times, repr(e)))
                retry_times += 1
                self._change_proxy()

            if retry_times >= 3:
                UrlLogger.get_instance("failed").info(url)
                print("post error due to cookie and proxy both has been changed for limit times.")
                return False

    def _do_submit(self, url):
        url = url.strip()
        headers = {"Connection": "keep-alive",
                   "Origin": "https://ziyuan.baidu.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "Accept": "application/json, text/javascript, */*; q=0.01",
                   "X-Requested-With": "XMLHttpRequest",
                   "X-Request-By": "baidu.ajax",
                   "Referer": "https://ziyuan.baidu.com/linksubmit/url",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,mr;q=0.6",
                   "Cookie": self._cookie,
                   }
        resp = requests.post(url="https://ziyuan.baidu.com/linksubmit/urlsubmit",
                             data={"url": url},
                             headers=headers,
                             proxies=self._proxy,
                             timeout=10)
        return resp, url


if __name__ == "__main__":
    runner = BaiduSubmit()
    runner.submit("http://www.baidu.com")
