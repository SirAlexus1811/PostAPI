#Stop the freeze breeze with threading. Each PostGnome has its own thread
import threading
#import the GNOMESS
import Instagram.instaGnome as instaGnome
#import env and git handler so we can create one instance for one thread
from utils.env_handler import EnvHandler
from utils.git_handler import GitHandler
#Logging imports
import logging

class postGnomeController:
    def __init__(self):# env_handler, git_handler):
        #self.env_handler_single = env_handler # not needed cause we wont use a single gnome we'll always make at least 1 thread
        #self.git_handler_single = git_handler
        self.env_handlers = []
        self.git_handlers = []
        self.threads = []
        self.thread_status = {} # Dictionary to keep track of thread statuses, e.g., {thread_id: "running" or "finished"}
        
        '''
        Quick note for the statuses and later representation in UI:
        "0" = waiting;  "."
        "1" = running;  "~"
        "2" = finished; "✔"
        "3" = error;    "✖"
        '''
        
    def postingGnomeInsta(self, number, account, envH, gitH):
        gnome = instaGnome.instaGnome(number, envH, gitH)
        #Gnome Posting Logic here with call of post function etc
        
        pass
        
    #Called by UI to start the multiposting process for Instagram, creates threads for each posting gnome
    def multipost_instagram(self, accounts):
        #numerate accs in list and setup new instances of env and git handler for the gnome
        for idx, acc in enumerate(accounts):
            env_handler = EnvHandler(".env_program/settings.env")
            if env_handler is not None:
                env_handler.load(".env_program/git.env")  # Ensure the environment is loaded before initializing GitHandler
            else:
                logging.error("PGCtr: EnvHandler is not initialized before GitHandler!")
                raise RuntimeError("EnvHandler must be initialized before GitHandler.")
        
            git_handler = GitHandler(
                env_handler.get("GIT_USERNAME"),
                env_handler.get("GIT_EMAIL"),
                env_handler.get("REPO_PATH")
            )
            self.env_handlers.append(env_handler)
            self.git_handlers.append(git_handler)
            
            #Set thread status
            self.thread_status[idx] = "0" # waiting
            
            #Create and start the thread
            t = threading.Thread(
                target=self.postingGnomeInsta,
                args=(idx, acc, env_handler, git_handler)
            )
            t.start()
            self.threads.append(t)

    #Returns true or false wether there are still threads running, must be called by UI main window
    def wait_for_threads(self):
        