
import pandas as pd
import numpy as np
from stock_predictor.core.logger import get_logger

logger = get_logger(__name__)

def calculate_sma(data, window):
    """Calculates the Simple Moving Average (SMA)."""
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data, window):
    """Calculates the Exponential Moving Average (EMA)."""
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, fast_window=12, slow_window=26, signal_window=9):
    """Calculates the Moving Average Convergence Divergence (MACD)."""
    fast_ema = calculate_ema(data, fast_window)
    slow_ema = calculate_ema(data, slow_window)
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def calculate_atr(data, window=14):
    """Calculates the Average True Range (ATR)."""
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(window=window).mean()
