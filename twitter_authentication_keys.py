import sys
import re
import io
import os
import random

def strip_quotes(string):
    if string[1] == "\"" and string[-1] == "\"":
        return string[1:-1]
    else:
        return string

def read_account_file(filepath):
    owner = None
    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None
    print "Reading key file: " + filepath
    with io.open(filepath, "r", encoding = "utf-8") as file:
        for line in file:
            if line is not None:
                line = line.strip()
                if re.search("^.+\=.+$", line):
                    key, value = line.split("=")
                    key = key.strip()
                    value = value.strip()
                    if key == "owner":
                        owner = strip_quotes(value)
                    if key == "consumer_secret":
                        consumer_secret = strip_quotes(value)
                    if key == "consumer_key":
                        consumer_key = strip_quotes(value)
                    if key == "access_token":
                        access_token = strip_quotes(value)
                    if key == "access_token_secret":
                        access_token_secret = strip_quotes(value)
    if owner is not None and consumer_key is not None and  consumer_secret is not None and  access_token is not None and  access_token_secret is not None:
        return [owner, consumer_key, consumer_secret, access_token, access_token_secret]
    else:
        return None

def read_account_keys():
    accounts = {}
    keys_dir = "keys"
    for path, dirs, files in os.walk(keys_dir):
        for filename in files:
            if "DS_Store" not in filename:
                filepath = os.path.join(path, filename)
                details = read_account_file(filepath)
                if details is not None:
                    owner = details[0]
                    accounts[owner] = {}
                    accounts[owner]["consumer_key"] = details[1]
                    accounts[owner]["consumer_secret"] = details[2]
                    accounts[owner]["access_token"] = details[3]
                    accounts[owner]["access_token_secret"] = details[4]
    return accounts

def get_account_credentials():
# read in accounts from keys directory
    accounts = read_account_keys()
    available_accounts = []
    for name, data in accounts.iteritems():
        available_accounts.append(name)
    if len(available_accounts) < 1:
        print "No accounts available to sign on with..."
        sys.exit(0)
    else:
        print "Found pool of " + str(len(available_accounts)) + " accounts."
        print available_accounts

# randomly choose an available account to start the stream on
    chosen = random.randint(0, len(available_accounts) - 1)
    print "Rolling dice... Got " + str(chosen)
    acct_name = available_accounts[chosen]
    consumer_key = accounts[acct_name]["consumer_key"]
    consumer_secret = accounts[acct_name]["consumer_secret"]
    access_token = accounts[acct_name]["access_token"]
    access_token_secret = accounts[acct_name]["access_token_secret"]
    return consumer_key, consumer_secret, access_token, access_token_secret
