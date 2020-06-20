# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax (.link <text_to_highlight> <link>)

import asyncio
from userbot import syntax


@bot.on(command(pattern="link ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    string = event.pattern_match.group(1)
    strings = string.split()
    link = strings[-1]
    strings = strings[:-1]
    string = " ".join(strings)
    output = f"[{string}]({link})"
    await event.edit(output)


syntax.update({
    "hyperlink": "\
```.link <text> <paste_link_here>```\
\nUsage: Generate a hyperlink using the provided link.\
"
})
