# encoding=utf-8

import numpy as np
import talib


def MA(records, period):
    return talib.MA(np.array([i.Close for i in records]), period).tolist()


def MACD(records, short, long, period):
    a, b, c = talib.MACD(np.array([i.Close for i in records]), short, long, period)
    return a.tolist(), b.tolist(), c.tolist()
