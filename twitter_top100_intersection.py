from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from twitter_authentication_keys import get_account_credentials
import pprint
import numpy as np
import os.path
import random
import time
import hashlib
import base64
import json
import sys
import re
import io

if __name__ == '__main__':
    date_string = datetime.now().strftime("%Y%m%d%H%M")
    consumer_key, consumer_secret, access_token, access_token_secret = get_account_credentials()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)
    print "Signing in as: "+auth_api.me().name
    follower_list = {}
    filename = "top-100-bot-search/serialized.txt"
    print "Reading serialized data: " + filename
    if os.path.exists(filename):
        handle = open(filename, "r")
        follower_list = json.load(handle)
        handle.close()
    user_lists = {}
    for path, dirs, files in os.walk("top-100-bot-search"):
        for filename in files:
            if "serialized.txt" not in filename:
                filepath = os.path.join(path, filename)
                with open(filepath) as f:
                    lines = f.read().splitlines()
                for line in lines:
                    if filename in user_lists:
                        user_lists[filename].append(line)
                    else:
                        user_lists[filename] = []
                        user_lists[filename].append(line)

    id_list = []
    for twid, count in sorted(follower_list.items(), key=lambda x:x[1], reverse=True):
        if count > 20:
            id_list.append(twid)
    print
    print "Found: " + str(len(id_list))

    output_string = "ID | Screen_name | created_at | following | followers | tweets | default_profile | default_profile_image | follows_trump\n"
    raw_data = "ID | Screen_name | created_at | following | followers | tweets | default_profile | default_profile_image | follows_trump\n"

    id_count = 0
    block_count = 0
    id_blocks = {}
    for twid in id_list:
        if block_count in id_blocks:
            id_blocks[block_count].append(twid)
        else:
            id_blocks[block_count] = []
            id_blocks[block_count].append(twid)
        id_count += 1
        if id_count >= 99:
            id_count = 0
            block_count += 1
    print "Found " + str(block_count) + " data blocks."

    bots_found = 0
    trumps_found = 0
    for block, data in id_blocks.iteritems():
        print "Iterating block:" + str(block) + "/" + str(block_count)
        users_list = auth_api.lookup_users(user_ids=data)
        for item in users_list:
            screen_name = item.screen_name
            user_id = item.id_str
            tweets = item.statuses_count
            likes = item.favourites_count
            lists = item.listed_count
            default_profile = "No"
            default_profile_image = "No"
            follows_trump = "No"
            if user_id in user_lists["realDonaldTrump.txt"]:
                follows_trump = "Yes"
            if item.default_profile is True:
                default_profile = "Yes"
            if item.default_profile_image is True:
                default_profile_image = "Yes"
            following = item.friends_count
            followers = item.followers_count
            created_day = item.created_at.day
            created_month = item.created_at.month
            created_year = item.created_at.year
            created_date = item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            current_row = user_id + " | " + screen_name + " | " + created_date + " | " + str(following) + " | " + str(followers) + " | " + str(tweets) + " | " + default_profile + " | " + default_profile_image + " | " + follows_trump + "\n"

            raw_data += current_row
            if ("Yes" in default_profile) and ("Yes" in default_profile_image) and (tweets == 0):
                    if (created_year == 2017) and (created_month == 6) and (created_day == 1):
                        output_string += current_row
                        bots_found += 1
                        if "Yes" in follows_trump:
                            trumps_found += 1

            filename = "top-100-bot-search/potential-bots-" + date_string + ".txt"
            handle = open(filename, "w")
            handle.write(output_string)
            handle.close

            filename = "top-100-bot-search/raw-data-" + date_string + ".txt"
            handle = open(filename, "w")
            handle.write(raw_data)
            handle.close

    print "Found: " + str(bots_found)
    print "Found: " + str(trumps_found) + " bots following trump."

