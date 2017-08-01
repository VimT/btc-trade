# encoding=utf-8
from unittest import TestCase

from trade.client import Client


class TestClient(TestCase):
    def setUp(self):
        self.client = Client("47877bd7-ff597182-6e6c4ca2-d0fb1", "34890b00-b820b016-dc3cdafe-ba350", True)

    def test_query_account_info(self):
        info = self.client.query_account_info()
        self.assertIn('total', info)

    def test_query_orders_in_progress(self):
        orders = self.client.query_orders_in_progress()
        self.assertIsInstance(orders, list)

    def test_query_recently_orders(self):
        orders = self.client.query_recently_orders()
        self.assertIsInstance(orders, list)

    def test_query_order(self):
        order = self.client.query_order(1)

    def test_cancel_order(self):
        r = self.client.cancel_order(1)

    def test_market_price_buy(self):
        self.skipTest("money!")
        r = self.client.market_price_buy(1)

    def test_market_price_sell(self):
        r = self.client.market_price_sell(1)

    def test_limit_price_buy(self):
        self.skipTest("money!")
        r = self.client.market_price_buy(1)

    def test_limit_price_sell(self):
        r = self.client.limit_price_sell(0.001, 1)
        print()

    def test_get_kline(self):
        r = self.client.get_kline()

    def test_get_market_status(self):
        r = self.client.get_market_status()

    def test_get_deal_detail(self):
        r = self.client.get_deal_detail()
