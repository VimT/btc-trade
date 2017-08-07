# coding=utf-8
import threading
from datetime import datetime

from .client import Client
from .mock import MockClient
from .structures import *


class Trade:
    def __init__(self):
        from . import cf
        self._access_key = cf.get('config', 'access_key')
        self._secret_key = cf.get('config', 'secret_key')
        self.mock = cf.getboolean('config', 'mock')
        need_proxy = cf.getboolean('config', 'need_proxy')
        proxy = cf.get('config', 'proxy')
        if self.mock:
            self.client = MockClient(self._access_key, self._secret_key, need_proxy, proxy)
        else:
            self.client = Client(self._access_key, self._secret_key, need_proxy, proxy)

    def GetAccount(self):
        """返回交易所账户信息

        :return: 返回一个Account结构
        """
        response = self.client.query_account_info()
        return Account(float(response['available_cny_display']), float(response['frozen_cny_display']),
                       float(response['available_btc_display']), float(response['frozen_btc_display']))

    def GetTicker(self):
        """获取当前市场行情

        :return: 返回一个Ticker结构
        """
        response = self.client.get_market_status()
        data = response['ticker']
        return Ticker(data['high'], data['low'], data['sell'], data['buy'], data['last'], data['vol'])

    def GetRecords(self, period):
        """K线历史

        :param period:
        :return:
        """
        response = self.client.get_kline(period)
        result = []
        for i in response:
            t = i[0]
            time = datetime(int(t[:4]), int(t[4:6]), int(t[6:8]), int(t[8:10]), int(t[10:12]), int(t[12:14]),
                            int(t[14:]))
            result.append(Record(int(time.timestamp() * 1000), i[1], i[2], i[3], i[4], i[5]))
        return result

    def Buy(self, amount, price=-1):
        """买

        :param amount: 买价值多少的币
        :param price: 限定价格，-1则为市价单
        :return: 返回订单ID
        """
        if price == -1:
            response = self.client.market_price_buy(amount)
        else:
            response = self.client.limit_price_buy(amount, price)
        if response.get('result') == 'success':
            rid = response.get('id')
            threading.Thread(target=self.client._save_record, name='save' + str(rid), args=(rid,)).start()
            return rid
        else:
            raise Exception('交易失败：' + response)

    def Sell(self, amount, price=-1):
        """卖

        :param amount: 卖比特币数量
        :param price: 限定价格，-1则为市价单
        :return: 返回订单ID
        """
        if price == -1:
            response = self.client.market_price_sell(amount)
        else:
            response = self.client.limit_price_sell(amount, price)
        if response.get('result') == 'success':
            rid = response.get('id')
            threading.Thread(target=self.client._save_record, name='save' + str(rid), args=(rid,)).start()
            return rid
        else:
            raise Exception('交易失败：' + response)
