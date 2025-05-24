#This will be the test file for Instagram
import os
import requests
from dotenv import load_dotenv

ENV_PATH = ".env/instagram.env"
IMAGE_URL = "https://raw.githubusercontent.com/SirAlexus1811/PostAPI-Testdata/main/test.jpg"
CAPTION = "My first test Post on Instagram via Graph-API !"
#https://github.com/SirAlexus1811/PostAPI-Testdata/blob/main/test.jpg
#Load env file if it exists
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)

#Get access token and instagram id
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or input("Access Token: ").strip()
IG_ID = os.getenv("IG_ACC_ID") or input("Instagram Account ID: ").strip()

#Create Upload URL
upload_url = f"https://graph.instagram.com/v22.0/{IG_ID}/media"
payload = {
    "image_url": IMAGE_URL,
    "caption": CAPTION,
    "access_token": ACCESS_TOKEN
}

#Create Response
response = requests.post(upload_url, data=payload)
response_data = response.json()
print(response_data)

if "id" in response_data:
    media_id = response_data["id"]

    #Pulish Post
    publish_url = f"https://graph.instagram.com/v22.0/{IG_ID}/media_publish"
    publish_payload = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN
    }

    publish_response = requests.post(publish_url, data=publish_payload)
    print(publish_response.json())
else:
    print("DEBUG: Error while uploading a picture.")
