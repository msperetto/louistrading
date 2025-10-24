# To run the tests, in root folder, use the command:
# python -m unittest main/tests/test_delist.py

import unittest
from prod.delist import Delist

class TestDelist(unittest.TestCase):
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

    def test_get_binance_announcements_returns_list(self):
        delist = Delist()
        result = delist.get_binance_announcements()
        # Check that result is a list
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0, "No announcements returned")
        # Check that each item in the list is a dictionary with expected keys
        for announcement in result:
            self.assertIsInstance(announcement, dict)
            self.assertIn('id', announcement)
            self.assertIn('code', announcement)
            self.assertIn('title', announcement)

if __name__ == '__main__':
    unittest.main()