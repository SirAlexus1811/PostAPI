from fileinput import filename
import logging
import os
import shutil
import requests

import utils.git_handler_OLD as git_handler_OLD

class instagram_poster:
    CAPTION = "" # Placeholder; will be set in init()
    IMAGE_URL_LOCAL = "" # Will be set through url-func
    GIT_URL = "" # Here the github rawusercontent link will be safed by the func
    response_id = "" # Will be Used

    #Envhandler will be given with correct loaded environment -> UI will do this 
    def __init__(self, env_handler):
        self.env_handler = env_handler
        self.access_token = self.env_handler.get("ACCESS_TOKEN")
        self.ig_id = self.env_handler.get("IG_ACC_ID")
        if not self.access_token or not self.ig_id:
            logging.error("INSTAGRAM_POSTER: ACCESS_TOKEN or IG_ACC_ID not found in environment variables.")
            raise ValueError("ACCESS_TOKEN or IG_ACC_ID not found!")

    #Sets Picture related variables
    def setupPost(self, caption, img_path):
        self.CAPTION = caption
        self.IMAGE_URL_LOCAL = img_path

    #This Function will upload the picture from the UI into the git and creates (maybe return) the rawgithubusercontent link
    def uploadPicture2Git(self, local_URL):
        #Repo Config
        repo_path = self.env_handler.get("REPO_PATH")
        git_username = self.env_handler.get("GIT_USERNAME")
        git_email = self.env_handler.get("GIT_EMAIL")
        if not repo_path or not git_username or not git_email:
            logging.error("INSTAGRAM_POSTER: REPO_PATH, GIT_USERNAME or GIT_EMAIL not found in environment variables.")
            raise ValueError("REPO_PATH, GIT_USERNAME or GIT_EMAIL not found!")
        
        #Create Target Path and copy the image into the repo
        target_path = os.path.join(repo_path, filename := os.path.basename(local_URL))
        shutil.copy2(local_URL, target_path)

        #GitPython comes into play here -> Commit and Push the Picture
        repo = 


    def create_Up_URL(self):
        url = f"https://graph.instagram.com/v22.0/{self.ig_id}/media"
        params = {
            "image_url": self.GIT_URL,
            "caption": self.CAPTION,
            "access_token": self.access_token
        }
        response = requests.post(url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error creating upload URL: {response.text}")
            raise Exception(f"Error creating upload URL: {response.text}")
        return response.json().get("id")
    
    def verify_post(self):
        print("")