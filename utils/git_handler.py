import os
import logging
from git import Repo, GitCommandError

class GitHandler:
    # Initialize the GitHandler with the environment handler
    def __init__(self, env_handler):
        self.env_handler = env_handler
        self.repo_path = self.env_handler.get("REPO_PATH")
        if not self.repo_path:
            logging.error("GIT_HANDLER: REPO_PATH not found in environment variables.")
            raise ValueError("REPO_PATH not found!")
        self.repo = Repo(self.repo_path)
        self.set_git_config()

    # Set Git Username and Email from environment variables
    def set_git_config(self):
        git_username = self.env_handler.get("GIT_USERNAME")
        git_email = self.env_handler.get("GIT_EMAIL")
        if git_username and self.repo.config_reader().get_value("user", "name", None) != git_username:
            self.repo.config_writer().set_value("user", "name", git_username).release()
            logging.info(f"GIT_HANDLER: Git username set to {git_username}")
        if git_email and self.repo.config_reader().get_value("user", "email", None) != git_email:
            self.repo.config_writer().set_value("user", "email", git_email).release()
            logging.info(f"GIT_HANDLER: Git email set to {git_email}")

    # Create a new branch
    def create_branch(self, branch_name):
        try:
            self.repo.git.checkout("-b", branch_name)
            logging.info(f"GIT_HANDLER: Branch '{branch_name}' created and checked out.")
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error creating branch '{branch_name}': {e}")

    # Checkout an existing branch
    def checkout_branch(self, branch_name):
        try:
            self.repo.git.checkout(branch_name)
            logging.info(f"GIT_HANDLER: Branch '{branch_name}' checked out.")
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error checking out branch '{branch_name}': {e}")

    # Add all changes to the staging area
    def add_all_changes(self):
        try:
            self.repo.git.add(A=True)
            logging.info("GIT_HANDLER: All changes added to staging area.")
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error adding changes: {e}")

    #Commit changes func with message
    def commit_changes(self, commit_message):
        try:
            if not commit_message:
                commit_message = "No Commit Message Provided"
            self.repo.git.commit(m=commit_message)
            logging.info(f"GIT_HANDLER: Changes committed with message: '{commit_message}'")
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error committing changes: {e}")
        
    # Push changes to the remote repository
    def push_changes(self, branch_name):
        try:
            self.repo.git.push("origin", branch_name)
            logging.info(f"GIT_HANDLER: Changes pushed to branch '{branch_name}' successfully.")
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error pushing changes to branch '{branch_name}': {e}")
    
    #Dumps git status into log
    def dump_git_status(self):
        try:
            status = self.repo.git.status()
            logging.info(f"GIT_HANDLER: Git status: {status}")
            logging.info(status)
        except GitCommandError as e:
            logging.error(f"GIT_HANDLER: Error getting git status: {e}")