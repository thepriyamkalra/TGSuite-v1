# For UniBorg
# Syntax .get (repo, heroku, packs)
import sys
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import REPOLINK, DEPLOYLINK, PACKS
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="get ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "repo":
        await event.edit(f"**Click** [here]({REPOLINK}) **to goto the custom github repo.**")
    elif input_str == "heroku":
        await event.edit(f"**Click** [here]({DEPLOYLINK}) **to goto the heroku deploy page.**")
    elif input_str == "packs":
        await event.edit(f"**Found the following sticker pack data:**\n{PACKS}")
    else:
        pass
