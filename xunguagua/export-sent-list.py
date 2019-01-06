import json
import time

import os
import requests

_URL_ = "http://yun.xunguagua.com/member/?app=member&controller=list&type={type}&page={page}"

print("input cookie:")
cookie = input()

print("choose type, 1-供求, 2-新闻")
type_key = input()

last_title = "_NONE_"
if os.path.exists("./sent-list.csv"):
    for line in open("./sent-list.csv", encoding="GBK"):
        line = line.strip()
        if not line:
            continue
        last_title = line.split(",")[0]
if last_title != "_NONE_":
    print("found last title: " + last_title)

results = []
page = 1
while page < 9999:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "yun.xunguagua.com",
        "Referer": "http://yun.xunguagua.com/member/?app=member&controller=list",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    resp = requests.get(_URL_.format(type=type_key, page=page), headers=headers)
    if resp.status_code != 200:
        print("got status code: " + str(resp.status_code))

    sent_list_resp = json.loads(resp.text)
    sent_list = sent_list_resp["list"]
    if not sent_list or len(results) >= int(sent_list_resp["total"]):
        break

    for sent_log in sent_list:
        title = sent_log["title"].replace(",", "，").strip()
        if title == last_title:
            print("encounter last title<{}>, stop.".format(title))
            page = 10000
            break
        results.append(title + "," + sent_log["url"])

    print("page " + str(page) + " finished, current size: " + str(len(results)))
    time.sleep(2)
    page += 1

with open("./sent-list.csv", encoding="GBK", mode="a") as f:
    f.write("\n".join(reversed(results)))
