# encoding=utf-8
from unittest import TestCase

from trade import Trade


class TestTrade(TestCase):
    def setUp(self):
        self.exchange = Trade()

    def test_GetAccount(self):
        r = self.exchange.GetAccount()
        print()

    def test_GetTicker(self):
        r = self.exchange.GetTicker()
        print()

    def test_Buy(self):
        r = self.exchange.Buy(10000)
        print()

    def test_Sell(self):
        r = self.exchange.Sell(100000)
        print()
