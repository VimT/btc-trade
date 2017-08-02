# coding=utf-8
from trade import *

buy_abs = -20
buy_cl_abs = 15
sell_abs = 20
sel_cl_abs = 15
N = 3
rate = 1.01
sell_price_abs = 30


class Part:
    def __init__(self, buy_flag, buy_price, low_macd, high_macd, high_sel_price):
        self.buy_flag = buy_flag
        self.buy_price = buy_price
        self.low_macd = low_macd
        self.high_macd = high_macd
        self.high_sel_price = high_sel_price


def main():
    Log(exchange.GetAccount())
    Log("this is test begin")

    parts = [Part(0, 0, 99999, 0, 0) for _ in range(N)]

    has_buy = 0
    can_buy = True
    lowest = 99999

    while True:
        recs = exchange.GetRecords(PERIOD_M5)
        macd, _, _ = TA.MACD(recs, 12, 26, 9)
        acc = exchange.GetAccount()
        balance = acc.Balance
        stocks = acc.Stocks
        ticker = exchange.GetTicker()

        last1 = macd[-1]
        last2 = macd[-2]

        Log(acc)
        Log(f"行情:{ticker.Buy} MACD:{last1}  {last2}")

        if lowest - 100 > ticker.Buy or last1 > 0:
            can_buy = True

        for i in parts:
            if i.buy_flag == 0:
                if last1 < buy_abs and last1 < i.low_macd:
                    i.low_macd = last1
                if last1 < buy_abs and last1 - i.low_macd > buy_cl_abs and can_buy:
                    buy = balance / (N - has_buy)
                    exchange.Buy(buy)
                    has_buy += 1
                    balance -= buy
                    i.buy_flag = 1
                    can_buy = False
                    i.buy_price = ticker.Buy
                    lowest = ticker.Buy
                    i.high_macd = 0
                    i.high_sel_price = 0
                    Log(f"买入价格:{ticker.Buy} MACD:{last1}  {last2}")
            if i.buy_flag == 1:
                if last1 > sell_abs and last1 > i.high_macd:
                    i.high_macd = last1

                if last1 > sell_abs and ticker.Sell > i.high_sel_price:
                    i.high_sel_price = ticker.Sell

                if last1 > sell_abs and i.high_macd - last1 > sel_cl_abs \
                        and ticker.Sell / i.buy_price >= rate \
                        and i.high_sel_price - ticker.Sell > sell_price_abs:
                    sell = stocks / has_buy
                    exchange.Sell(sell)
                    has_buy -= 1
                    stocks -= sell
                    i.buy_flag = 0
                    i.low_macd = 99999
                    Log(f"卖出价格:{ticker.Sell} MACD:{last1}  {last2}")
                    # Log(str(macd[2][len(macd[2])-1])+"  "+str(macd[2][len(macd[2])-2]))
        Sleep(60000)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(exchange.GetAccount())
        exit(0)
