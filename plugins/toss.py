# For The-TG-Bot-3.0
# Syntax .toss

import random
import re
from userbot import syntax


@bot.on(command("toss ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await event.edit("**Heads**. \n You were correct.")
        elif input_str == "tails":
            await event.edit("**Heads**. \n You Lose.")
        else:
            await event.edit("**Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await event.edit("**Tails**. \n You were correct.")
        elif input_str == "heads":
            await event.edit("**Tails**. \n You Lose.")
        else:
            await event.edit("**Tails**.")
    else:
        await event.edit("¯\_(ツ)_/¯")


syntax.update({
    "toss": "\
```.toss <heads/tails>```\
\nUsage: Flips a virtual coin and returns the outcome, test your luck!\
"
})
