import unittest
import pyRofex
from parameterized import parameterized
from classes import Market, Symbol, BuyingStrategy, Price


class UnitTests(unittest.TestCase):

    def setUp(self):
        pyRofex.initialize(
            user="user",
            password="password",
            account="account",
            environment=pyRofex.Environment.REMARKET
        )
        self.right_test_symbol = Symbol("DOEne21")
        self.wrong_test_symbol = Symbol("DOEnero2021")
        self.existing_symbols = Market.get_existing_symbols()
        self.set_up_existing_symbols = ["DOEne21", "DODic20", "DOMar21"]
        self.price = Price("DOEne21")
        self.market_data_last_price = self.price.query_market_data(
            pyRofex.MarketDataEntry.LAST)
        self.market_data_bid_price = self.price.query_market_data(
            pyRofex.MarketDataEntry.BIDS)
        self.buying_strategy = BuyingStrategy("DOEne21")

    def test_get_existing_symbols_returns_list(self):
        self.assertIsInstance(self.existing_symbols, list)

    def test_validate_right_entered_symbol(self):
        self.symbol_to_validate = self.right_test_symbol.validate_entered_symbol(
            self.set_up_existing_symbols)
        self.assertTrue(self.symbol_to_validate)

    def test_validate_right_entered_symbol_returns_string(self):
        self.symbol_to_validate = self.right_test_symbol.validate_entered_symbol(
            self.set_up_existing_symbols)
        self.assertIsInstance(self.symbol_to_validate, str)

    def test_validate_wrong_entered_symbol(self):
        self.symbol_to_validate = self.wrong_test_symbol.validate_entered_symbol(
            self.set_up_existing_symbols)
        self.assertFalse(self.symbol_to_validate)

    def test_validate_wrong_entered_symbol_returns_none(self):
        self.symbol_to_validate = self.wrong_test_symbol.validate_entered_symbol(
            self.set_up_existing_symbols)
        self.assertIsInstance(self.symbol_to_validate, type(None))

    def test_query_market_data_last_price_returns_dict(self):
        self.assertIsInstance(self.market_data_last_price, dict)

    def test_query_market_data_bid_price_returns_dict(self):
        self.assertIsInstance(self.market_data_bid_price, dict)

    @parameterized.expand([
        [1, int],
        [10, int],
        [100, int],
        [1000, int],
        [1.99, float],
        [19.99, float],
        [199.99, float],
        [1999.99, float]
    ])
    def test_buy_fixed_price(self, number, return_value_type):
        testing_price = self.buying_strategy.buy_fixed_price(number)
        self.assertIsInstance(testing_price, return_value_type)

    @parameterized.expand([
        [10, 1, 9],
        [10.18, 1.19, 8.99],
        [100, 0.01, 99.99],
        [999.99, 1, 998.99],
        [1999.99, 564.99, 1435]
    ])
    def test_buy_fixed_quantity_less_than_bid_price(
            self,
            bid_price,
            fixed_quantity,
            buying_price
    ):
        testing_price = self.buying_strategy.buy_fixed_quantity_less_than_bid_price(
            bid_price,
            fixed_quantity
        )
        self.assertEqual(testing_price, buying_price)

    @parameterized.expand([
        [None, 50],
        [2000, 1999.99]
    ])
    def test_buy_one_cent_less_than_bid_or_50_with_None_Price(
            self,
            bid_price,
            buying_price
    ):
        testing_price = self.buying_strategy.buy_one_cent_less_than_bid_or_50(
            bid_price
        )
        self.assertEqual(testing_price, buying_price)


if __name__ == '__main__':
    unittest.main()
