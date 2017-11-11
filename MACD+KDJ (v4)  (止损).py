N=2 
rate = 1.01 

start_time = "2017-08-14 11:00:00"#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+2*60*60))
end_time = "2017-08-14 20:00:00"#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+22*60*60))

class Part:
    def __init__(self, buy_flag, buy_price, thresh, x):
        self.buy_flag = buy_flag
        self.buy_price = buy_price
        self.thresh = thresh
        self.x = x
        
def check_time():
    if time.time() < time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')):
        #未到起始时间
        return -1 
    if time.time() > time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')):
        #到达终止时间
        return 0
    #进行策略
    return 1

def get_lowest_buy_price(parts):
    ret = 99999
    for i in parts:
        if i.buy_flag == True and i.buy_price < ret:
            ret = i.buy_price
    return ret    

def sell(stocks):
    btc = round(stocks - 0.00005 , 4)
    if btc < 0.001:
        Log("交易数量过少:" + str(round(stocks, 6)))
    else:
        exchange.Sell(btc)
        
def buy(balance):
    cny = round(balance - 0.005, 2)
    if cny <= 0:
        Log("交易数量过少:" + str(round(balance, 6)))
    else:
        exchange.Buy(cny)
        
def KDJ_cross(K,D,J):
    if (K[-2] < D[-2] and K[-1] >= D[-1] and D[-1] < 60) or K[-1] < D[-1] < 20:
        return 0
    if (K[-3] > D[-3] and K[-2] <= D[-2]) or (K[-2] > D[-2] and K[-1] <= D[-1]):
        return 1
    return -1  

def main():
    Log(exchange.GetAccount())
    #初始化N个仓
    parts = [Part(False, 0, 0, 0) for _ in range(N)]
    buy_count = 0
    
    #允许买入标志
    can_buy = True
    stop_loss = False
    time_count = 0
    time_flag = False
    
    #-1不能买卖 0可以买入 1可以卖出
    select = -1
    while True:
        Sleep(60000)
        
        #拉取K线记录
        recs = exchange.GetRecords(PERIOD_M5)
        #计算BOLL线和KDJ线
        #up, mid, low = TA.BOLL(recs, 20, 2)
        K, D, J = TA.KDJ(recs, 9, 3, 3)
        [dif, dea, macd] = TA.MACD(recs,12,26,9)
        #获取账户信息和此时的买卖信息
        acc = exchange.GetAccount()
        ticker = exchange.GetTicker()

        
        #检查策略起始, 终止时间
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
            
        #每隔1小时打印一次账户信息
        time_count += 1
        if time_count % 60 == 0:
            Log(str(acc))
        
        #刷新买入标志
        low_buy_price = get_lowest_buy_price(parts)
        if low_buy_price - 100 > ticker.Buy:
            can_buy = True
        
        if select != 0 and macd[-3] + macd[-4] + macd[-5] + macd[-2] < 0:
            select = 0
            can_buy = True
        elif select != 1 and macd[-3] + macd[-4] + macd[-5] + macd[-2] > 0:
            select = 1
                
        #打印行情
        Log("行情: "+str(ticker.Buy)+"  "+str(select)+"  "+str(stop_loss)+"  MACD:"+str(round(macd[-1]))+" "+str(round(macd[-2]))+"  KDJ:("+str(round(K[-1]))+" "+str(round(D[-1]))+")("+str(round(K[-2]))+" "+str(round(D[-2]))+")")
        
        
        if stop_loss == True and (dea[-2] >= dea[-3] or macd[-1] > 0):
            stop_loss = False
        
        #遍历仓位
        for i in parts:
            if i.buy_flag == True and macd[-1] < -30 and D[-1] - K[-1] > 1:
                if ticker.Buy >= i.thresh + i.x:
                    i.x += -macd[-1]
                else:
                    if ticker.Buy >= i.thresh:
                        i.thresh += i.x / 2
                        i.x = 0
                    else:
                        Log("before stop_loss sell:" + str(acc))
                        sell(acc.Stocks / buy_count)
                        buy_count -= 1
                        stop_loss = True
                        i.buy_flag = False 
                        acc = exchange.GetAccount()
                        Log("after stop_loss sell:" + str(acc))
                        continue       
            #买入条件
            if i.buy_flag == False and can_buy == True and stop_loss == False  and select == 0:
                if (KDJ_cross(K,D,J) == 0 or macd[-1] > 3) and D[-1] < 60:
                    Log("before buy:" + str(acc))
                    buy(acc.Balance / (N - buy_count))
                    buy_count += 1
                    can_buy = False
                    i.buy_flag = True 
                    i.buy_price = ticker.Buy
                    i.x = 0
                    i.thresh = ticker.Buy - 500
                    acc = exchange.GetAccount()
                    Log("after buy:" + str(acc))
                    
            #卖出条件
            if i.buy_flag == True and select == 1:
                if macd[-1] < -3 and ticker.Sell / i.buy_price >= rate:
                    Log("before sell:" + str(acc))
                    sell(acc.Stocks / buy_count)
                    buy_count -= 1
                    i.buy_flag = False 
                    acc = exchange.GetAccount()
                    Log("after sell:" + str(acc))
        
        
        
        
        
        
        
        
        
        
        