# For UniBorg
# By Priyam Kalra
# Syntax (.modules)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import MODULE_LIST


@borg.on(admin_cmd(pattern="modules ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    counter = 0
    modules = "**List of available modules:**\n"
    for module in MODULE_LIST:
        modules += f"~ ```{MODULE_LIST}```\n"
    modules += "**Tip --> Use .syntax <module_name> for more info.**"
    await event.edit(modules)
