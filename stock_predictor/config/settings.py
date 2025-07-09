
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Stock analysis parameters
STOCK_PRICE_RANGE = (900, 6000)
TIME_FRAME_DAYS = 20
TOP_N_STOCKS = 5
