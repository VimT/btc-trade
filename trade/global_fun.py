# encoding=utf-8

import time

# create logger
import logging

logger_name = "btc"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)s: %(levelname)s: %(message)s"
formatter = logging.Formatter(fmt)

# create file handler
log_path = "btc.log"
fh = logging.FileHandler(log_path)
fh.setFormatter(formatter)

# create stream handler
sh = logging.StreamHandler()
sh.setFormatter(formatter)

# add handler and formatter to logger
logger.addHandler(fh)
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
