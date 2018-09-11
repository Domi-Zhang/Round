from logging.handlers import RotatingFileHandler

from flask import Flask, logging

from baidu_submit import api

app = Flask(__name__)

api.register_routes(app)

if __name__ == '__main__':
    logger = logging.getLogger('werkzeug')
    handler = RotatingFileHandler("logs/access.log", maxBytes=4096 * 1024, backupCount=10)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    app.run(host="0.0.0.0",
            port=19501,
            debug=False,
            threaded=True)
