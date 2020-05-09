# global variables will be assigned here
# can be imported in any module to make life easier.
from sample_config import Config
LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
BLACKLIST = Config.UB_BLACK_LIST_CHAT
SUDO_USERS = Config.SUDO_USERS
PACK_NAME = Config.PACK_NAME
ANIM_PACK_NAME = Config.ANIM_PACK_NAME
DEPLOYLINK = Config.HEROKU_LINK
REPOLINK = Config.REPO_LINK
PACKS = Config.PACKS_CONTENT
DL = Config.TMP_DOWNLOAD_DIRECTORY
# add modules to this list using MODULES_LIST.append(MODULE_NAME)
MODULE_LIST = []
# add syntax to this dictionary using SYNTAX.update()
SYNTAX = {}
BUILD = "USERDEBUG-50x03"
