# To run the tests, in root folder, use the command:
# python -m unittest main/tests/test_list.py

import unittest
from prod.binance import Binance
from common.delist import Delist

class TestDelist(unittest.TestCase):
    def test_get_binance_announcements_returns_list(self):
        result = Binance().get_list_announcements()
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