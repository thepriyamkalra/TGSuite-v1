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
# add modules to the list using MODULES_LIST.append(MODULE_NAME)
MODULES_LIST = ["~admin", "~afk", "~alive", "~bio", "~coinflip", "~download", "~get", "~hyperlink", "~id", "~insult", "~kang", "~locks", "~lydia", "~notes", "~pastebin", "~ping", "~pmpermit", "~point", "~purge", "~python", "~quotes", "~reactions", "~rename", "~report", "~spam", "~stat", "~translate", "~type", "~upload", "~urbandictionary", "~whois"]
# add syntax to this dictionary using SYNTAX.update
SYNTAX = {}