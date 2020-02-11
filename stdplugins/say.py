# For UniBorg
# By Priyam Kalra
# Syntax (.say <text_to_print>)
from uniborg.util import admin_cmd
from telethon.tl import functions, types
import time
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("say")

@borg.on(admin_cmd(pattern="say ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)
    if not input:
    	abe = await event.get_reply_message()
    	input = abe.text
    strings = input.split()
    count = 0
    output = ""
    for _ in strings:
        output += f"{strings[count]}\n"
        count += 1
        await event.edit(output)
        time.sleep(0.25)

SYNTAX.update({
    "say": "\
**Requested Module --> say**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.say <text_to_print> (or as a reply to target message)```\
\nUsage: Says anything you want it to say.\
"
})
