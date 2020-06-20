# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
import sys
from pathlib import Path
from userbot import Userbot
from userbot.storage import Storage
from telethon.sessions import StringSession


logging.basicConfig(level=logging.INFO)


ENV = bool(os.environ.get("ENV", False))
if ENV:
    from production import Config
else:
    if os.path.exists("development.py"):
        from development import Config
    else:
        logging.warning("No config.py Found!")
        logging.info(
            "Please run the command, again, after creating config.py similar to README.md")
        sys.exit(1)


if Config.DB_URI is None:
    logging.warning("No DB_URI Found!")
    sys.exit(1)


if len(Config.SUDO_USERS) >= 0:
    Config.SUDO_USERS.add("me")

if Config.SESSION is not None:
    session_name = str(Config.SESSION)
    userbot = Userbot(
        StringSession(session_name),
        plugin_path="plugins/",
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    userbot.run_until_disconnected()
elif len(sys.argv) == 2:
    session_name = str(sys.argv[1])
    userbot = Userbot(
        session_name,
        plugin_path="plugins/",
        connection_retries=None,
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    userbot.run_until_disconnected()
else:
    # throw error
    logging.error("USAGE EXAMPLE:\n"
                  "python3 -m thetgbot <SESSION_NAME>"
                  "\nPlease follow the above format to run your userbot."
                  "\nAborting.")
