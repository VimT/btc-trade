# coding=utf-8
from trade import *

start_time = "2017-08-13 20:40:00"  # time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+2*60*60))
end_time = "2017-08-14 10:00:00"  # time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+22*60*60))

N = 2
rate = 1.01


class Part:
    def __init__(self, buy_flag, buy_price, thresh, x):
        self.buy_flag = buy_flag
        self.buy_price = buy_price
        self.thresh = thresh
        self.x = x


def check_time():
    if time.time() < time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')):
        # 未到起始时间
        return -1
    if time.time() > time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')):
        # 到达终止时间
        return 0
    # 进行策略
    return 1


def get_lowest_buy_price(parts):
    ret = 99999
    for i in parts:
        if i.buy_flag == True and i.buy_price < ret:
            ret = i.buy_price
    return ret


def sell(stocks):
    btc = round(stocks - 0.00005, 4)
    if btc < 0.001:
        Log("错误: 交易数量过少:" + str(round(stocks, 6)))
    else:
        exchange.Sell(btc)


def buy(balance):
    cny = round(balance - 0.005, 2)
    if cny <= 0:
        Log("错误: 交易数量过少:" + str(round(balance, 6)))
    else:
        exchange.Buy(cny)


def main():
    Log(exchange.GetAccount())
    # 初始化N个仓
    parts = [Part(False, 0, 0, 0) for _ in range(N)]
    buy_count = 0

    # 允许买入标志
    can_buy = True
    stop_loss = False
    time_count = 0
    time_flag = False

    # -1不能买卖 0可以买入 1可以卖出
    select = -1
    buy_abs = 3
    while True:
        Sleep(60000)

        # 拉取K线记录
        recs = exchange.GetRecords(PERIOD_M5)
        # 计算BOLL线和KDJ线
        # up, mid, low = TA.BOLL(recs, 20, 2)
        # K, D, J = TA.KDJ(recs, 9, 3, 3)
        [macd, dif, dea] = TA.MACD(recs, 12, 26, 9)
        # 获取账户信息和此时的买卖信息
        acc = exchange.GetAccount()
        ticker = exchange.GetTicker()

        # 检查策略起始, 终止时间
        if check_time() == -1:
            continue
        if check_time() == 0:
            Log("终止时间到, 卖出所有!")
            Log(str(acc))
            sell(acc.Stocks)
            acc = exchange.GetAccount()
            Log(str(acc))
            break
        if time_flag == False:
            Log("开始时间到, 策略开始运行!")
            time_flag = True

        # 每隔1小时打印一次账户信息
        time_count += 1
        if time_count % 60 == 0:
            Log(str(acc))

        # 刷新买入标志
        low_buy_price = get_lowest_buy_price(parts)
        if low_buy_price - 100 > ticker.Buy:
            can_buy = True

        if macd[-4] + macd[-6] + macd[-5] + macd[-7] < -10:
            select = 0
        elif macd[-4] + macd[-6] + macd[-5] + macd[-7] > 10:
            select = 1
        else:
            select = -1

        # 打印行情
        Log("行情: " + str(ticker.Buy) + "  " + str(select) + "  " + str(stop_loss) + "  " + str(
            round(macd[-1])) + " " + str(round(macd[-2])) + " " + str(round(dif[-2])) + " " + str(round(dea[-2])))

        if stop_loss == True and dea[-2] >= dea[-3]:
            stop_loss = False

        # 遍历仓位
        for i in parts:
            if i.buy_flag == True and macd[-1] < -30:
                if ticker.Buy >= i.thresh + i.x:
                    i.x += -macd[-1]
                else:
                    if ticker.Buy >= i.thresh:
                        i.thresh += i.x / 2
                        i.x = 0
                    else:
                        Log("befor stop_loss sell:" + str(acc))
                        sell(acc.Stocks / buy_count)
                        buy_count -= 1
                        stop_loss = True
                        i.buy_flag = False
                        acc = exchange.GetAccount()
                        Log("after stop_loss sell:" + str(acc))
                        continue
                        # 买入条件
            if i.buy_flag == False and can_buy == True and stop_loss == False:
                if macd[-1] > 3 and select == 0 and dea[-1] < 0:
                    Log("befor buy:" + str(acc))
                    buy(acc.Balance / (N - buy_count))
                    buy_count += 1
                    can_buy = False
                    i.buy_flag = True
                    i.buy_price = ticker.Buy
                    i.x = 0
                    i.thresh = ticker.Buy - 300
                    acc = exchange.GetAccount()
                    Log("after buy:" + str(acc))

            # 卖出条件
            if i.buy_flag == True and select == 1:
                if macd[-1] < -5 and ticker.Sell / i.buy_price >= rate:
                    Log("before sell:" + str(acc))
                    sell(acc.Stocks / buy_count)
                    buy_count -= 1
                    i.buy_flag = False
                    acc = exchange.GetAccount()
                    Log("after sell:" + str(acc))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print(exchange.GetAccount())
        exit(0)
