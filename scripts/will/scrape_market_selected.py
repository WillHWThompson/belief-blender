
import sys
sys.path.append("../../src")
from scraping import *
import manifoldpy as mp
from datetime import datetime
import time
from bertopic import BERTopic
import matplotlib.pyplot as plt
from tqdm import tqdm
import requests 
import glob
import pandas as pd
import json

with open('../../src/data/markets_to_select', 'r') as f:
    # Read each line into a list
    market_data = f.readlines()
# Remove newline characters
market_data = [market.strip() for market in market_data][:5]

market_list = scrape_market_text(market_data)
pd.DataFrame(market_list).to_parquet("../../src/data/market_text_data.csv")

#loop through market ids and exract market data and append it to a list
