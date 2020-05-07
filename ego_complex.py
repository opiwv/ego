#code compiled by orion hollin from social feed manager (SFM)
#tutorial and guidelines at the following hyperlinks -
#code guidelines:
#https://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20170720-building-social-network-graphs-JSON.ipynb
#node mapping tutorial for SFM:
#https://gwu-libraries.github.io/sfm-ui/posts/2017-09-08-sna

import sys
import json
import re
import numpy as np
from datetime import datetime
import pandas as pd  

tweetfile = 'opiwv.json'

# 1. Export edges from Retweets

fh = open(tweetfile, 'r')

userdata = pd.DataFrame(columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count' ))
edges = pd.DataFrame(columns=('Source','Target','Strength'))

for line in fh:
    try:
        tweet = json.loads(line)
    except:
        continue
    if 'retweeted_status' not in tweet:
        continue
    
    userdata = userdata.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['user']['screen_name'],
                                tweet['user']['created_at'],
                                tweet['user']['profile_image_url_https'],
                                tweet['user']['followers_count'],
                                tweet['user']['friends_count']]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)
    userdata = userdata.append(pd.DataFrame([[tweet['retweeted_status']['user']['id_str'],
                                tweet['retweeted_status']['user']['screen_name'],
                                tweet['retweeted_status']['user']['created_at'],
                                tweet['retweeted_status']['user']['profile_image_url_https'],
                                tweet['retweeted_status']['user']['followers_count'],
                                tweet['retweeted_status']['user']['friends_count']]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)                 
    edges = edges.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['retweeted_status']['user']['id_str'],
                                str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))]]
                                , columns=('Source','Target','Strength')), ignore_index=True)           
# 2. Export edges from Mentions

fh = open(tweetfile, 'r')

userdata = pd.DataFrame(columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count' ))
edges = pd.DataFrame(columns=('Source','Target','Strength'))

for line in fh:
    try:
        tweet = json.loads(line)
    except:
        continue
    if len(tweet['entities']['user_mentions']) == 0:
        continue
    
    for mention in tweet['entities']['user_mentions']:
        userdata = userdata.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['user']['screen_name'],
                                tweet['user']['created_at'],
                                tweet['user']['profile_image_url_https'],
                                tweet['user']['followers_count'],
                                tweet['user']['friends_count']]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)
        if len(userdata[userdata['Id'].str.contains(mention['id_str'])]) == 0:
            userdata = userdata.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['user']['screen_name'],
                                np.nan,
                                np.nan,
                                np.nan,
                                np.nan]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)
        edges = edges.append(pd.DataFrame([[tweet['user']['id_str'],
                                    mention['id_str'],
                                    str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))]]
                                    , columns=('Source','Target','Strength')), ignore_index=True)  
# 3. Export edges from Replies

fh = open(tweetfile, 'r')

userdata = pd.DataFrame(columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count' ))
edges = pd.DataFrame(columns=('Source','Target','Strength'))

for line in fh:
    try:
        tweet = json.loads(line)
    except:
        continue
    if tweet['in_reply_to_user_id_str'] is None:
        continue

    userdata = userdata.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['user']['screen_name'],
                                tweet['user']['created_at'],
                                tweet['user']['profile_image_url_https'],
                                tweet['user']['followers_count'],
                                tweet['user']['friends_count']]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)
    if len(userdata[userdata['Id'].str.contains(tweet['in_reply_to_user_id_str'])]) == 0:
            userdata = userdata.append(pd.DataFrame([[tweet['in_reply_to_user_id_str'],
                                tweet['in_reply_to_screen_name'],
                                np.nan,
                                np.nan,
                                np.nan,
                                np.nan]], columns=('Id','Label','user_created_at','profile_image','followers_count','friends_count')), ignore_index=True)
    edges = edges.append(pd.DataFrame([[tweet['user']['id_str'],
                                tweet['in_reply_to_user_id_str'],
                                str(datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))]]
                                , columns=('Source','Target','Strength')), ignore_index=True)

strengthLevel = 5  # Network connection strength level: the number of times in total each of the tweeters responded to or mentioned the other.
                   # If you have 1 as the level, then all tweeters who mentioned or replied to another at least once will be displayed. But if you have 5, only those who have mentioned or responded to a particular tweeter at least 5 times will be displayed, which means that only the strongest bonds are shown.

edges2 = edges.groupby(['Source','Target'])['Strength'].count()
edges2 = edges2.reset_index()
edges2 = edges2[edges2['Strength'] >= strengthLevel]

# Export nodes from the edges and add node attributes for both Sources and Targets.
userdata = userdata.sort_values(['Id','followers_count'], ascending=[True, False])
userdata = userdata.drop_duplicates(['Id'], keep='first') 

ids = edges2['Source'].append(edges2['Target']).to_frame()
ids.columns = ['Id']
ids = ids.drop_duplicates()

nodes = pd.merge(ids, userdata, on='Id', how='left')

# change column names for Kumu import (Run this when using Kumu)
nodes.columns = ['Id', 'Label', 'Date', 'Image', 'followers_count', 'friends_count']
edges2.columns = ['From','To','Strength']
# Print nodes to check
nodes.head(3)
# Print edges to check
edges2.head(3)
# Export nodes and edges to csv files
nodes.to_csv('nodes.csv', encoding='utf-8', index=False)
edges2.to_csv('edges.csv', encoding='utf-8', index=False)