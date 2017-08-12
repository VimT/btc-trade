# 交易平台模块 接口文档

---

[toc]

## 说明
使用火币的API
为交易策略模块、网站提供服务，使用数据方的接口

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
exchange.GetAccount()  # 获取交易所账户信息，返回一个Account类实例
exchange.GetTicker()  # 获取当前市场行情，返回一个Ticker类实例
exchange.GetRecords(period)  # K线历史，period为K线周期，默认返回300条K线记录
exchange.Buy(amount, price=-1)  # 买操作
exchange.Sell(amount, price=-1)  # 卖操作
```

### TA库
TA库是一个市场分析工具，这里是对`ta-lib`库的一个封装
```python
real = TA.MA(records, period)  # 移动平均线
macdhist, macdsignal, macd = TA.MACD(records, short, long, period)  # 指数平滑异同平均线
upperband, middleband, lowerband = BOLL(records, period, multiplier)  # 布林线
```

### 全局函数
```python
Log(msg)  # 记录日志，会打印到屏幕，存储到文件和数据库
Sleep(millisecond)  # 休眠时间
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

### 数据结构
定义了几种数据接口，方便策略方使用。
```python
class Account:
    def __init__(self, Balance, FrozenBalance, Stocks, FrozenStocks, NetAsset):
        """账户信息，exchange.GetAccount()返回

        :param Balance: 余额，人民币
        :param FrozenBalance: 冻结的余额
        :param Stocks: BTC数量
        :param FrozenStocks: 冻结的BTC数量
        """
        ...
```

```python
class Record:
    def __init__(self, Time, Open, High, Low, Close, Volume):
        """标准OHLC结构, 用来画K线和指标分析用，exchange.GetRecords(period)返回

        :param Time: 毫秒的时间戳
        :param Open: 开盘价
        :param High: 最高价
        :param Low: 最低价
        :param Close: 收盘价
        :param Volume: 交易量
        """
        ...
```

```python
class Ticker:
    def __init__(self, High, Low, Sell, Buy, Last, Volume):
        """实时市场行情，exchange.GetTicker()返回

        :param High: 最高价
        :param Low: 最低价
        :param Sell: 卖一价
        :param Buy: 卖一价
        :param Last: 最后成交价
        :param Volume: 最近成交量
        """
        ...
```

---



## exchange.client的接口
之前说`Trade`类实际是对`Client`的包装，所以可以通过 `exchange.client` 调用实际API接口，client返回的都是实际接口的返回值。但一般不会直接使用他，一般是在做手动操作或者调试的时候才调用。

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

## 模拟交易
继承Client类，根据需要，重写

    market_price_sell(amount)
    market_price_buy(amount)
    query_account_info()

三个方法，即实现模拟交易，方便策略方测试策略。



