
import unittest
from stock_predictor.core.api_fetcher import get_stock_data

class TestApiFetcher(unittest.TestCase):

    def test_get_stock_data_valid_ticker(self):
        """Tests that get_stock_data returns a DataFrame for a valid ticker."""
        data = get_stock_data("TCS.NS")
        self.assertFalse(data.empty)

    def test_get_stock_data_invalid_ticker(self):
        """Tests that get_stock_data returns an empty DataFrame for an invalid ticker."""
        data = get_stock_data("INVALIDTICKER")
        self.assertTrue(data.empty)

if __name__ == '__main__':
    unittest.main()
