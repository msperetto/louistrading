# To run the tests, in root folder, use the command:
# python -m unittest main/tests/delist_check_ticker_in_futures.py

import unittest

from common.delist import Delist

class TestDelistCheckTickerInFutures(unittest.TestCase):
    def test_check_ticker_in_futures_true(self):
        delist = Delist()
        # Act
        result = delist.check_ticker_in_futures('BTCUSDT')
        # Assert
        self.assertTrue(result)

    def test_check_ticker_in_futures_false(self):
        delist = Delist()
        # Act
        result = delist.check_ticker_in_futures('SOMEFAKETICKER')
        # Assert
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()