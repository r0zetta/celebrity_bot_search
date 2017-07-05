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

input_file = "top100.txt"
output_file = "intersection.txt"

def get_name_list():
    return_array = []
    if os.path.exists(input_file):
        with io.open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                if line is not None:
                    line = line.strip()
                    return_array.append(line)
    return return_array


if __name__ == '__main__':
    consumer_key, consumer_secret, access_token, access_token_secret = get_account_credentials()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)
    print "Signing in as: "+auth_api.me().name
    queried = 0
    threshold = 20
    max = 100

    name_list = get_name_list()
    follower_list = {}
    for name in name_list:
        if queried > max:
            break
        print "Getting followers for " + name
        followers = auth_api.followers_ids(name)
        filename = "top-100-bot-search/" + name + ".txt"
        print "Writing: " + filename
        handle = open(filename, 'w')
        for twid in followers:
            handle.write(str(twid) + "\n")
        handle.close
        for twid in followers:
            if twid in follower_list:
                follower_list[twid] += 1
            else:
                follower_list[twid] = 1
        queried += 1
        filename = "top-100-bot-search/serialized.txt"
        print "Writing: " + filename
        handle = open(filename, 'w')
        json.dump(follower_list, handle, indent=4)
        handle.close()
        time.sleep(65)
