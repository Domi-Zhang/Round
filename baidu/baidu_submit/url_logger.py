# coding=utf-8
import logging
import os
from logging.handlers import RotatingFileHandler

import app_env


class UrlLogger:
    __loggers = dict()

    @classmethod
    def get_instance(cls, logger_name):
        if logger_name not in cls.__loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel("INFO")

            log_file_path = app_env.get_app_root() + "/baidu_submit/logs"
            if not os.path.exists(log_file_path):
                os.makedirs(log_file_path)
            fh = RotatingFileHandler(log_file_path + "/" + logger_name, maxBytes=4096 * 1024, backupCount=10)
            fmt = logging.Formatter('%(message)s')
            fh.setFormatter(fmt)
            logger.addHandler(fh)
            cls.__loggers[logger_name] = logger
        return cls.__loggers[logger_name]
