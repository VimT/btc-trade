from trade import *

buy_abs = -20
buy_cl_abs = 15
sell_abs = 20
sel_cl_abs = 15


def main():
    Log(exchange.GetAccount())
    Log("this is test begin")
    buy_flag = 0
    buy_price = 0
    low_price = 99999
    high_price = 0
    while True:
        recs = exchange.GetRecords(PERIOD_M5)
        macd = TA.MACD(recs, 12, 26, 9)
        acc = exchange.GetAccount()
        ticker = exchange.GetTicker()
        Log("行情：" + str(ticker.Buy) + " MACD:" + str(macd[0][len(macd[0]) - 1]) + "  " + str(
            macd[0][len(macd[0]) - 2]))
        if buy_flag == 0:
            if macd[0][len(macd[0]) - 1] < buy_abs and macd[0][len(macd[0]) - 1] < low_price:
                low_price = macd[0][len(macd[0]) - 1]
            if macd[0][len(macd[0]) - 1] < buy_abs and macd[0][len(macd[0]) - 1] - low_price > buy_cl_abs:
                exchange.Buy(acc.Balance)
                buy_flag = 1
                buy_price = ticker.Buy
                high_price = 0
                Log("买入价格:" + str(ticker.Buy) + " MACD:" + str(macd[0][len(macd[0]) - 1]) + "  " + str(
                    macd[0][len(macd[0]) - 2]))
        else:
            if macd[0][len(macd[0]) - 1] > sell_abs and macd[0][len(macd[0]) - 1] > high_price:
                high_price = macd[0][len(macd[0]) - 1]
            if macd[0][len(macd[0]) - 1] > sell_abs and high_price - macd[0][
                        len(macd[0]) - 1] > sel_cl_abs and ticker.Sell / buy_price >= 1.01:
                exchange.Sell(acc.Stocks)
                buy_flag = 0
                low_price = 99999
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
