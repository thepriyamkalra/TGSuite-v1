# For UniBorg
# Syntax .flip
from telethon import events
import random, re
from uniborg.util import admin_cmd


@borg.on(admin_cmd("flip ?(.*)"))
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
            await event.edit("**Heads**. \n Better luck next time!...")
        else:
            await event.edit("**Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await event.edit("**Tails**. \n You were correct.")
        elif input_str == "heads":
            await event.edit("**Tails**. \n Better luck next time!...")
        else:
            await event.edit("**Tails**.")
    else:
        await event.edit("¯\_(ツ)_/¯")
