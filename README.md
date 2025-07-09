# Stock Predictor

## Overview

This project provides a stock analysis and recommendation system. It fetches historical stock data, performs technical analysis, and recommends stocks based on predefined criteria. The system is designed to be efficient, utilizing concurrent data fetching to handle a growing list of stock symbols.

## Features

-	**Concurrent Data Fetching:** Efficiently fetches historical stock data for multiple symbols simultaneously using `yfinance`.
-	**Technical Analysis:** Calculates key indicators such as Simple Moving Average (SMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Average True Range (ATR).
-	**Stock Recommendation:** Identifies potential buy opportunities based on customizable criteria, including uptrend and RSI levels.
-	**Configurable Settings:** Easily adjust recommendation parameters and API keys through dedicated configuration files.
-	**Logging:** Comprehensive logging to track the application's operations and aid in debugging.

## Setup

To set up and run this project, follow these steps:

### Prerequisites

-	Python 3.8 or higher
-	`pip` (Python package installer)

### Installation

1.	**Navigate to the project directory:**

    ```bash
    cd "C:\Users\Admin\Desktop\trading project"
    ```

2.	**Install dependencies:**

    The project uses a `requirements.txt` file to manage its dependencies. Install them using pip:

    ```bash
    pip install -r stock_predictor/requirements.txt
    ```

3.	**Set up Environment Variables:**

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

-	**Format:** Each stock symbol should be on a new line, under the `Symbol` header.
-	**No Duplicates:** Ensure each stock symbol appears only once in the list to avoid redundant processing and duplicate recommendations.

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

-	`STOCK_PRICE_RANGE`: A tuple defining the minimum and maximum price for a stock to be considered for recommendation. (e.g., `(100, 5000)`)
-	`TIME_FRAME_DAYS`: The number of days for historical data fetching (currently set to 1 year by default in `api_fetcher.py`, but this setting can be integrated if needed for more granular control).
-	`TOP_N_STOCKS`: The number of top recommended stocks to display.

### 3. Modifying Recommendation Logic (`core/recommender.py`)

The core recommendation criteria are defined in `stock_predictor/core/recommender.py`.

Currently, a stock is recommended if it meets the following conditions:

-	It is in an **Uptrend** (last price > 50-day SMA).
-	It is **Not Overbought** (RSI <= 70).

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

-	**No Recommendations:**
    -	**Strict Criteria:** The current recommendation criteria might be too strict. Consider relaxing them in `core/recommender.py` or adjusting thresholds in `config/settings.py`.
    -	**Insufficient Data:** Ensure `yfinance` is able to fetch data for all symbols. Check for warnings like "No data found for X. It might be delisted or an invalid ticker." in the logs.
-	**Duplicate Recommendations:** Ensure there are no duplicate stock symbols in your `Stock_List.csv` file.
-	**API Rate Limits:** If you encounter issues with data fetching, you might be hitting API rate limits from `yfinance` or NewsAPI. Consider adding delays between requests (advanced topic) or reducing the number of stocks processed at once.

## Technical Deep Dive

This section provides a more in-depth look into the technical architecture and design choices of the Stock Predictor project.

### 1. Architecture Overview

The project follows a modular architecture, separating concerns into distinct components:

-	**`main.py`**: The entry point of the application, responsible for loading stock symbols, initiating the recommendation process, and displaying results.
-	**`config/`**: Contains configuration settings (`settings.py`) and environment variables (`.env`).
-	**`core/`**: Houses the core logic of the application, including:
    -	`api_fetcher.py`: Handles fetching raw stock data from external APIs (e.g., `yfinance`).
    -	`analyzer.py`: Performs technical analysis on stock data to derive indicators and trends.
    -	`recommender.py`: Implements the stock recommendation logic based on analyzed data.
    -	`indicators.py`: Contains functions for calculating various technical indicators.
    -	`logger.py`: Configures and provides logging utilities.
-	**`tests/`**: Contains unit tests for various modules to ensure correctness and prevent regressions.

### 2. Concurrency Model

To address performance bottlenecks associated with fetching data for a large number of stock symbols, the project utilizes **`concurrent.futures.ThreadPoolExecutor`**.

-	**Rationale:** Fetching data from external APIs is an I/O-bound operation (waiting for network responses). `ThreadPoolExecutor` is ideal for such tasks as it allows multiple API requests to be made concurrently, significantly reducing the overall execution time compared to sequential fetching.
-	**Implementation:** The `recommender.py` module submits `get_stock_data` calls for each ticker to a thread pool. `as_completed` is then used to process results as they become available, rather than waiting for all tasks to finish.

### 3. Data Flow

The data flows through the system in a clear pipeline:

1.	**Stock Symbols Loading:** `main.py` loads stock symbols from `Stock_List.csv`.
2.	**Data Fetching:** For each symbol, `api_fetcher.py` (via `get_stock_data`) fetches historical price data using the `yfinance` library.
3.	**Technical Analysis:** The fetched data is passed to `analyzer.py`, which calculates various technical indicators (SMA, RSI, MACD, ATR) using functions from `indicators.py`.
4.	**Recommendation Logic:** The analyzed data (including calculated indicators) is then fed into `recommender.py`, where predefined rules are applied to determine if a stock should be recommended.
5.	**Output:** Finally, `main.py` displays the recommended stocks to the user.

### 4. Technical Indicators Implementation

The `core/indicators.py` module encapsulates the logic for calculating standard technical indicators:

-	**Simple Moving Average (SMA):** Calculated as the average of a stock's closing prices over a specified period. Used to identify trends.
-	**Relative Strength Index (RSI):** A momentum oscillator that measures the speed and change of price movements. Used to identify overbought or oversold conditions.
-	**Moving Average Convergence Divergence (MACD):** A trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. Used to identify bullish or bearish momentum.
-	**Average True Range (ATR):** A measure of market volatility. Used in calculating stop-loss and target prices.

These calculations are performed using `pandas` for efficient data manipulation.

### 5. Modularity and Separation of Concerns

The project is structured to promote modularity and separation of concerns:

-	Each core function (data fetching, analysis, recommendation, logging) resides in its own dedicated module.
-	Configuration settings are centralized in `config/settings.py`, making them easy to manage and modify without altering core logic.
-	Tests are separated into their own directory, ensuring that changes to the codebase can be verified independently.
This structure enhances maintainability, readability, and testability.

### 6. Error Handling and Logging

-	**Error Handling:** Basic error handling is implemented, particularly around API calls (e.g., `FileNotFoundError` for `Stock_List.csv`, `data.empty` checks for `yfinance` responses, `try-except` blocks for network issues).
-	**Logging:** The `core/logger.py` module provides a centralized logging mechanism. It uses Python's built-in `logging` module to output messages to both a file (`stock_predictor.log`) and the console. Different logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) allow for flexible control over the verbosity of output, which is crucial for debugging and monitoring the application.

### 7. External Libraries

The project leverages several powerful Python libraries:

-	**`yfinance`**: For fetching historical stock data from Yahoo Finance.
-	**`newsapi-python`**: For fetching stock-related news (though currently not actively used in the recommendation logic).
-	**`pandas`**: Essential for data manipulation and analysis, especially for handling time-series stock data and calculating indicators.
-	**`numpy`**: Used by `pandas` for numerical operations.
-	**`matplotlib`**: For plotting stock data (currently commented out in `main.py`).
-	**`python-dotenv`**: For loading environment variables from a `.env` file.
-	**`peewee`**: (Indirectly used by `yfinance`) A lightweight ORM, likely used by `yfinance` for caching or internal data management.
