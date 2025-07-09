import csv
import pandas as pd
from stock_predictor.core.recommender import recommend_stocks
from stock_predictor.core.api_fetcher import get_stock_data
from stock_predictor.core.logger import get_logger
import matplotlib.pyplot as plt

logger = get_logger(__name__)

def load_stock_symbols(file_path):
    """Loads stock symbols from a CSV file."""
    symbols = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbols.append(row['Symbol'])
    except FileNotFoundError:
        logger.error(f"Stock list file not found: {file_path}")
    return symbols

def plot_recommendation(ticker, analysis):
    """Plots the stock data with recommendation details."""
    data = get_stock_data(ticker, period="6m")
    if data.empty:
        return

    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price')
    plt.axhline(y=analysis['target_price'], color='g', linestyle='--', label=f"Target: {analysis['target_price']:.2f}")
    plt.axhline(y=analysis['stop_loss'], color='r', linestyle='--', label=f"Stop-Loss: {analysis['stop_loss']:.2f}")
    plt.title(f"{ticker} Recommendation")
    plt.legend()
    plt.show()

def main(progress_callback=None):
    """Main function to run the stock recommender."""
    logger.info("Starting stock recommendation analysis...")
    
    stock_list_file = "Stock_List.csv"
    stock_symbols = load_stock_symbols(stock_list_file)

    if not stock_symbols:
        logger.error("No stock symbols loaded. Exiting.")
        return []

    recommendations = recommend_stocks(stock_symbols, progress_callback=progress_callback)

    return recommendations

if __name__ == "__main__":
    main()
