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
# add modules to this list using MODULES_LIST.append(MODULE_NAME)
# add syntax to this dictionary using SYNTAX.update
SYNTAX = {}
class MODULE_LISTS(list):
    def __init__(self):
        self.MODULES=[]
    def append(self,item):
        self.MODULES.append(item)        
    def __str__(self):
        self.MODULES.sort()
        return str(self.MODULES)
    def __len__(self):
        return len(self.MODULES)
    def __delitem__(self, index):
        self.MODULES.__delitem__(index - 1)
    def insert(self, index, value):
        self.MODULES.insert(index - 1, value)
    def __setitem__(self, index, value):
        self.MODULES.__setitem__(index - 1, value)
    def __getitem__(self, index):
        return self.MODULES.__getitem__(index - 1)
    def __iter__(self):
        return iter(self.MODULES)
MODULE_LIST=[]