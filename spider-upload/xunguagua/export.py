import json
import os
import time

import requests

import app_env

_URL_ = "http://yun.xunguagua.com/member/?app=member&controller=list&type={type}&page={page}"


def init_session():
    sess = requests.Session()
    sess.headers.update({
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "yun.xunguagua.com",
        "Referer": "http://yun.xunguagua.com/member/?app=member&controller=list",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest"
    })
    return sess


def get_last_time(type_key):
    last_time = None
    if os.path.exists(app_env.get_app_root() + "/xunguagua/last-time-" + type_key + ".txt"):
        last_time = open(app_env.get_app_root() + "/xunguagua/last-time-" + type_key + ".txt", encoding="UTF-8").read().strip()
        last_time = round(time.mktime(time.strptime(last_time, '%Y/%m/%d %H:%M:%S')))
    return last_time


def run():
    cookie = open(app_env.get_app_root() + "/xunguagua/cookie.txt", encoding="UTF-8").read().strip()
    sess = init_session()
    results = []
    for type_key in ["1", "2"]:
        last_pub_time = run_pages(cookie, results, sess, type_key)
        if last_pub_time is not None:
            with open(app_env.get_app_root() + "/xunguagua/last-time-" + type_key + ".txt", mode="w") as f:
                f.write(last_pub_time)

    if results:
        write_results(results)
    print("found results " + str(len(results)) + " for type " + type_key)
    return len(results)


def run_pages(cookie, results, sess, type_key):
    last_time = get_last_time(type_key)
    page = 1
    last_pub_time = None
    while page < 9999:
        resp = sess.get(_URL_.format(type=type_key, page=page), headers={
            "Cookie": cookie
        })
        if resp.status_code != 200:
            print("got status code: " + str(resp.status_code))
            break

        sent_list_resp = json.loads(resp.text)
        sent_list = sent_list_resp["list"]
        if not sent_list or len(results) >= int(sent_list_resp["total"]):
            break

        for sent_log in sent_list:
            title = sent_log["title"].replace(",", "，").strip()
            url = sent_log["url"].strip()
            pub_time = int(sent_log["time"])
            if last_time is not None and pub_time <= last_time:
                page = 10000
                break

            pub_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(pub_time))
            results.append((title, pub_time, url))
            if last_pub_time is None:
                last_pub_time = pub_time

        print("page " + str(page) + " finished, current size: " + str(len(results)))
        time.sleep(2)
        page += 1
    return last_pub_time


def write_results(results):
    sent_list_f = open(app_env.get_app_root() + "/xunguagua/sent-list.csv", encoding="GBK", mode="w")
    urls_f = open(app_env.get_app_root() + "/xunguagua/urls.txt", encoding="GBK", mode="w")
    for result in results:
        sent_list_f.write(",".join(result) + "\n")
        urls_f.write(result[2] + "\n")
    sent_list_f.flush()
    sent_list_f.close()
    urls_f.flush()
    urls_f.close()
