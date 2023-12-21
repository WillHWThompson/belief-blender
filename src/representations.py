#!/bin/python3
"""
Module: representations.py
Description: This module provides functions for generating text representations of comments and markets.
Authors: Jean-Gabriel Young <jyoung22@uvm.edu>
"""
from datetime import datetime
from collections.abc import Iterable
import manifoldpy


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

def market_text_representation(marketSlug):
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
    market = manifoldpy.api.get_slug(marketSlug)
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
