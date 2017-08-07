# coding=utf-8
from trade.client import Client


class MockClient(Client):
    def __init__(self, access_key, secret_key, need_proxy, proxy):
        Client.__init__(self, access_key, secret_key, need_proxy, proxy)
        self.available_cny_display = 100
        self.available_btc_display = 0

    def market_price_sell(self, amount):
        last = Client.get_market_status(self)['ticker']['last']
        self.available_cny_display += amount * last
        self.available_btc_display -= amount
        return dict(result='success', id=0)

    def market_price_buy(self, amount):
        last = Client.get_market_status(self)['ticker']['last']
        self.available_cny_display -= amount
        self.available_btc_display += amount / last
        return dict(result='success', id=0)

    def query_account_info(self):
        return dict(available_cny_display=self.available_cny_display,
                    available_btc_display=self.available_btc_display,
                    frozen_cny_display=0, frozen_btc_display=0)

    def _save_record(self, rid):
        pass
