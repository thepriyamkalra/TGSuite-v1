# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax (.say <text_to_print>)

import time
from userbot import syntax


@bot.on(command(pattern="say ?(.*)"))
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

syntax.update({
    "say": "\
```.say <text_to_print> (or as a reply to target message)```\
\nUsage: Says anything you want it to say.\
"
})
