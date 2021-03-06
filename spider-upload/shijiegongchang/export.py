import time

import requests
from bs4 import BeautifulSoup

import app_env

_URL = "https://company.ch.gongchang.com/qiye3785770-9aeb/product.html?page={}"


def init_session():
    sess = requests.Session()
    sess.headers.update({
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,mr;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "Hm_lvt_a39a1bb1395dcbf5a2fd98bbce30ec99=1547910755,1547952441; Hm_lpvt_a39a1bb1395dcbf5a2fd98bbce30ec99=1547952441; Hm_lvt_1feded28e200c1f62aa6738cb40e9f68=1547910755,1547952441; Hm_lpvt_1feded28e200c1f62aa6738cb40e9f68=1547952441",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    })
    return sess


def run_pages(sess, context):
    start_url = context["start_url"]
    results = []
    page = 1
    while page < 9999:
        list_resp = sess.get(_URL.format(page), verify=False)
        list_resp.encoding = "UTF-8"
        html_entity = BeautifulSoup(list_resp.text, 'html.parser')
        links = html_entity.select("#content div.pro-recommend-list a")
        for link in links:
            title = link.attrs["title"]
            href = link.attrs["href"]
            if href.find("//") == 0:
                href = "https:" + href

            # 没有输入起始url，从启动时发现的第一条url开始计算
            if not start_url["sjgc"]:
                start_url["sjgc"] = href

            if start_url["sjgc"] == href:
                page = 10000
                break

            results.append((title, href))
        print("page " + str(page) + " finished, current size: " + str(len(results)))
        time.sleep(2)
        page += 1

    if results:
        # 记录这次抓到的最新的url
        start_url["sjgc"] = results[0][1]
    return results


def run(context):
    sess = init_session()
    results = run_pages(sess, context)
    if results:
        write_results(results)
    return len(results)


def write_results(results):
    sent_list_f = open(app_env.get_app_root() + "/shijiegongchang/sent-list.csv", encoding="UTF-8", mode="w")
    urls_f = open(app_env.get_app_root() + "/shijiegongchang/urls.txt", encoding="UTF-8", mode="w")
    for result in results:
        sent_list_f.write(",".join(result) + "\n")
        urls_f.write(result[1] + "\n")
    sent_list_f.flush()
    sent_list_f.close()
    urls_f.flush()
    urls_f.close()
