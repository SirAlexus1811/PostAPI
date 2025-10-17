from fileinput import filename
import logging
import os
import shutil
import requests
import time

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
        self.env_handler.load(".env_program/instagram.env")

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
    def uploadPicture2Git(self, filepath):
        #Set IMAGE_URL_LOCAL from Filepath
        self.IMAGE_URL_LOCAL = filepath
        
        #Repo Config
        self.env_handler.load(".env_program/git.env")  # Ensure the environment is loaded before initializing GitHandler
        repo_path = self.env_handler.get("REPO_PATH")
        git_username = self.env_handler.get("GIT_USERNAME")
        git_email = self.env_handler.get("GIT_EMAIL")
        filename = os.path.basename(self.IMAGE_URL_LOCAL)
        
        #Debug Message
        logging.info(f"INSTAGRAM_POSTER: Loaded Values from git.env - Repo: {repo_path}, User: {git_username}, Email: {git_email}, Filename: {filename}")
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
    def create_Up_URL(self, media_type):
        #Create Upload Url
        url = f"https://graph.instagram.com/v24.0/{self.ig_id}/media"
        if media_type == "image":
            logging.info("INSTAGRAM_POSTER: Creating upload URL for image...")
            params = {
                "image_url": self.GIT_URL,
                "caption": self.CAPTION,
                "access_token": self.access_token
            }
        elif media_type == "video":
            logging.info("INSTAGRAM_POSTER: Creating upload URL for video...")
            params = {
                "media_type": "REELS",
                "share_to_feed": "true",
                "video_url": self.GIT_URL,
                "caption": self.CAPTION,
                "access_token": self.access_token
            }
        else:
            logging.error("INSTAGRAM_POSTER: Invalid media type specified for upload URL creation.")
            raise ValueError("Invalid media type specified. Must be 'image' or 'video'.")
        
        #Create Response returns the IG_ID
        response = requests.post(url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error creating upload URL: {response.text}")
            raise Exception(f"Error creating upload URL: {response.text}")
        #Return and save to env file
        #self.env_handler.setV(", self.ig_id) #given ID is not IG ID its media ID
        #self.env_handler.save()  # Save the updated environment variables
        #Grab Media ID and Uri; Uri needed for videos
        container_id = response.json().get("id")
        container_uri = response.json().get("uri")
        logging.info(f"INSTAGRAM_POSTER: Created upload URL successfully. Media ID: {container_id}, URI: {container_uri}")
        return container_id, container_uri
    
    #Insert Logging operations here
    def wait_for_media_ready(self, creation_id, timeout=120, poll_interval=5):
        url = f"https://graph.instagram.com/v24.0/{creation_id}"
        params = {
            "fields": "status_code",
            "access_token": self.access_token
        }
        logging.info("INSTAGRAM_POSTER: Waiting for media to be ready...")
        waited = 0
        while waited < timeout:
            response = requests.get(url, params=params)
            data = response.json()
            status = data.get("status_code")
            if status == "FINISHED":
                return True
            #else:
                #raise Exception(f"Media not ready yet: {data}")
            time.sleep(poll_interval)
            waited += poll_interval
        raise TimeoutError("Media was not ready after waiting. Media Upload may take longer or failed.")

    def postPicOnInstagram(self):
        #Prepare Upload and get media ID; media uri not needed for pictures
        conatiner_id, conatiner_uri = self.create_Up_URL("image")
        if not conatiner_id:
            logging.error("INSTAGRAM_POSTER: Got no Media-ID, Abortion.")
            return False

        #Publish Media
        publish_url = f"https://graph.instagram.com/v24.0/{self.ig_id}/media_publish"
        params = {
            "creation_id": conatiner_id,
            "access_token": self.access_token
        }
        response = requests.post(publish_url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error publishing: {response.text}")
            raise Exception(f"Error publishing: {response.text}")

        logging.info(f"INSTAGRAM_POSTER: Post published successfully! (Picture) Response: {response.json()}")
        return response.json()
    
    def postReelOnInstagram(self):
        #Create Container with create_up_url
        container_id, container_uri = self.create_Up_URL("video")
        if not container_id: #CONTAINER_URI ONLY NEEDED FOR RESUMABLE SESSION
            logging.error("INSTAGRAM_POSTER: Got no Media-ID or URI, Abortion.")
            return False
        
        ##ONLY NEEDED FOR RESUMABLE SESSION
        #Upload the Video
        #video_path = self.GIT_URL
        #file_size = os.path.getsize(video_path)
        #headers = {
         #   "Authorization": f"OAuth {self.access_token}",
          #  "file_url": video_path
            #"offset": "0",
            #"file_size": str(file_size),
            #"--data-binary": str(video_path)
        #}
        #Open the video and read bytes
        #with open(video_path, "rb") as f:
        #    video_data = f.read()
        #upload_url = container_uri      #f"https://rupload.facebook.com/ig-api-upload/v24.0/{media_id}"
        
        #upload_response = requests.post(upload_url, headers=headers)
        #if upload_response.status_code != 200:
        #    logging.error(f"Error uploading the video: {upload_response.text}")
        #   return False
        
        #Status checkup
        try:
            self.wait_for_media_ready(container_id)
        except Exception as e:
            logging.error(f"Error at status checkup: {e}")
            return False
        
        #Publish the Reel
        publish_url = f"https://graph.instagram.com/v24.0/{self.ig_id}/media_publish"
        params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        response = requests.post(publish_url, params=params)
        if response.status_code != 200:
            logging.error(f"INSTAGRAM_POSTER: Error publishing: {response.text}")
            raise Exception(f"Error publishing: {response.text}")

        logging.info(f"INSTAGRAM_POSTER: Reel published successfully! Response: {response.json()}")
        return response.json()