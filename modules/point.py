# For The-TG-Bot v3
# By Priyam Kalra
# Syntax (.point <text_to_print>)

import asyncio



@client.on(events(pattern="point ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)
    await event.edit("╱╭━━┳━┳━┳╮" + " " + input + "\n━┫╱┓┣┳━━━╯\n╱╱╱┃┃╯\n━┫╱╰┛╯\n╱╰━━━╯\n")

ENV.HELPER.update({
    "point": "\
```.point <text_to_print>```\
\nUsage: Point at some text to get attention in a group chat.\
"
})
