from fileinput import filename
import logging
import os
import shutil
import requests

class instagram_poster:
    CAPTION = "" # Placeholder; will be set in init()
    IMAGE_URL_LOCAL = "" # Will be set through url-func
    GIT_URL = "" # Here the github rawusercontent link will be safed by the func
    response_id = "" # Will be Used

    #Envhandler will be given with correct loaded environment -> UI will do this 
    def __init__(self, env_handler, git_handler):
        self.env_handler = env_handler
        self.git_handler = git_handler

        #Load correct instagram.env
        self.env_handler.load(".env/instagram.env")

        self.access_token = self.env_handler.get("ACCESS_TOKEN")
        self.ig_id = self.env_handler.get("IG_ACC_ID")
        if not self.access_token or not self.ig_id:
            logging.error("INSTAGRAM_POSTER: ACCESS_TOKEN or IG_ACC_ID not found in environment variables.")
            raise ValueError("ACCESS_TOKEN or IG_ACC_ID not found!")

    #Sets Picture related variables
    def setupPost(self, caption, img_path):
        self.CAPTION = caption
        self.IMAGE_URL_LOCAL = img_path

    #Set ig_id
    def setIG_ID(self, ig_id):
        self.ig_id = ig_id
    
    #Set access token
    def setAT(self, access_token):
        self.access_token = access_token

    #This Function will mvoe the picture from the UI into the git and creates (maybe return) the rawgithubusercontent link
    def uploadPicture2Git(self):
        #Repo Config
        self.env_handler.load(".env/git.env")  # Ensure the environment is loaded before initializing GitHandler
        repo_path = self.env_handler.get("REPO_PATH")
        git_username = self.env_handler.get("GIT_USERNAME")
        git_email = self.env_handler.get("GIT_EMAIL")
        filename = os.path.basename(self.IMAGE_URL_LOCAL)
        #Branch Selection not added yet
        #branch = "main"  # Default branch, can be changed if needed -> There will be an Option in UI later on

        if not repo_path or not git_username or not git_email:
            logging.error("INSTAGRAM_POSTER: REPO_PATH, GIT_USERNAME or GIT_EMAIL not found in environment variables.")
            raise ValueError("REPO_PATH, GIT_USERNAME or GIT_EMAIL not found!")
        
        #Create Target Path and copy the image into the repo
        target_path = os.path.join(repo_path, filename)
        shutil.copy2(self.IMAGE_URL_LOCAL, target_path)

        #Use Githandler Instance
        self.git_handler.set_repo_path(repo_path)
        self.git_handler.set_git_username(git_username)
        self.git_handler.set_git_email(git_email)
        self.git_handler.set_git_config() #Must be run in order to update the repo_config in git

        #Ceckout main branch or else it will be inconsistend and will not work
        self.git_handler.checkout_branch("main")

        #File should already be copied to destination
        #Add all changes, commit and push to main - Branch selection not added yet
        self.git_handler.add_all_changes()
        self.git_handler.commit_changes(f"Add image for Instagram post: {filename}")
        self.git_handler.push_changes("main")

        logging.info("INSTAGRAM_POSTER: Picture moved to Repo and pushed!")

        #Create and get Rawlink to save
        self.raw_url = self.git_handler.get_raw_url(filename)
        self.GIT_URL = self.raw_url

        #Debug Message
        self.git_handler.dump_git_status()  # Optional: Dump git status for debugging
        logging.info(f"INSTAGRAM_POSTER: Uploaded Picture to Git, Raw-Link: {self.raw_url}")

    #Creates the Upload Url
    def create_Up_URL(self):
        #Create Upload Url
        url = f"https://graph.instagram.com/v22.0/{self.ig_id}/media"
        params = {
            "image_url": self.GIT_URL,
            "caption": self.CAPTION,
            "access_token": self.access_token
        }
        #Create Response returns the IG_ID
        response = requests.post(url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error creating upload URL: {response.text}")
            raise Exception(f"Error creating upload URL: {response.text}")
        #Return and save to env file
        self.env_handler.setV("IG_ACC_ID", self.ig_id)
        self.env_handler.save()  # Save the updated environment variables
        return response.json().get("id")
    
    def postOnInstagram(self):
        #Prepare Upload and get media ID
        media_id = self.create_Up_URL()
        if not media_id:
            logging.error("INSTAGRAM_POSTER: Got no Media-ID, Abortion.")
            return False

        #Publish Media
        publish_url = f"https://graph.instagram.com/v22.0/{self.ig_id}/media_publish"
        params = {
            "creation_id": media_id,
            "access_token": self.access_token
        }
        response = requests.post(publish_url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error publishing: {response.text}")
            raise Exception(f"Error publishing: {response.text}")

        logging.info(f"INSTAGRAM_POSTER: Post published successfully! Response: {response.json()}")
        return response.json()