import subprocess
print("Downloading latest version of The-TG-Bot..")
subprocess.run("git clone https://github.com/justaprudev/The-TG-Bot git && mv git/* . && rm -rf git", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print("Starting process with command `python3 -m thetgbot`")
print("State changed from starting to up")
subprocess.run("python3 -m thetgbot", shell=True)
