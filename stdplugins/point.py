# For UniBorg
# By Priyam Kalra
# Syntax (.point <text_to_print>)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("point")

@borg.on(admin_cmd(pattern="point ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input = event.pattern_match.group(1)
        await event.edit("╱╭━━┳━┳━┳╮" + " " + input + "\n━┫╱┓┣┳━━━╯\n╱╱╱┃┃╯\n━┫╱╰┛╯\n╱╰━━━╯\n")

SYNTAX.update({
    "point": "\
**Requested Module --> point**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.point <text_to_print>```\
\nUsage: Point at some text to get attention in a group chat.\
"
})