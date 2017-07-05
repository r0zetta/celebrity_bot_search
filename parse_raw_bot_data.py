import io
import os
import re
import pprint
import random
import time
import hashlib
import base64
import sys
import datetime

data_dir = "top-100-bot-search/"

def get_data():
    filename = data_dir + "raw-data-201706011805.txt"
    output_string = "ID | Screen_name | created_at | following | followers | tweets | default_profile | default_profile_image | follows_trump\n"
    bot_count = 0
    trump_count = 0
    if os.path.exists(filename):
        with open(filename) as f:
            lines = f.read().splitlines()
        for line in lines:
            twid, name, date, following, followers, tweets, def_profile, def_picture, follows_trump = line.split("|")
            if "21" in following and "0" in tweets and "Yes" in def_profile and "Yes" in def_picture:
                output_string += line + "\n"
                bot_count += 1
                if "Yes" in follows_trump:
                    trump_count += 1
    print output_string
    print "Found " + str(bot_count)
    print "Found " + str(trump_count) + " trump followers"

if __name__ == '__main__':
    get_data()

