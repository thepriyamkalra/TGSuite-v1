from git.Repo import clone_from as clone
from shutil import copytree, rmtree
from os.environ import get
GITHUB_REPO_LINK = get("GITHUB_REPO_LINK", "https://github.com/justaprudev/The-TG-Bot")
print("Downloading latest version of The-TG-Bot..")
clone(GITHUB_REPO_LINK, "package")
copytree("package", ".", dirs_exist_ok=True)
rmtree("package")
import thetgbot
