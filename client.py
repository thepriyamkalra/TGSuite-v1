import os
from git import Repo
from shutil import copytree, rmtree
GITHUB_REPO_LINK = os.environ.get("GITHUB_REPO_LINK", "https://github.com/justaprudev/The-TG-Bot")
print("Downloading latest version of The-TG-Bot..")
Repo.clone_from(GITHUB_REPO_LINK, "package")
copytree("package", ".", dirs_exist_ok=True)
rmtree("package")
import thetgbot
