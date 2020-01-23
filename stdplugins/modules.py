# For UniBorg
# By Priyam Kalra
# Syntax (.modules)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import MODULES_LIST

@borg.on(admin_cmd(pattern="modules ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input = event.pattern_match.group(1)
        await event.edit(*MODULES_LIST)
