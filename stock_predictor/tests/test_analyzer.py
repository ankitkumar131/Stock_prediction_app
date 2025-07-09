
import unittest
import pandas as pd
from stock_predictor.core.analyzer import analyze_stock

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set up a sample DataFrame for testing."""
        self.data = pd.DataFrame({
            'Open': [100, 102, 101, 103, 105, 106, 107, 108, 109, 110],
            'High': [103, 104, 103, 105, 106, 107, 108, 109, 110, 111],
            'Low': [99, 101, 100, 102, 104, 105, 106, 107, 108, 109],
            'Close': [102, 103, 102, 104, 105, 106, 107, 108, 109, 110]
        })

    def test_analyze_stock(self):
        """Tests that analyze_stock returns a dictionary with the expected keys."""
        analysis = analyze_stock(self.data)
        self.assertIsInstance(analysis, dict)
        expected_keys = [
            'last_price', 'sma_20', 'sma_50', 'rsi', 'macd_bullish_cross',
            'rsi_oversold', 'rsi_overbought', 'trend', 'support', 'resistance',
            'stop_loss', 'target_price'
        ]
        for key in expected_keys:
            self.assertIn(key, analysis)

if __name__ == '__main__':
    unittest.main()
