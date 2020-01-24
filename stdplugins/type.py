# For UniBorg
# Syntax .type <text>

from telethon import events
import asyncio
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


MODULE_LIST.append("type")

@borg.on(events.NewMessage(pattern=r"\.type (.*)", outgoing=True))
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



SYNTAX.update({
    "type": "\
**Requested Module --> type**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.type <text_to_type>```\
\nUsage: Type text with a fancy typing animation.\
"
})