# coding=utf-8
from trade import *

buy_abs = -20
buy_cl_abs = 15
sell_abs = 20
sel_cl_abs = 15
N = 3
rate = 1.01
sell_price_abs = 30


def main():
    Log(exchange.GetAccount())
    Log("this is test begin")
    buy_flag = {}
    buy_price = {}
    low_macd = {}
    high_macd = {}
    high_sel_price = {}
    for i in range(0, N, 1):
        buy_flag[i] = 0
        buy_price[i] = 0
        low_macd[i] = 99999
        high_macd[i] = 0
        high_sel_price[i] = 0

    has_buy = 0
    can_buy = 1
    lowest = 99999

    while True:
        recs = exchange.GetRecords(PERIOD_M5)
        macd = TA.MACD(recs, 12, 26, 9)
        acc = exchange.GetAccount()
        balance = acc.Balance
        stocks = acc.Stocks
        ticker = exchange.GetTicker()
        Log(acc)
        Log("行情:" + str(ticker.Buy) + " MACD:" + str(macd[0][len(macd[0]) - 1]) + "  " + str(
            macd[0][len(macd[0]) - 2]))
        if lowest - 100 > ticker.Buy or macd[0][len(macd[0]) - 1] > 0:
            can_buy = 1

        for i in range(0, N, 1):
            if buy_flag[i] == 0:
                if macd[0][len(macd[0]) - 1] < buy_abs and macd[0][len(macd[0]) - 1] < low_macd[i]:
                    low_macd[i] = macd[0][len(macd[0]) - 1]
                if macd[0][len(macd[0]) - 1] < buy_abs and macd[0][len(macd[0]) - 1] - low_macd[i] > buy_cl_abs and can_buy == 1:
                    buy = balance / (N - has_buy)
                    exchange.Buy(buy)
                    has_buy += 1
                    balance -= buy
                    buy_flag[i] = 1
                    can_buy = 0
                    buy_price[i] = ticker.Buy
                    lowest = ticker.Buy
                    high_macd[i] = 0
                    high_sel_price[i] = 0
                    Log("买入价格:" + str(ticker.Buy) + " MACD:" + str(macd[0][len(macd[0]) - 1]) + "  " + str(
                        macd[0][len(macd[0]) - 2]))
            if buy_flag[i] == 1:
                if macd[0][len(macd[0]) - 1] > sell_abs and macd[0][len(macd[0]) - 1] > high_macd[i]:
                    high_macd[i] = macd[0][len(macd[0]) - 1]

                if macd[0][len(macd[0]) - 1] > sell_abs and ticker.Sell > high_sel_price[i]:
                    high_sel_price[i] = ticker.Sell

                if macd[0][len(macd[0]) - 1] > sell_abs and high_macd[i] - macd[0][
                            len(macd[0]) - 1] > sel_cl_abs and ticker.Sell / buy_price[i] >= rate and high_sel_price[
                    i] - ticker.Sell > sell_price_abs:
                    sell = stocks / has_buy
                    exchange.Sell(sell)
                    has_buy -= 1
                    stocks -= sell
                    buy_flag[i] = 0
                    low_macd[i] = 99999
                    Log("卖出价格:" + str(ticker.Sell) + " MACD:" + str(macd[0][len(macd[0]) - 1]) + "  " + str(
                        macd[0][len(macd[0]) - 2]))
                    # Log(str(macd[2][len(macd[2])-1])+"  "+str(macd[2][len(macd[2])-2]))
        Sleep(60000)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(exchange.GetAccount())
        exit(0)
