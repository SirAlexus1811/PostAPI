import logging
#from numpy import info

class instaGnome:
    def __init__(self, number, env_handler, git_handler):
        self.number = number
        self.env_handler = env_handler
        self.git_handler = git_handler

    def post(self, account, cap, media, mtype, location):
        #Posting Logic here, with use of account info etc
        logging.info("GNOME "+ str(self.number) + ": Posting to Instagram account: " + account + " started!")
        
        logging.info("GNOME "+ str(self.number) + ": Checking posting information...")
        
        #Check cap and media
        if not cap or not media:
            logging.error("UI: Caption or Image path is empty.")
            #Fix: Create pop-up maybe with error message
            #tk.Label(self.content_frame, text="Please fill in both fields.", fg="red").pack(pady=5)
            return
        
        #Check media type
        if mtype == "image":
            if not media.lower().endswith(('.jpg', '.jpeg')):
                #Fix the same as above with pop-up
                #tk.Label(self.content_frame, text="Please select a picture that is a .jpg or .jpeg!", fg="red").pack(pady=5)
                logging.error("GNOME "+ str(self.number) + ": Selected media is not a valid image file.")
                return
        elif mtype == "video":
            if not media.lower().endswith((".mp4", ".mov")):
                #Same as above again with pop-up
                #tk.Label(self.content_frame, text="Please select a video, that is a .mp4 or .mov!", fg="red").pack(pady=5)
                logging.error("GNOME "+ str(self.number) + ": Selected media is not a valid video file.")
                return
        
        #Check if a valid account was given
        if not account:
            logging.warning("GNOME "+ str(self.number) + ": No Accounts selected!")
            return
        
        logging.info("GNOME "+ str(self.number) + f": Posting information: '{media}' with cap '{cap}' on account '{account["username"]}'. Starting posting process...")
        
        #Actual posting logic here; no posting loop needed because one gnome only posts for one account (in a thread)
        
        