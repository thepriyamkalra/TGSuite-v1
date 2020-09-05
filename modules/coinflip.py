# For The-TG-Bot v3
# Syntax .coinflip

import random
import re



@client.on(events("coinflip ?(.*)"))
async def handler(event):
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


ENV.HELPER.update({
    "coinflip": "\
```.coinflip <optional_choice>```\
\nUsage: Flips a virtual coin and returns the outcome, test your luck!\
"
})
