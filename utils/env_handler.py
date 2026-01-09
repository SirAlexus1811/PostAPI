#No need for dotenv anymore lol

import os
import logging # For Logging Handler

class EnvHandler:
    def __init__(self, env_fPath):
        self.env_fPath = env_fPath
        self.env = {} # Dictionary to load whole env into and return asked values
        self.load()

    #returns the value of the key if it exists, otherwise returns default
    def get(self, key, default=None):
        return self.env.get(key, default)

    #Load an Env file from a dictionary
    def load(self, env_fPath=None):
        if env_fPath:
            self.env_fPath = env_fPath
        self.env = {}
        if os.path.exists(self.env_fPath):
            try:
                with open(self.env_fPath, "r") as f:
                    for line in f:
                        if "=" in line and not line.strip().startswith("#"):
                            key, value = line.strip().split("=", 1)
                            self.env[key] = value
                logging.info(f"ENV_HANDLER: Loaded {self.env_fPath}")
            except Exception as e:
                logging.error(f"ENV_HANDLER: Error loading {self.env_fPath}: {e}")

    def setV(self, key, new_keyvalue):
        old_value = self.env.get(key)
        self.env[key] = new_keyvalue
        self.save()
        if old_value == new_keyvalue:
            logging.info(f"ENV_HANDLER: {key} already correct in env file. No changes made.")
        elif old_value is not None:
            logging.info(f"ENV_HANDLER: {key} updated from {old_value} to {new_keyvalue}.")
        else:
            logging.info(f"ENV_HANDLER: Added {key} with value: {new_keyvalue}")

    def save(self):
        try:
            with open(self.env_fPath, "w") as f:
                for key, value in self.env.items():
                    f.write(f"{key}={value}\n")
            logging.info(f"ENV_HANDLER: Saved {self.env_fPath}")
        except Exception as e:
            logging.error(f"ENV_HANDLER: Error saving {self.env_fPath}: {e}")