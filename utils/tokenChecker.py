#from operator import is_
#from urllib import response
import concurrent.futures
import requests
import threading
#import json
import logging

#Mainly checks and extends all tokens in a account list (json file)
class TokenChecker:
    def __init__(self, accounts, callback, maxworkers=5):
        self.accounts = accounts
        self.callback = callback
        self.max_workers = maxworkers
        
    def renew_all_tokens(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        for idx, acc in enumerate(self.accounts):
            executor.submit(self.renew_token, idx, acc)
        
    def check_all_tokens(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        for idx, acc in enumerate(self.accounts):
            executor.submit(self.check_token, idx, acc)
        
    #Renews token via a get request to Graph API
    def renew_token(self, idx, acc):
        token = acc.get("token", "")
        url = "https://graph.instagram.com/refresh_access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": token
        }
        data = "" # So it wont be unbound
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            logging.info(f"TC: Renewed token for account {acc.get('username', idx)}: Response: {data}")
            is_renewed = True and "error" not in data
        except Exception as e:
            is_renewed = False
            logging.error(f"TC: Error renewing token for account {acc.get('username', idx)}: {e}")
            
        #Callback back to UI
        self.callback(idx, is_renewed, data)
    
    #Checks Token via a get request to Graph API
    def check_token(self, idx, acc):
        token = acc.get("token", "")
        ig_id = acc.get("IG_ID", "")
        url=f"https://graph.instagram.com/v24.0/{ig_id}"
        params = {
            "fields": "id",
            "access_token": token
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            logging.info(f"TC: Checked token for account {acc.get('username', idx)}: Response: {data}")
            is_valid = "id" in data and "error" not in data
            acc["Status"] = "✔" if is_valid else "✖"
            
        except Exception as e:
            is_valid = False
            logging.error(f"TC: Error checking token for account {acc.get('username', idx)}: {e}")
            
        #Callback back to UI
        self.callback(idx, is_valid)