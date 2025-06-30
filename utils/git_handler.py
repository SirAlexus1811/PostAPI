#Simple Git handler that will be used to push imgs to the Postapi Storage Repo. GitPython will be used for this.
from git import Repo, GitCommandError
import os
from dotenv import load_dotenv
from utils.env_handler import update_env_entry
import logging #for the logging function in debug section

# Path to the .env file
ENV_PATH = ".env/git.env"

# Load the .env file if it exists
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)

#Setup Git Username and Email
GIT_USERNAME = os.getenv("GIT_USERNAME") or input("Git Username: ").strip()
GIT_EMAIL = os.getenv("GIT_EMAIL") or input("Git Email: ").strip()

# Path to git repo #OLD path.abspath(os.path.join(os.path.dirname(__file__), "../"))
#CAUTION: This path must point to the Repo outside the program folder. This is for posting purposes important, because the media will be uploaded into a cache repo and then posted.
REPO_PATH = os.getenv("REPO_PATH") or input("Path to Git Repository: ").strip()
repo = Repo(REPO_PATH)

# Set Local git config (not global)
def set_git_config():
    config_writer = repo.config_writer()
    changed = False

    try:
        if GIT_USERNAME and repo.config_reader().get_value("user", "name", None) != GIT_USERNAME:
            config_writer.set_value("user", "name", GIT_USERNAME)
            changed = True
            logging.info(f"GIT_HANLDER: Git username set to {GIT_USERNAME}")
        if GIT_EMAIL and repo.config_reader().get_value("user", "email", None) != GIT_EMAIL:
            config_writer.set_value("user", "email", GIT_EMAIL)
            changed = True
            logging.info(f"GIT_HANLDER: Git email set to {GIT_EMAIL}")
        if changed:
            logging.info("GIT_HANLDER: Git config updated successfully.")
        else:
            logging.info("GIT_HANLDER: No changes made to Git config.")
    finally:
        config_writer.release()

# Create Branch Func
def create_branch(branch_name):
    try:
        repo.git.checkout("-b", branch_name)
        logging.info(f"GIT_HANLDER: Branch '{branch_name}' created and checked out.")
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error creating branch '{branch_name}': {e}")

# Checkout Branch Func
def checkout_branch(branch_name):
    try:
        repo.git.checkout(branch_name)
        logging.info(f"GIT_HANLDER: Branch '{branch_name}' checked out.")
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error checking out branch '{branch_name}': {e}")

# Add all changes func
def add_all_changes():
    try:
        repo.git.add(A=True)
        logging.info("GIT_HANLDER: All changes added to staging area.")
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error adding changes: {e}")

# Commit changes func
def commit_changes(commit_message):
    try:
        if not commit_message:
            commit_message = "No Commit Message Provided"
        repo.git.commit(m=commit_message)
        logging.info(f"GIT_HANLDER: Changes committed with message: '{commit_message}'")
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error committing changes: {e}")

# Push changes func
def push_changes(branch_name):
    try:
        repo.git.push("origin", branch_name)
        logging.info(f"GIT_HANLDER: Changes pushed to branch '{branch_name}'.")
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error pushing changes to branch '{branch_name}': {e}")

def git_status():
    try:
        status = repo.git.status()
        logging.info("GIT_HANLDER: Current Git Status:")
        logging.info(status)
    except GitCommandError as e:
        logging.info(f"GIT_HANLDER: Error getting git status: {e}")