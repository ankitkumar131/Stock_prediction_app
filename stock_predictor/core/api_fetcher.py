
import yfinance as yf
from newsapi import NewsApiClient
from stock_predictor.config.settings import NEWS_API_KEY
from stock_predictor.core.logger import get_logger

logger = get_logger(__name__)

def get_stock_data(ticker, period="1y"):
    """Fetches historical stock data from yfinance."""
    logger.info(f"Fetching historical data for {ticker}...")
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    if data.empty:
        logger.warning(f"No data found for {ticker}. It might be delisted or an invalid ticker.")
    return data

def get_stock_news(query):
    """Fetches stock news from NewsAPI."""
    logger.info(f"Fetching news for {query}...")
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    try:
        headlines = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
        return headlines
    except Exception as e:
        logger.error(f"Could not fetch news: {e}")
        return None
