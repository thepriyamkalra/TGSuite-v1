# For UniBorg
# By Priyam Kalra
# Syntax (.link <link>)

from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("hyperlink")

@borg.on(admin_cmd(pattern="link ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input = event.pattern_match.group(1)
        await event.edit("Click [here](" + input + ")")
        
        
SYNTAX.update({
    "hyperlink": "\
**Requested Module --> hyperlink**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.link <paste_link_here>```\
\nUsage: Generated a hyperlink using the provided link.\
"
})

