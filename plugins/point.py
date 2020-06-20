# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax (.point <text_to_print>)

import asyncio
from userbot import syntax


@bot.on(command(pattern="point ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)
    await event.edit("╱╭━━┳━┳━┳╮" + " " + input + "\n━┫╱┓┣┳━━━╯\n╱╱╱┃┃╯\n━┫╱╰┛╯\n╱╰━━━╯\n")

syntax.update({
    "point": "\
```.point <text_to_print>```\
\nUsage: Point at some text to get attention in a group chat.\
"
})
