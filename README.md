# 交易平台模块 接口文档

---

[toc]

## 说明
使用火币的API
为交易策略模块提供服务

### 依赖

- ta-lib
- numpy
- requests


## 下载与使用
```shell
git clone https://gitlab.com/562593188/btc.git
cd btc
touch config.ini  # 创建配置文件
python main.py
```

`config.ini`内容如下
```ini
[config]
mock = True  # 是否使用模拟交易
need_proxy = True  # 是否需要HTTP代理
proxy =  # HTTP代理地址
access_key =  # 火币access_key
secret_key =  # 火币secret_key
```


python console使用：
```python
from trade import *
```
导入了

1. `exchange = Trade()` 交易工具
2. TA库
3. 一些全局函数
4. 一些常量


### Trade类

`Trade` 实现了策略方会用到的的几个接口，实际是对`Client`类实例的封装

有以下接口：
```python
exchange.GetAccount()
exchange.GetTicker()
exchange.GetRecords(period)
exchange.Buy(amount)
exchange.Sell(amount)
```

### TA库
TA库是一个市场分析工具，这里是对`ta-lib`库的一个封装
```python
TA.MA(records, period)  # 移动平均线
TA.MACD(records, short, long, period)  # 指数平滑异同平均线
```

### 全局函数
```python
Log(msg)  # 写日志
Sleep(t)  # 休眠
```

### 全局变量
```python
# 以下是exchange.GetRecords(period) 可以传入的period
PERIOD_M1 = '001'
PERIOD_M5 = '005'
PERIOD_M15 = '015'
PERIOD_M30 = '030'
PERIOD_H1 = '060'
PERIOD_D1 = '100'
```

---



## exchange.client的接口
之前说`Trade`类实际是对`Client`的包装，所以可以通过 `exchange.client` 调用实际API接口，client返回的都是实际接口的返回值

### 获取行情

#### 获取K线
```Python
exchange.client.get_kline(period, length=300)
```

[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-Interval)



#### 实时行情数据接口
```Python
exchange.client.get_market_status()
```

[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-Candlestick-Chart)
[返回示例](http://api.huobi.com/staticmarket/ticker_btc_json.js)

#### 买卖盘实时成交数据
```Python
exchange.client.get_deal_detail()
```
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-Order-Book-and-TAS)
[返回示例](http://api.huobi.com/staticmarket/detail_btc_json.js)

---

### 查询个人信息与订单

#### 查询余额
```python
exchange.client.query_account_info()
```
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-get_account_info)

#### 获取所有正在进行的委托
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-get_orders)
```python
exchange.client.query_orders_in_progress()
```

####查询个人最新10条已成交订单
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-get_new_deal_orders)
```python
exchange.client.query_recently_orders()
```

#### 查询委托详情
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-order_info)
```python
exchange.client.query_order(order_id)
```

---

### 交易

#### 撤销订单
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-cancel_order)
```python
exchange.client.cancel_order(order_id)
```

#### 市价买
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-buy_market)
```python
exchange.client.market_price_buy(amount)
```

#### 市价卖
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-sell_market)
```python
exchange.client.market_price_sell(amount)
```

#### 限价单买
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-buy)
```python
exchange.client.limit_price_buy(amount, price)
```

#### 限价单卖
[官方API文档](https://github.com/huobiapi/API_Docs/wiki/REST-sell)
```python
exchange.client.limit_price_sell(amount, price)
```





