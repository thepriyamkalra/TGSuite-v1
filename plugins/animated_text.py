# For The-TG-Bot-3.0
# Syntax .type <text>, .say <text>

import asyncio
import time
from userbot import syntax


@bot.on(command(pattern="type (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    # https://t.me/AnotherGroup/176551
    input_str = event.pattern_match.group(1)
    typing_symbol = "|"
    DELAY_BETWEEN_EDITS = 0.3
    previous_text = ""
    await event.edit(typing_symbol)
    await asyncio.sleep(DELAY_BETWEEN_EDITS)
    for character in input_str:
        previous_text = previous_text + "" + character
        typing_text = previous_text + "" + typing_symbol
        await event.edit(typing_text)
        await asyncio.sleep(DELAY_BETWEEN_EDITS)
        await event.edit(previous_text)
        await asyncio.sleep(DELAY_BETWEEN_EDITS)


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
    "animated text": "\
• ```.type <text_to_type>```\
\nUsage: Type text with a fancy typing animation.\
\n\n• ```.say <text_to_print> (or as a reply to target message)```\
\nUsage: Says anything you want it to say.\
"
})
