import manifoldpy
from datetime import datetime
from collections.abc import Iterable
from tqdm import tqdm
import manifoldpy as mp


def _text_date(timestamp):
    """Turn timestamp into a text date in the format of mm-dd-yyyy."""
    return datetime.utcfromtimestamp(timestamp/1000).strftime('%m-%d-%Y')

def _textify(comment):
    """Turn a comment into a text representation."""
    return [y['text'] for x in comment.content['content'] 
            if (x['type'] == 'paragraph' and  isinstance(x.get('content'), Iterable)) 
            for y in x.get('content') if y.get('type') == 'text']

def comment_text_representation(comment):
    """Turn a comment into a full text representation including dates and likes."""
    representation = "[Date]: " + _text_date(comment.createdTime) + "\n" \
        "[Likes] " + str(comment.likes) + "\n" \
        "[Text]: " + " ".join(_textify(comment)) + "\n"
    return representation


def market_text_representation(market):
    """Construct text representation of a market from its slug.
    
    Parameters
    ----------
    marketSlug : str
        The slug of the market to be represented.
    
    Returns
    -------
    str
        The text representation of the market.
    """
    # get market from slug
    marketSlug = market.slug
    # get comments by market creator
    comment_data = manifoldpy.api.get_comments(marketSlug=marketSlug)
    comments = [c for c in comment_data if c.userId == market.creatorId]
    representation = "[Market title] " + market.question + "\n" + \
        '[Market description] ' + market.textDescription + "\n" + \
        '[Market creator] ' + market.creatorName + "\n" + \
        '[Creation date] ' + _text_date(market.createdTime) + "\n" + \
        '[Closing data] ' + _text_date(market.closeTime) + "\n" + \
        "------------------------------------------------------\n" + \
        "Comments by market creator\n" + \
        "------------------------------------------------------\n" + \
        "---\n".join([comment_text_representation(c) for c in comments])
    return representation



def scrape_market_text(market_id_list):
    """
    Scrapes market data for a given list of market IDs.

    Args:
        market_id_list (list): A list of market IDs to scrape.

    Returns:
        list: A list of dictionaries containing the scraped market data.
    """
    market_data = []
    for market_id_i in tqdm(market_id_list):
        print(market_id_i)
        try:
            my_market = mp.api.get_market(market_id_i)
        except Exception as e:
            print(e)
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
        return market_data