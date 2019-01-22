import json
import time

import requests

import app_env

_URL_ = "http://yun.xunguagua.com/member/?app=member&controller=list&type={type}&page={page}"


def init_session():
    cookie = open(app_env.get_app_root() + "/xunguagua/cookie.txt", encoding="GBK").read().strip()
    sess = requests.Session()
    sess.headers.update({
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "yun.xunguagua.com",
        "Referer": "http://yun.xunguagua.com/member/?app=member&controller=list",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": cookie
    })
    return sess


def run(context):
    sess = init_session()
    results = []
    for type_key in ["1", "2"]:
        results.extend(run_pages(sess, type_key, context))

    if results:
        write_results(results)
    print("found results " + str(len(results)) + " for type " + type_key)
    return len(results)


def run_pages(sess, type_key, context):
    start_url = context["start_url"]
    results = []
    page = 1
    while page < 9999:
        resp = sess.get(_URL_.format(type=type_key, page=page))
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
            # 没有输入起始url，从启动时发现的第一条url开始计算
            if not start_url["xgg"+type_key]:
                start_url["xgg" + type_key] = url

            if start_url["xgg"+type_key] == url:
                page = 10000
                break

            pub_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(pub_time))
            results.append((title, pub_time, url))
        print("page " + str(page) + " finished, current size: " + str(len(results)))
        time.sleep(2)
        page += 1

    if results:
        # 记录这次抓到的最新的url
        start_url["xgg"+type_key] = results[0][1]
    return results


def write_results(results):
    sent_list_f = open(app_env.get_app_root() + "/xunguagua/sent-list.csv", encoding="UTF-8", mode="w")
    urls_f = open(app_env.get_app_root() + "/xunguagua/urls.txt", encoding="UTF-8", mode="w")
    for result in results:
        sent_list_f.write(",".join(result) + "\n")
        urls_f.write(result[2] + "\n")
    sent_list_f.flush()
    sent_list_f.close()
    urls_f.flush()
    urls_f.close()
