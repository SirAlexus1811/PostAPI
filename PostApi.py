#Here will be the starter for this Program
#Import UI
from Ui.main_ui import PostAPIApp

#Import for global Env_Handler
from utils.env_handler import EnvHandler

#Logging imports
from utils.tkinter_log_handler import TkinterLogHandler
import logging

#For Requirements checking
import os
import importlib.util

#Controller for the PostAPI application
class PostAPIController:
    debug_handler = None  # Placeholder for debug handler
    env_handler = None  # Placeholder for environment handler

    def __init__(self):
        # Initialize the logger
        self.env_handler = EnvHandler(".env/settings.env")  # Load environment variables from .env file
        self.startLogger()
        self.checkRequirements()
        
    #Starts the logger - Will be called on start
    def startLogger(self):
    # === Start Logger ===
        self.debug_handler = TkinterLogHandler(None)  # Initialize with None, will be set later (Text_widget in UI)
        self.debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging.getLogger().addHandler(self.debug_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Ctr: Hello PostAPI!")
        logging.info("Ctr: Started Logger")

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
