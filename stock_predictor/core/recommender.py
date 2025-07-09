
from concurrent.futures import ThreadPoolExecutor, as_completed
from stock_predictor.core.api_fetcher import get_stock_data
from stock_predictor.core.analyzer import analyze_stock
from stock_predictor.config.settings import STOCK_PRICE_RANGE
from stock_predictor.core.logger import get_logger

logger = get_logger(__name__)

def recommend_stocks(tickers):
    """Recommends stocks based on a set of rules, fetching data concurrently."""
    recommendations = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(get_stock_data, ticker): ticker for ticker in tickers}
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                data = future.result()
                if data.empty:
                    logger.warning(f"Skipping {ticker}: No data or empty data received.")
                    continue
                
                analysis = analyze_stock(data)
                if not analysis:
                    logger.info(f"Skipping {ticker}: No analysis generated.")
                    continue
                
                logger.debug(f"Analysis for {ticker}: {analysis}") # Added debug log

                # Recommendation logic
                price_in_range = STOCK_PRICE_RANGE[0] <= analysis['last_price'] <= STOCK_PRICE_RANGE[1]
                is_uptrend = analysis['trend'] == 'Uptrend'
                is_bullish_cross = analysis['macd_bullish_cross']
                is_not_overbought = not analysis['rsi_overbought']

                if is_uptrend and is_not_overbought:
                    confidence_score = (analysis['rsi'] / 100) * 0.4 + (1 if is_bullish_cross else 0) * 0.6
                    recommendations.append({
                        'ticker': ticker,
                        'last_price': analysis['last_price'],
                        'target_price': analysis['target_price'],
                        'stop_loss': analysis['stop_loss'],
                        'confidence': round(confidence_score * 100, 2)
                    })
            except Exception as exc:
                logger.error(f'{ticker} generated an exception: {exc}')
                
    # Sort by confidence
    recommendations.sort(key=lambda x: x['confidence'], reverse=True)
    return recommendations
