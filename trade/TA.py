# coding=utf-8

import numpy as np
import talib


def MA(records, period):
    # SMA的几种实现方式 https://discuss.tradewave.net/t/is-there-a-faster-sma-method-with-numpy-output-than-talib/691
    return talib.MA(np.array([i.Close for i in records]), period).tolist()


def MACD(records, short, long, period):
    a, b, c = talib.MACD(np.array([i.Close for i in records]), short, long, period)
    c = 2 * c
    return c.tolist(), a.tolist(), b.tolist()


def BOLL(records, period, multiplier):
    upper, mid, lower = talib.BBANDS(np.array([i.Close for i in records]), period, multiplier, multiplier)
    return upper.tolist(), mid.tolist(), lower.tolist()


def KDJ(records, n=9, k_period=3, d_period=3):
    # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
    close = np.array([i.Close for i in records])
    low = np.array([i.Low for i in records])
    high = np.array([i.High for i in records])

    RSV, _ = talib.STOCHF(high, low, close, 9, 3)

    length = len(records)
    K = np.zeros(length)
    D = np.zeros(length)

    K[n] = 50.0
    D[n] = 50.0

    for i in range(n + 1, length):
        K[i] = (1 * RSV[i] + (k_period - 1) * K[i - 1]) / k_period
        D[i] = (1 * K[i] + (d_period - 1) * D[i - 1]) / d_period
    J = 3 * K - 2 * D
    return K, D, J
