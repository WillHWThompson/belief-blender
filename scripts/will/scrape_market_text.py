%load_ext autoreload
%autoreload 2 
#%autoreload 2
# market = results[0]
# print(market['slug'])
# my_slug = market['slug']
# my_market = mp.api.get_slug(my_slug)
# print(my_marA

import os 
import sys
sys.path.append("../src")
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

#load all of the bets into a single dataframe
file_glob = "/Users/willthompson/Documents/CSDS/side_projects/belief-blender/src/data/bets"

to_load=[]
file_list = glob.glob(file_glob + "/*.json")
market_ids = set()
#identify all of the unique market ids in the bets dataset
for path in tqdm(file_list):
    # print(path)
    with open(path, 'r') as f:
       df = pd.read_json(f)
       market_ids.update(set(df.contractId.unique()))


#GET MARKET DATA
market_ids_list = list(market_ids)
market_data = []
market_id_i = market_ids_list[1]

#loop through market ids and exract market data and append it to a list
for market_id_i in tqdm(market_ids_list):
    try:
        my_market = mp.api.get_market(market_id_i)
    except:
        print("market not found")
        continue
    market_dict = {}
    market_dict['id'] = market_id_i
    market_dict['creatorId'] = my_market.creatorId
    market_dict['createdTime'] = my_market.createdTime
    market_dict['question'] = my_market.question
    market_dict['tags'] = my_market.tags
    market_dict['totalLiquidity'] = my_market.totalLiquidity
    try:
        market_dict['text'] = market_text_representation(my_market)
    except:
        print("market not found")
        continue
    market_data.append(market_dict)

market_data_df = pd.DataFrame(market_data)
pd.to_parquet(market_data_df, "market_data.parquet")
