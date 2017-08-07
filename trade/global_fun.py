# coding=utf-8

import time

# create logger
import logging
from datetime import datetime

import sys

logger_name = 'btc'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)s: %(levelname)s: %(message)s"
formatter = logging.Formatter(fmt)

# create file handler
if len(sys.argv) > 1:
    now = datetime.now()
    log_path = "./log/{}-{}-{}_{}_{}_{}.log".format(now.year, now.month, now.day, now.hour, now.minute,
                                                    sys.argv[1])
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# create stream handler
sh = logging.StreamHandler()
sh.setFormatter(formatter)

# add handler and formatter to logger

logger.addHandler(sh)


def Log(msg):
    """保存一条信息到日志列表

    :param msg:
    :return:
    """
    logger.info(msg)


def Sleep(t):
    """参数为毫秒数,如Sleep(1000)为休眠一秒

    :param t: 毫秒数
    :return:
    """
    time.sleep(t / 1000)
