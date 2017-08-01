from trade import *


def main():
    Log(exchange.GetAccount())
    Log("this is test begin")
    buy_flag = 0
    buy_price = 0
    while True:
        recs = exchange.GetRecords(PERIOD_M1)
        avgs = TA.MA(recs, 10)
        avgs2 = TA.MA(recs, 60)
        dif = []
        dif_total = 0.0
        dif_count = 9
        for i in range(len(avgs) - 1, len(avgs) - 1 - dif_count, -1):
            d = avgs[i] - avgs2[i]
            dif.append(d)
            dif_total += d
        dif_avg = dif_total / dif_count
        # Log(dif)
        acc = exchange.GetAccount()
        ticker = exchange.GetTicker()
        # Log("log:"+str(dif[0])+" "+str(dif[1])+" "+str(dif_avg)+" "+str(ticker.Buy)+" "+str(ticker.Sell))
        if buy_flag == 0:
            if dif[0] < -100 and dif[0] > dif[1]:
                exchange.Buy(acc.Balance)
                buy_flag = 1
                buy_price = ticker.Buy
                Log("buy:" + str(dif[0]) + " " + str(dif[1]) + " " + str(dif_avg) + " " + str(ticker.Buy))
        else:
            if dif[0] > 50 and dif[0] < dif[1] and ticker.Sell / buy_price >= 1.01:
                exchange.Sell(acc.Stocks)
                buy_flag = 0
                Log("sell:" + str(dif[0]) + " " + str(dif[1]) + " " + str(dif_avg) + " " + str(ticker.Sell))
        Sleep(60000)


if __name__ == '__main__':
    main()
