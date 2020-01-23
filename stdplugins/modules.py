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
    counter = 0
    modules = "**List of available modules:**\n"
    for module in MODULES_LIST:
        modules += f"```{MODULES_LIST[counter]}```\n"
        counter += 1
    modules += "**Tip --> Use .syntax <module_name> for for info.**"
    await event.edit(modules)
