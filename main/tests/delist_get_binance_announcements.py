import unittest
from common.delist import Delist

class TestDelistGetBinanceAnnouncements(unittest.TestCase):
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
            self.assertIn('type', announcement)
            self.assertIn('releaseDate', announcement)
        

if __name__ == '__main__':
    unittest.main()