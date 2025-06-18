import tkinter as tk
from tkinter import ttk

#for safing settings
from dotenv import dotenv_values, load_dotenv
from utils.env_handler import update_env_entry
from utils.git_handler import ENV_PATH as GIT_ENV_PATH

#Env Path Settings
SETTINGS_ENV_PATH = ".env/settings.env"

class PostAPIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Post API App")
        self.geometry("900x600")

        # === Main Container Frame ===
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # === Left Menu ===
        self.menu_frame = tk.Frame(self.container, bg="#ddd", width=100)
        self.menu_frame.pack(side="left", fill="y")

        self.content_frame = tk.Frame(self.container, bg="#fff")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # === Menü-Buttons ===
        self.buttons = []
        menu_items = [
            ("1. Einstellungen", self.show_settings),
            ("2. Instagram", self.show_instagram),
            ("3. TikTok", self.show_tiktok),
            ("4. Automatisierung", self.show_automation),
            ("5. Credits", self.show_credits)
        ]

        for text, command in menu_items:
            btn = tk.Button(self.menu_frame, text=text, command=command, height=2)
            btn.pack(fill="x")
            self.buttons.append(btn)

        # === Startansicht ===
        self.show_settings()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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

        tk.Button(self.content_frame, text="Save Git Settings", command=self.save_settings_GIT).pack(pady=10)

        #Debug Box
        frame_debug = tk.Frame(self.content_frame)  # New frame for debug settings
        frame_debug.pack(pady=5)

        tk.Label(frame_debug, text="Debug Settings:", font=("Arial", 14)).pack()
        self.debug_var = tk.BooleanVar(value=(dotenv_values(SETTINGS_ENV_PATH).get("DEBUG_MODE") == "True"))
        debug_cb = tk.Checkbutton(frame_debug, text="Activate Debug-Mode", variable=self.debug_var)
        debug_cb.pack(pady=10)

        tk.Button(self.content_frame, text="Save Debug Settings", command=lambda: update_env_entry(SETTINGS_ENV_PATH, "DEBUG_MODE", str(self.debug_var.get()))).pack(pady=10)

    def show_instagram(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Instagram Post-Manager", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.content_frame, text="Access Token:").pack()
        self.ig_token_entry = tk.Entry(self.content_frame)
        self.ig_token_entry.pack()

        tk.Label(self.content_frame, text="Bild-URL:").pack()
        self.ig_image_entry = tk.Entry(self.content_frame)
        self.ig_image_entry.pack()

        tk.Label(self.content_frame, text="Account Auswahl:").pack()
        self.ig_account_list = ttk.Combobox(self.content_frame, values=["Account 1", "Account 2"])
        self.ig_account_list.pack()

        tk.Button(self.content_frame, text="Bild posten", command=self.post_image).pack(pady=10)

    def show_tiktok(self):
        self.clear_content()
        tk.Label(self.content_frame, text="TikTok (in Entwicklung)", font=("Arial", 18)).pack(pady=10)

    def show_automation(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Automatisierung (geplant)", font=("Arial", 18)).pack(pady=10)

    def show_credits(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Credits", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.content_frame, text="Autor: Siralexus\nEmail: alexgeschaeftlich@posteo.com").pack(pady=20)

    # === Functions ===
    def save_settings_GIT(self):
        git_username = self.git_user_entry.get()
        git_email = self.git_email_entry.get()
        if git_username and git_email:
            # Update the .env file with the new Git settings; no need to check if they are already set as the function will handle that
            update_env_entry(GIT_ENV_PATH, "GIT_USERNAME", git_username)
            update_env_entry(GIT_ENV_PATH, "GIT_EMAIL", git_email)
            tk.Label(self.content_frame, text=f"Git settings safed: {git_username}, {git_email}").pack()
        else:
            tk.Label(self.content_frame, text="Please Enter something.").pack()

    def post_image(self):
        token = self.ig_token_entry.get()
        image_url = self.ig_image_entry.get()
        account = self.ig_account_list.get()
        print(f"Poste Bild an {account} mit URL {image_url} und Token {token}")


if __name__ == "__main__":
    app = PostAPIApp()
    app.mainloop()