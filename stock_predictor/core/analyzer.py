
from stock_predictor.core.indicators import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_atr
)
from stock_predictor.core.logger import get_logger

logger = get_logger(__name__)

def analyze_stock(data):
    """Analyzes a stock's data to generate trading signals."""
    if data.empty:
        return None

    logger.info("Analyzing stock data...")

    # Calculate indicators
    data['sma_20'] = calculate_sma(data, 20)
    data['sma_50'] = calculate_sma(data, 50)
    data['rsi'] = calculate_rsi(data)
    data['macd'], data['macd_signal'] = calculate_macd(data)
    data['atr'] = calculate_atr(data)

    # Get the most recent data point
    latest = data.iloc[-1]

    # Analysis logic
    analysis = {
        'last_price': latest['Close'],
        'sma_20': latest['sma_20'],
        'sma_50': latest['sma_50'],
        'rsi': latest['rsi'],
        'macd_bullish_cross': latest['macd'] > latest['macd_signal'] and data.iloc[-2]['macd'] < data.iloc[-2]['macd_signal'],
        'rsi_oversold': latest['rsi'] < 30,
        'rsi_overbought': latest['rsi'] > 70,
        'trend': 'Uptrend' if latest['Close'] > latest['sma_50'] else 'Downtrend',
        'support': data['Low'].rolling(window=20).min().iloc[-1],
        'resistance': data['High'].rolling(window=20).max().iloc[-1],
    }

    # Calculate stop-loss and target
    analysis['stop_loss'] = latest['Close'] - (latest['atr'] * 1.5)
    analysis['target_price'] = latest['Close'] + (latest['atr'] * 2)

    return analysis
