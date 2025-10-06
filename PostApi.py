#Here will be the starter for this Program
#Import UI
from Ui.main_ui import PostAPIApp

#Import for global Env_Handler
from utils.env_handler import EnvHandler

#Import for global Git_Handler
from utils.git_handler import GitHandler

#Import for global Instagram_Poster
from Instagram.post.insta_post import instagram_poster

#Logging imports
from utils.tkinter_log_handler import TkinterLogHandler
import logging

#For Requirements checking
import os
import importlib.util

#Temp For Debug Purposes
#import sys
#print("\n".join(sys.path))

#Controller for the PostAPI application
class PostAPIController:
    debug_handler = None  # Placeholder for debug handler
    env_handler = None  # Placeholder for environment handler
    git_handler = None  # Placeholder for git handler
    instagram_poster = None  # Placeholder for Instagram poster

    def __init__(self):
        # Initialize Handlers, Posters and Logger
        self.startLogger()
        self.checkRequirements()
        self.startEnvHandler()
        self.startGitHandler()
        self.startInstagramPoster()
        
    #Starts the logger - Will be called on start
    def startLogger(self):
    # === Start Logger ===
        self.debug_handler = TkinterLogHandler(None)  # Initialize with None, will be set later (Text_widget in UI)
        self.debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging.getLogger().addHandler(self.debug_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Ctr: Hello PostAPI!")
        logging.info("Ctr: Started Logger")

    #Start Env_Handler
    def startEnvHandler(self):
        # Create an instance of the EnvHandler class
        self.env_handler = EnvHandler(".env_program/settings.env")
        # Debug Message
        logging.info("Ctr: EnvHandler started with env path: {}".format(self.env_handler.env_fPath))

    #Start Git_Handler
    def startGitHandler(self):
        if self.env_handler is not None:
            self.env_handler.load(".env_program/git.env")  # Ensure the environment is loaded before initializing GitHandler
        else:
            logging.error("Ctr: EnvHandler is not initialized before GitHandler!")
            raise RuntimeError("EnvHandler must be initialized before GitHandler.")
        self.git_handler = GitHandler(
            git_user=self.env_handler.get("GIT_USERNAME"),
            git_mail=self.env_handler.get("GIT_EMAIL"),
            repo_path=self.env_handler.get("REPO_PATH")
        )
        #Debug Message
        logging.info("Ctr: GitHandler started with repo path: {}".format(self.git_handler.repo_path))

    #Start Instagram Poster
    def startInstagramPoster(self):
        # Create an instance of the instagram_poster class
        self.instagram_poster = instagram_poster(self.env_handler, self.git_handler)
        # Debug Message
        logging.info("Ctr: Instagram Poster started")

    # Runs the main application loop
    def run(self):
        app = PostAPIApp(self.debug_handler, controller=self)
        def on_close():
            TkinterLogHandler.save_log_history()
            app.destroy()
        app.protocol("WM_DELETE_WINDOW", on_close)
        app.mainloop()

    def checkRequirements(self):
        # This function can be used to check if all requirements are met
        logging.info("Ctr: Checking requirements...")
        requirements_path = "requirements.txt"
        missing = []
        # Mapping requirements.txt -> Importname
        pkg_import_map = {
            "python-dotenv": "dotenv",
            "Flask": "flask",
            "gitpython": "git",
            "numpy": "numpy",
            "requests": "requests",
            "tk": "tkinter",
            "tkinter": "tkinter"
        }
        if not os.path.exists(requirements_path):
            logging.warning("Ctr: requirements.txt not found!")
            return

        with open(requirements_path) as req_file:
            for line in req_file:
                pkg = line.strip()
                if not pkg or pkg.startswith("#"):
                    continue
                import_name = pkg_import_map.get(pkg, pkg.split("[")[0].replace("-", "_"))
                # Tkinter is a special case, as it is not installed via pip
                try:
                    if import_name == "tkinter":
                        import tkinter
                    else:
                        importlib.import_module(import_name)
                except ImportError:
                    missing.append(pkg)

        if missing:
            logging.warning(f"Ctr: Missing pakages: {', '.join(missing)}")
            print(f"Please install all missing pakages with: pip install -r requirements.txt")
        else:
            logging.info("Ctr: All requirements are installed :).")

#Main function to start the application
if __name__ == "__main__":
    Controller = PostAPIController()
    Controller.run()
