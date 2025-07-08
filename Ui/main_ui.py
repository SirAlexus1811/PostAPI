#from doctest import debug
import tkinter as tk
from tkinter import ttk

#for safing settings
from dotenv import dotenv_values, load_dotenv, set_key
from utils import env_handler
from utils.env_handler_OLD import update_env_entry
from utils.git_handler import ENV_PATH as GIT_ENV_PATH
import os # For Logfile saving and path handling

#For Logging
import logging

from utils.tkinter_log_handler import TkinterLogHandler

#Env Path Settings Not needed because first instance of env handler load this settings file
#SETTINGS_ENV_PATH = ".env/settings.env"

class PostAPIApp(tk.Tk):
    debug_handler = None  # Placeholder for debug handler

    def __init__(self, debug_handler, controller):
        super().__init__()
        self.title("Post API App")
        self.geometry("1200x800")

        #Set the given Attributes
        self.debug_handler = debug_handler
        self.controller = controller
        
        #Setup Env Handler
        if self.controller and hasattr(self.controller, "env_handler"):
            self.controller.env_handler.load(".env/settings.env")
        else:
            logging.error("UI: No valid Controller or env_handler passed!")
            raise ValueError("No valid Controller or env_handler passed!")
        
        # Set the icon if it exists
        icon_path = "assets/icon.ico"
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            logging.warning(f"UI: Icon file {icon_path} not found. Using default icon.")

        # === Main Container Frame ===
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # === Left Menu ===
        self.menu_frame = tk.Frame(self.container, bg="#ddd", width=100)
        self.menu_frame.pack(side="left", fill="y")

        self.content_frame = tk.Frame(self.container, bg="#fff")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.build_menu()

        # === Startpage ===
        self.show_Menu()

    def build_menu(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        
        # === Menü-Buttons ===
        self.buttons = []
        menu_items = [
            ("PostAPI Menu", self.show_Menu),  # Title
            ("1. How to Use", self.show_HowToUse),  # How to Use
            ("2. Settings", self.show_settings),
            ("3. Instagram", self.show_instagram),
            ("4. TikTok", self.show_tiktok),
            ("5. Client-Mode", self.show_client_mode),
            ("6. Credits", self.show_credits),
            ("7. Exit", self.exit_app)
        ]

        if self.controller.env_handler.get("DEBUG_MODE", "False").lower() in ("true", "1", "yes"):
            menu_items.append(("8. Debug", self.show_debug))

        for text, command in menu_items:
            btn = tk.Button(self.menu_frame, text=text, command=command, height=2)
            btn.pack(fill="x")
            self.buttons.append(btn)
        
        # Debug Message
        logging.info("UI: Built Menu")

    def clear_content(self):
        #Delete Logging-Handler if there is one exisiting
        if hasattr(self, "debug_handler"):
            if self.debug_handler is not None:
                self.debug_handler.set_widget(None)  # Clear the widget reference

        #Del all widgets in content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Debug Message
        logging.info("UI: Cleared Content Frame")

    def show_Menu(self):
        #Clear content and show the main menu
        self.clear_content()
        tk.Label(self.content_frame, text="PostAPI Menu", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.content_frame, text="Please select an option from the left menu.").pack(pady=10)

        #Debug Message
        logging.info("UI: Opened Main Menu")

    def show_HowToUse(self):
        #Clear content and show How to Use
        self.clear_content()
        tk.Label(self.content_frame, text="How to Use", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.content_frame, text="1. Setup this Program via the Settings Tab.\n"
                                          "2. Use the Instagram menu to post pictures and Videos on Instagram. (WIP)\n"
                                          "3. Use the TikTok menu to post pictures and videos on TikTok. (WIP)\n"
                                          "4. Use the Client-Mode to use a server instance of our server setups. (Very WIP)\n"
                                          "5. Check the Credits for author information.").pack(pady=10)

        #Debug Message
        logging.info("UI: Opened How to Use Page")

    def show_settings(self):
        #Load Dotenv and show existing settings
        git_username = dotenv_values(GIT_ENV_PATH).get("GIT_USERNAME") or ""
        git_email = dotenv_values(GIT_ENV_PATH).get("GIT_EMAIL") or ""

        self.clear_content()
        tk.Label(self.content_frame, text="Settings / Config", font=("Arial", 18)).pack(pady=10)

        # Git config
        tk.Label(self.content_frame, text="Git Settings:", font=("Arial", 14)).pack()
        #Git Username
        frame_user = tk.Frame(self.content_frame) # New frame for user git settings
        frame_user.pack(pady=5)

        tk.Label(frame_user, text="Git Username:", width=40).pack(side="left")
        self.git_user_entry = tk.Entry(frame_user, width=40)
        self.git_user_entry.insert(0, git_username)  # Set existing username
        self.git_user_entry.pack(side="left", padx=5)

        #Git Email
        frame_email = tk.Frame(self.content_frame)  # New frame for email git settings
        frame_email.pack(pady=5)

        tk.Label(frame_email, text="Git Email:", width=40).pack(side="left")
        self.git_email_entry = tk.Entry(frame_email, width=40)
        self.git_email_entry.insert(0, git_email)  # Set existing email 
        self.git_email_entry.pack(side="left", padx=5)

        # Local Repo Path
        frame_path = tk.Frame(self.content_frame)  # New frame for local repo path
        frame_path.pack(pady=5)

        tk.Label(frame_path, text="Local Repo Path:", width=40).pack(side="left")
        self.local_repo_entry = tk.Entry(frame_path, width=40)
        self.local_repo_entry.insert(0, dotenv_values(GIT_ENV_PATH).get("REPO_PATH") or "")  # Set existing local repo path
        self.local_repo_entry.pack(side="left", padx=5)

        # Save Button for Git Settings
        tk.Button(self.content_frame, text="Save Git Settings", command=self.save_settings_GIT).pack(pady=10)

        #Debug Box
        frame_debug = tk.Frame(self.content_frame)  # New frame for debug settings
        frame_debug.pack(pady=5)

        tk.Label(frame_debug, text="Debug Settings:", font=("Arial", 14)).pack()
        self.debug_var = tk.BooleanVar(value=(self.controller.env_handler.get("DEBUG_MODE") == "True"))
        debug_cb = tk.Checkbutton(frame_debug, text="Activate Debug-Mode", variable=self.debug_var)
        debug_cb.pack(pady=10)

        tk.Button(self.content_frame, text="Save Debug Settings", command=self.save_settings_DEBUG).pack(pady=10)

        #Message Box for Settings
        self.frame_message = tk.Frame(self.content_frame)  # New frame for message box
        self.frame_message.pack(pady=5)

        #Debug Message
        logging.info("UI: Opened Settings Page")

    def show_instagram(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Instagram Post-Manager", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.content_frame, text="Access Token:").pack()
        self.ig_token_entry = tk.Entry(self.content_frame)
        self.ig_token_entry.pack()

        tk.Label(self.content_frame, text="Local Picture-URL:").pack()
        self.ig_image_entry = tk.Entry(self.content_frame)
        self.ig_image_entry.pack()

        tk.Label(self.content_frame, text="Select Account:").pack()
        self.ig_account_list = ttk.Combobox(self.content_frame, values=["Account 1", "Account 2"])
        self.ig_account_list.pack()

        tk.Button(self.content_frame, text="Post Picture", command=self.post_image).pack(pady=10)

        # Debug Message
        logging.info("UI: Opened Instagram Page")

    def show_tiktok(self):
        self.clear_content()
        tk.Label(self.content_frame, text="TikTok (WIP)", font=("Arial", 18)).pack(pady=10)

        #Debug Message
        logging.info("UI: Opened TikTok Page (WIP)")

    def show_client_mode(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Client Mode (For Servers)", font=("Arial", 18)).pack(pady=10)

        #Debug Message
        logging.info("UI: Opened Client Mode Page (WIP)")

    def show_credits(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Credits", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.content_frame, text="Author: Siralexus\nEmail: alexgeschaeftlich@posteo.com").pack(pady=20)

        #Debug Message
        logging.info("UI: Opened Credits Page")

    def show_debug(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Debug-Infos", font=("Arial", 18)).pack(pady=10)
        self.debug_console = tk.Text(self.content_frame, height=20, width=80, state="normal", bg="#222", fg="#0f0")
        self.debug_console.pack(pady=10, fill="both", expand=True) # Expandable to fill the space
    
        # Log-Historie anzeigen
        self.debug_console.delete("1.0", "end")
        for msg in TkinterLogHandler.log_history:
            self.debug_console.insert("end", msg + "\n")
        self.debug_console.config(state="disabled")

        #Set Debug Console as widget for logging
        if self.debug_handler is not None:
            self.debug_handler.set_widget(self.debug_console)

        logging.info("UI: Opened Debug Console")

    # === Functions ===
    def save_settings_GIT(self):
        git_username = self.git_user_entry.get()
        git_email = self.git_email_entry.get()
        local_repo_path = self.local_repo_entry.get()
        if git_username and git_email and local_repo_path:
            # Update the .env file with the new Git settings; no need to check if they are already set as the function will handle that
            update_env_entry(GIT_ENV_PATH, "GIT_USERNAME", git_username)
            update_env_entry(GIT_ENV_PATH, "GIT_EMAIL", git_email)
            update_env_entry(GIT_ENV_PATH, "REPO_PATH", local_repo_path)
            # Remove previous messages
            for widget in self.frame_message.winfo_children():
              widget.destroy()
            tk.Label(self.frame_message, text=f"Git settings saved:\n{git_username}\n{git_email}\n{local_repo_path}\n").pack()
        else:
            tk.Label(self.frame_message, text="Please Enter something.").pack()

        # Debug Message
        logging.info("UI: Saved Git Settings")

    def save_settings_DEBUG(self):
        debug_mode = self.debug_var.get()
        self.controller.env_handler.setV("DEBUG_MODE", str(debug_mode))  # Save the debug mode setting
        #update_env_entry(SETTINGS_ENV_PATH, "DEBUG_MODE", str(debug_mode))
        # Remove previous messages
        for widget in self.frame_message.winfo_children():
            widget.destroy()
        tk.Label(self.frame_message, text=f"Debug mode set to: {debug_mode}").pack()
        self.build_menu()  # Rebuild the menu to reflect changes    

        #Debug Message
        logging.info("UI: Saved Debug Settings")

    #Exit Func
    def exit_app(self):
        logging.info("UI: Exiting Application")
        # Save log history before exiting
        TkinterLogHandler.save_log_history()
        self.quit()


    def post_image(self):
        token = self.ig_token_entry.get()
        image_url = self.ig_image_entry.get()
        account = self.ig_account_list.get()
        logging.info(f"UI: Poste Bild an {account} mit URL {image_url} und Token {token}")
