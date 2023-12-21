import glob
import pandas as pd
import json
from tqdm import tqdm

#load all of the bets into a single dataframe
file_glob = "data/bets"

to_load=[]
file_list = glob.glob(file_glob + "/*.json")
market_ids = set()
df_list = []
#identify all of the unique market ids in the bets dataset
for path in tqdm(file_list):
    # print(path)
    with open(path, 'r') as f:
       df = pd.read_json(f)
       df_list.append(df)
df_mega = pd.concat(df_list)
df_mega.to_json("data/combined_bets.json")
       #market_ids.update(set(df.contractId.unique()))
