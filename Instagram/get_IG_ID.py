import os
import requests                     #Used to send get request to GRAPH API
#import subprocess                   #Used for the curl command; now with requests
from urllib.parse import urlencode  #Makes the URL request for GRAPH API
from dotenv import load_dotenv      #Loads the env file

#Path to .env File for Instagram
ENV_PATH = "./.env/instagram.env"

#Load env if it exists
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)

#Get existing Data; when it does not exist it asks for it on the command line
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or input("Access Token: ").strip()
FB_PAGE_ID = os.getenv("FB_PAGE_ID") or input ("Facebook Page ID: ").strip()

#Make URL with selected params (selection will be added later)
BASE_URL = f"https://graph.facebook.com/v22.0/me"
PARAMS = {
    "fields": "id,name",
    "access_token": ACCESS_TOKEN
}
FULL_URL = BASE_URL + "?" + urlencode(PARAMS);

#Sent the request via requests to the GRAPH API to get .json block with PARAMS
response = requests.get(FULL_URL)
print(response.url)
print(response.json())