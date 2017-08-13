# coding=utf-8

"""
几个会用到的数据结构
"""


class Account:
    def __init__(self, Balance, FrozenBalance, Stocks, FrozenStocks, NetAsset):
        """账户信息

        :param Balance: 余额，人民币
        :param FrozenBalance: 冻结的余额
        :param Stocks: BTC数量
        :param FrozenStocks: 冻结的BTC数量
        """
        self.Balance = Balance
        self.FrozenBalance = FrozenBalance
        self.Stocks = Stocks
        self.FrozenStocks = FrozenStocks
        self.NetAsset = NetAsset

    def __str__(self):
        return f"净资产：{self.NetAsset}，可用余额：{self.Balance}, 冻结的余额：{self.FrozenBalance}, BTC数量：{self.Stocks}，冻结的BTC数量：{self.FrozenBalance}"

    def __repr__(self):
        return "<Account %s>" % self


class Record:
    def __init__(self, Time, Open, High, Low, Close, Volume):
        """标准OHLC结构, 用来画K线和指标分析用

        :param Time: 毫秒的时间戳
        :param Open: 开盘价
        :param High: 最高价
        :param Low: 最低价
        :param Close: 收盘价
        :param Volume: 交易量
        """
        self.Time = Time
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.Volume = Volume

    def __str__(self):
        return f"毫秒的时间戳：{self.Time}， 开盘价：{self.Open}， 最高价：{self.High}， 最低价：{self.Low}， 收盘价：{self.Close}， 交易量：{self.Volume}"

    def __repr__(self):
        return "<Record %s>" % self


class Ticker:
    def __init__(self, High, Low, Sell, Buy, Last, Volume):
        """市场行情

        :param High: 最高价
        :param Low: 最低价
        :param Sell: 卖一价
        :param Buy: 卖一价
        :param Last: 最后成交价
        :param Volume: 最近成交量
        """
        self.High = High
        self.Low = Low
        self.Sell = Sell
        self.Buy = Buy
        self.Last = Last
        self.Volume = Volume

    def __str__(self):
        return f"最高价：{self.High}，最低价：{self.Low}，卖一价：{self.Sell}，买一价：{self.Buy}，最后成交量：{self.Last}，最近成交量：{self.Volume}"

    def __repr__(self):
        return "<Ticker %s>" % self
