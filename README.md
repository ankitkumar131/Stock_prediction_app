# Stock Predictor

## Overview

This project provides a stock analysis and recommendation system. It fetches historical stock data, performs technical analysis, and recommends stocks based on predefined criteria. The system is designed to be efficient, utilizing concurrent data fetching to handle a growing list of stock symbols.

## Features

-   **Concurrent Data Fetching:** Efficiently fetches historical stock data for multiple symbols simultaneously using `yfinance`.
-   **Technical Analysis:** Calculates key indicators such as Simple Moving Average (SMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Average True Range (ATR).
-   **Stock Recommendation:** Identifies potential buy opportunities based on customizable criteria, including uptrend and RSI levels.
-   **Configurable Settings:** Easily adjust recommendation parameters and API keys through dedicated configuration files.
-   **Logging:** Comprehensive logging to track the application's operations and aid in debugging.

## Setup

To set up and run this project, follow these steps:

### Prerequisites

-   Python 3.8 or higher
-   `pip` (Python package installer)

### Installation

1.  **Navigate to the project directory:**

    ```bash
    cd "C:\Users\Admin\Desktop\trading project"
    ```

2.  **Install dependencies:**

    The project uses a `requirements.txt` file to manage its dependencies. Install them using pip:

    ```bash
    pip install -r stock_predictor/requirements.txt
    ```

3.  **Set up Environment Variables:**

    The project uses a `.env` file for sensitive information like API keys. Create a file named `.env` in the `stock_predictor/` directory:

    ```
    # stock_predictor/.env
    NEWS_API_KEY=your_news_api_key_here
    ```

    Replace `your_news_api_key_here` with your actual API key from [NewsAPI](https://newsapi.org/).

## Usage

To run the stock recommendation system, execute the `main.py` script from the project root directory:

```bash
set PYTHONPATH=%PYTHONPATH%;C:\Users\Admin\Desktop\trading project && python stock_predictor/main.py
```

The application will fetch data, analyze stocks, and print recommendations to your console if any stocks meet the defined criteria.

## Customization

You can customize various aspects of the stock recommendation system to better suit your needs.

### 1. Adding/Updating Stock Details (`Stock_List.csv`)

To add or remove stock symbols for analysis, modify the `Stock_List.csv` file located in the project root directory (`C:\Users\Admin\Desktop\trading project\Stock_List.csv`).

-   **Format:** Each stock symbol should be on a new line, under the `Symbol` header.
-   **No Duplicates:** Ensure each stock symbol appears only once in the list to avoid redundant processing and duplicate recommendations.

    **Example `Stock_List.csv` content:**

    ```csv
    Symbol
    RELIANCE.NS
    TCS.NS
    INFY.NS
    # Add more symbols below
    ```

### 2. Adjusting Settings (`config/settings.py`)

Modify the `stock_predictor/config/settings.py` file to adjust core parameters:

-   `STOCK_PRICE_RANGE`: A tuple defining the minimum and maximum price for a stock to be considered for recommendation. (e.g., `(100, 5000)`)
-   `TIME_FRAME_DAYS`: The number of days for historical data fetching (currently set to 1 year by default in `api_fetcher.py`, but this setting can be integrated if needed for more granular control).
-   `TOP_N_STOCKS`: The number of top recommended stocks to display.

### 3. Modifying Recommendation Logic (`core/recommender.py`)

The core recommendation criteria are defined in `stock_predictor/core/recommender.py`.

Currently, a stock is recommended if it meets the following conditions:

-   It is in an **Uptrend** (last price > 50-day SMA).
-   It is **Not Overbought** (RSI <= 70).

Additionally, the recommendation is displayed only if its `confidence` score is above 75%.

You can modify these conditions to make the recommendations more or less strict. For example, to include `macd_bullish_cross` as a criterion:

```python
# In stock_predictor/core/recommender.py
# ...
        is_uptrend = analysis['trend'] == 'Uptrend'
        is_bullish_cross = analysis['macd_bullish_cross']
        is_not_overbought = not analysis['rsi_overbought']

        if is_uptrend and is_not_overbought and is_bullish_cross: # Added is_bullish_cross
# ...
```

### 4. Adjusting Logging (`core/logger.py`)

To change the verbosity of the logs, modify the `level` in `stock_predictor/core/logger.py`:

```python
# In stock_predictor/core/logger.py
# ...
logging.basicConfig(
    level=logging.INFO, # Change to logging.DEBUG for more detailed output
# ...
```

Common logging levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

## Troubleshooting

-   **No Recommendations:**
    -   **Strict Criteria:** The current recommendation criteria might be too strict. Consider relaxing them in `core/recommender.py` or adjusting thresholds in `config/settings.py`.
    -   **Insufficient Data:** Ensure `yfinance` is able to fetch data for all symbols. Check for warnings like "No data found for X. It might be delisted or an invalid ticker." in the logs.
-   **Duplicate Recommendations:** Ensure there are no duplicate stock symbols in your `Stock_List.csv` file.
-   **API Rate Limits:** If you encounter issues with data fetching, you might be hitting API rate limits from `yfinance` or NewsAPI. Consider adding delays between requests (advanced topic) or reducing the number of stocks processed at once.


```