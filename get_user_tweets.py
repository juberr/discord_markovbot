#!/usr/bin/env python
# coding: utf-8

import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

BEARER = os.getenv('TWITTER_BEARER')

# In[57]:


def get_user_tweets(userid):
    
    out = []
    
    #get first 100 tweets and add to output
    url = "https://api.twitter.com/2/users/{}/tweets".format(userid)
    headers = {"Authorization": "Bearer {}".format(BEARER)}
    
    params = {
    "max_results": 100,
    "exclude": "retweets,replies"
    }

    response = requests.request("GET", url, headers=headers, params=params)



    next_token = response.json()['meta']['next_token']
    
    for i in response.json()['data']:
        out.append(i['text'])
        
    #get next ~700 tweets using the next token in parameters, add to output
    for i in range(10):

        next_params = {
            "max_results": 100,
            "exclude": "retweets,replies",
            "pagination_token": next_token
        }
        
        next_response = requests.request("GET", url, headers=headers, params=next_params)
        
        data = next_response.json()
        
        if 'data' in data:
            for i in data['data']:
                out.append(i['text'])

            if "next_token" not in data['meta']:
                break
            else:
                next_token = data['meta']['next_token']
        
         
    return out