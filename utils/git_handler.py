import os
import logging
from git import Repo, GitCommandError

#Githandler working without the env handler
class GitHandler:
    # Initialize the GitHandler with the environment handler
    def __init__(self, git_user, git_mail, repo_path):
        self.repo_path = repo_path
        self.git_username = git_user 
        self.git_mail = git_mail
        if not self.repo_path:
            logging.error("GIT_HANDLER: REPO_PATH not found in environment variables.")
            raise ValueError("REPO_PATH not found!")
        self.repo = Repo(self.repo_path)
        self.set_git_config()

    # Set Git Username and Email from environment variables
    def set_git_config(self):
        if self.git_username and self.repo.config_reader().get_value("user", "name", None) != self.git_username:
            self.repo.config_writer().set_value("user", "name", self.git_username).release()
            logging.info(f"GIT_HANDLER: Git username set to {self.git_username}")
        if self.git_mail and self.repo.config_reader().get_value("user", "email", None) != self.git_mail:
            self.repo.config_writer().set_value("user", "email", self.git_mail).release()
            logging.info(f"GIT_HANDLER: Git email set to {self.git_mail}")

    #Sets a new Username+
    def set_git_username(self, username):
        self.git_username = username
        self.set_git_config()

    #Sets a new Email
    def set_git_email(self, email):
        self.git_mail = email
        self.set_git_config()

    #Sets a new Repo Path
    def set_repo_path(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)
        self.set_git_config()

    #Get Rawlink - Only needs filename as parameter
    def get_raw_url(self, filename):
        return f"https://raw.githubusercontent.com/{self.git_username}/{self.get_remote_repo_name()}/{self.get_current_branch()}/{filename}"

    # Get the current branch name
    def get_current_branch(self):
        try:
            branch_name = self.repo.active_branch.name
            logging.info(f"GIT_HANDLER: Current branch is '{branch_name}'")
            return branch_name
        except Exception as e:
            logging.error(f"GIT_HANDLER: Error getting current branch: {e}")
            return None

    #Get Repo Name
    def get_remote_repo_name(self):
        try:
            url = self.repo.remotes.origin.url
            #Example: 'https://github.com/USER/REPO.git'
            repo_name = url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            return repo_name
        except Exception as e:
            logging.error(f"GIT_HANDLER: Error getting remote repo name: {e}")
            return None

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