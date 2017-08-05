# encoding=utf-8

import numpy as np
import talib


def MA(records, period):
    return talib.MA(np.array([i.Close for i in records]), period).tolist()


def MACD(records, short, long, period):
    a, b, c = talib.MACD(np.array([i.Close for i in records]), short, long, period)
    c = 2 * c
    return c.tolist(), a.tolist(), b.tolist()


def BOLL(records, period, multiplier):
    upper, mid, lower = talib.BBANDS(np.array([i.Close for i in records]), period, multiplier, multiplier)
    return upper.tolist(), mid.tolist(), lower.tolist()
