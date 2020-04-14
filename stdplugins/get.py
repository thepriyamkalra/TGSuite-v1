# For UniBorg
# Syntax .get (repo, heroku, packs)
import sys
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import REPOLINK, DEPLOYLINK, PACKS, SYNTAX, MODULE_LIST
from uniborg.util import admin_cmd


MODULE_LIST.append("get")

@borg.on(admin_cmd(pattern="get ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "repo":
        await event.edit(f"Checkout  my Repo [ @GITHUB]({REPOLINK}) ")
    elif input_str == "heroku":
        await event.edit(f"**Click** [here]({DEPLOYLINK}) **to goto the heroku deploy page.**")
    elif input_str == "packs":
        await event.edit(f"**Found the following sticker pack data:**\n{PACKS}")
    elif input_str == "guide":
        await event.edit(f"[ Follow this Guide ](https://authoritydmc.github.io/BEASTBOT-REBORN/)")
    else:
        pass
        
        
SYNTAX.update({
    "get": "\
**Requested Module --> get**\
\nDetailed usage of fuction(s):\
\n\n```.get repo```\
\nUsage: Prints github repoistory link defined in the env variable [REPO_LINK].\
\n\n```.get heroku```\
\nUsage: Prints the heroku deploy link defined in the env variable [DEPLOY_LINK].\
\n\n```.get packs```\
\nUsage: Prints the sticker pack data defined in the env variable [PACKS_CONTENT].\
"
})
