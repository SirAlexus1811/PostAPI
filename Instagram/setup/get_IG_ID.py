import os
from xmlrpc.client import ResponseError
import requests                     #Used to send get request to GRAPH API
from urllib.parse import urlencode  #Makes the URL request for GRAPH API
from dotenv import load_dotenv      #Loads the env file

#selfmade handlers
from utils.env_handler import EnvHandler

#Path to .env File for Instagram
ENV_PATH = ".env/instagram.env"

#Load env if it exists
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)

#Get existing Data; when it does not exist it asks for it on the command line
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or input("Access Token: ").strip()
#FB_PAGE_ID = os.getenv("FB_PAGE_ID") or input ("Facebook Page ID: ").strip()
#This FB Page id will be asked in first request.

env_handler = EnvHandler(ENV_PATH)

#Make URL with selected params (selection will be added later)
BASE_URL = f"https://graph.instagram.com/v22.0/me"
PARAMS = {
    "fields": "id,name",
    "access_token": ACCESS_TOKEN
}
FULL_URL = BASE_URL + "?" + urlencode(PARAMS);

#Sent the request via requests to the GRAPH API to get .json block with PARAMS
response = requests.get(FULL_URL)

dataToProcess = response.json()
#print(response.url)
print(response.json())

#Look if ID is in the response
if "id" in dataToProcess:
    ig_id = dataToProcess["id"] #save id
    print("DEBUG: Found IG_ID!")

    env_handler.setV("IG_ACC_ID", ig_id)
    print("DEBUG: ENV UPDATED!")

    #Open Env File as f to read the lines from it
#    with open(ENV_PATH, "r") as f:
#        lines = f.readlines()
#        f.close()
    
    #Look if IG_ID already existing
#    if not any(line.startswith("IG_ACC_ID=") for line in lines):
#        #open with all rights as env_file
#        with open(ENV_PATH, "a") as env_file:
#            env_file.write(f"\nIG_ACC_ID={ig_id}")
#        print("DEBUG: Added IG_ACC_ID!")
