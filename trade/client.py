# coding=utf-8
import hashlib
import urllib.error
import urllib.parse
import urllib.request
from time import time

import requests

from .global_fun import Sleep


class Client:
    def __init__(self, access_key, secret_key, need_proxy, proxy):
        self._access_key = access_key
        self._secret_key = secret_key
        self.session = requests.session()
        self.proxy = dict(http=proxy, https=proxy)
        if need_proxy:
            self.session.proxies = self.proxy

    def _signature(self, params):
        """生成签名"""
        params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        message = urllib.parse.urlencode(params).encode()

        m = hashlib.md5()
        m.update(message)
        m.digest()

        sig = m.hexdigest()
        return sig

    def _send_request(self, method, params, optional=None):

        # 在参数中增加必须的字段
        params['created'] = int(time())
        params['access_key'] = self._access_key
        params['secret_key'] = self._secret_key
        params['method'] = method

        # 添加签名
        sign = self._signature(params)
        params['sign'] = sign
        del params['secret_key']

        # 添加选填参数
        if optional:
            params.update(optional)

        # 发送请求
        payload = urllib.parse.urlencode(params)

        r = self.session.post("https://api.huobi.com/apiv3", params=payload)
        if r.status_code == 200:
            data = r.json()
            if 'code' in data:
                raise Exception("交易失败，原因：" + data['message'])
            return data
        else:
            raise Exception("method:" + method + "请求失败")

    def query_account_info(self):
        """查询余额
        https://github.com/huobiapi/API_Docs/wiki/REST-get_account_info

        :return:dict
            total	总资产折合
            net_asset	净资产折合
            available_cny_display	可用人民币
            available_btc_display	可用比特币
            frozen_btc_display	冻结比特币
            frozen_cny_display	冻结人民币
        """
        method = 'get_account_info'
        params = {}
        optional = {'market': 'cny'}
        return self._send_request(method, params, optional)

    def query_orders_in_progress(self):
        """获取所有正在进行的委托
        https://github.com/huobiapi/API_Docs/wiki/REST-get_orders

        :return:
            id	委托订单id
            type	1买 2卖
            order_price	委托价格
            order_amount	委托数量
            processed_amount	已经完成的数量
            order_time	委托时间
        """
        method = 'get_orders'
        params = {'coin_type': 1}
        optional = {'market': 'cny'}
        return self._send_request(method, params, optional)

    def query_recently_orders(self):
        """查询个人最新10条已成交订单
        https://github.com/huobiapi/API_Docs/wiki/REST-get_new_deal_orders

        :return:
        """
        method = 'get_new_deal_orders'
        params = {'coin_type': 1}
        optional = {'market': 'cny'}
        return self._send_request(method, params, optional)

    def query_order(self, order_id):
        """查询委托详情
        https://github.com/huobiapi/API_Docs/wiki/REST-order_info

        :param order_id: 订单id
        :return:
        """
        method = 'order_info'
        params = {
            'coin_type': 1,
            'id': order_id
        }
        optional = {'market': 'cny'}
        return self._send_request(method, params, optional)

    def cancel_order(self, order_id):
        """撤销订单
        https://github.com/huobiapi/API_Docs/wiki/REST-cancel_order

        :param order_id: 订单id
        :return:
        """
        method = 'cancel_order'
        params = {
            'coin_type': 1,
            'id': order_id
        }
        optional = {'market': 'cny'}
        return self._send_request(method, params, optional)

    def market_price_buy(self, amount):
        """市价买
        https://github.com/huobiapi/API_Docs/wiki/REST-buy_market

        :param amount: 买入总金额
        :return:
            result	成功状态 success
            id	委托id
        """
        method = 'buy_market'
        params = {
            'coin_type': 1,
            'amount': amount
        }
        optional = {'trade_password': '',
                    'trade_id': '',
                    'market': 'cny'}
        return self._send_request(method, params, optional)

    def market_price_sell(self, amount):
        """市价卖
        https://github.com/huobiapi/API_Docs/wiki/REST-sell_market

        :param amount: 卖BTC数量
        :return:
        """
        method = 'sell_market'
        params = {
            'coin_type': 1,
            'amount': amount
        }
        optional = {'trade_password': '',
                    'trade_id': '',
                    'market': 'cny'}
        return self._send_request(method, params, optional)

    def limit_price_buy(self, amount, price):
        """限价单买
        https://github.com/huobiapi/API_Docs/wiki/REST-buy

        :param amount: 买数量
        :param price: 买价格
        :return:
        """
        method = 'buy'
        params = {
            'coin_type': 1,
            'print': price,
            'amount': amount
        }
        optional = {'trade_password': '',
                    'trade_id': '',
                    'market': 'cny'}
        return self._send_request(method, params, optional)

    def limit_price_sell(self, amount, price):
        """限价单卖
        https://github.com/huobiapi/API_Docs/wiki/REST-sell

        :param amount: 卖数量
        :param price: 卖价格
        :return:
        """
        method = 'sell'
        params = {
            'coin_type': 1,
            'print': price,
            'amount': amount
        }
        optional = {'trade_password': '',
                    'trade_id': '',
                    'market': 'cny'}
        return self._send_request(method, params, optional)

    def get_kline(self, period, length=300):
        """获取k线
        https://github.com/huobiapi/API_Docs/wiki/REST-Interval

        :return:
        """
        url = "http://api.huobi.com/staticmarket/btc_kline_[period]_json.js?length=" + str(length)
        url = url.replace("[period]", period)  # 1分钟，返回300条
        try:
            r = self.session.get(url)
            if r.status_code == 200:
                data = r.json()
                return data
        except Exception as e:
            print(e)
            return None

    def get_market_status(self, ltc=False):
        """实时行情数据接口
        https://github.com/huobiapi/API_Docs/wiki/REST-Candlestick-Chart
        http://api.huobi.com/staticmarket/ticker_btc_json.js

        :return:
        """
        url = "http://api.huobi.com/staticmarket/ticker_btc_json.js"
        if ltc:
            url = "http://api.huobi.com/staticmarket/ticker_ltc_json.js"
        try:
            r = self.session.get(url)
            if r.status_code == 200:
                data = r.json()
                return data
        except Exception as e:
            print(e)
            return None

    def get_deal_detail(self):
        """买卖盘实时成交数据
        https://github.com/huobiapi/API_Docs/wiki/REST-Order-Book-and-TAS
        http://api.huobi.com/staticmarket/detail_btc_json.js

        :return:
        """

        url = "http://api.huobi.com/staticmarket/detail_btc_json.js"
        try:
            r = self.session.get(url)
            if r.status_code == 200:
                data = r.json()
                return data
        except Exception as e:
            print(e)
            return None

    def _save_record(self, rid):
        from . import dao
        order = self.query_order(rid)
        status = order['status']
        d_status = {0: '未成交', 1: '部分成交', 2: '已完成', 3: '已取消', 4: '废弃（该状态已不再使用）', 5: '异常', 6: '部分成交已取消', 7: '队列中'}
        d_type = ['限价买', '限价卖', '市价买', '市价卖']
        count = 0
        while 1:
            if status == 2:
                id = order['id']
                type = d_type[order['type'] - 1]
                order_amount = order['order_amount']
                fee = order['fee']
                price = order['processed_price']
                final_amount = order['total']
                dao.insert_to_db_trade(id, price, order_amount, type, final_amount, fee)
                break
            elif status == 1 or status == 7 or status == 0:
                if count == 10:
                    break
                count += 1
                Sleep(500)
                order = self.query_order(rid)
                status = order['status']
