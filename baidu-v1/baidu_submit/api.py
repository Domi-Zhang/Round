from flask import request

from baidu_submit.service import BaiduSubmit

baidu_submit = BaiduSubmit()


def register_routes(app):
    @app.route('/baidu-submit/api/echo')
    def echo():
        return 'ok'

    @app.route('/baidu-submit/api/sync', methods=['GET', 'POST'])
    def run_sync():
        url = request.values.get("url")
        success = baidu_submit.submit(url)
        return "ok" if success else "failed"

    @app.route('/baidu-submit/api/async', methods=['GET', 'POST'])
    def run_async():
        url = request.values.get("url")
        priority = request.values.get("priority")
        priority = priority if priority is not None else 5  # 默认优先级是5，1为最高优先级
        baidu_submit.append_buffer(url, priority)
        return "ok"
