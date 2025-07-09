
import unittest
import pandas as pd
from stock_predictor.core.indicators import (
    calculate_sma,
    calculate_rsi,
    calculate_macd,
    calculate_atr
)

class TestIndicators(unittest.TestCase):

    def setUp(self):
        """Set up a sample DataFrame for testing."""
        self.data = pd.DataFrame({
            'Open': [100, 102, 101, 103, 105],
            'High': [103, 104, 103, 105, 106],
            'Low': [99, 101, 100, 102, 104],
            'Close': [102, 103, 102, 104, 105]
        })

    def test_calculate_sma(self):
        """Tests the SMA calculation."""
        sma = calculate_sma(self.data, 3)
        self.assertEqual(len(sma), len(self.data))

    def test_calculate_rsi(self):
        """Tests the RSI calculation."""
        rsi = calculate_rsi(self.data, 14)
        self.assertEqual(len(rsi), len(self.data))

    def test_calculate_macd(self):
        """Tests the MACD calculation."""
        macd, signal = calculate_macd(self.data)
        self.assertEqual(len(macd), len(self.data))
        self.assertEqual(len(signal), len(self.data))

    def test_calculate_atr(self):
        """Tests the ATR calculation."""
        atr = calculate_atr(self.data)
        self.assertEqual(len(atr), len(self.data))

if __name__ == '__main__':
    unittest.main()
