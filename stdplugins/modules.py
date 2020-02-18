# For UniBorg
# By Priyam Kalra
# modified by @authoritydmc
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
    modules = "**List of available modules({0}):**\n".format(len(MODULE_LIST))
    MODULE_LIST.sort()
    prev="1"
    for module in MODULE_LIST:
        if prev[0]!=module[0]:
            modules+=f"\t{module[0].upper()}\t\n"
        modules += f"~ ```{module}```\n"
        prev=module
    modules += "\n\n**Tip --> Use .syntax <module_name> for more info.**"
    await event.edit(modules)
