# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax (.spam <number of msgs> <text>)

from asyncio import wait
import asyncio
from time import sleep
from userbot import syntax


@bot.on(command(pattern="spam ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input = str(event.pattern_match.group(1))
    input_split = input.split()
    chat = event.chat_id
    count = str(input_split[0])
    strip = len(count)
    text = input[strip:]
    if not text:
        text = reply
    if text and count != None:
        for spam in range(int(count)):
            await bot.send_message(
                event.chat_id,
                text,
                parse_mode="HTML",
                force_document=False,
                silent=True
            )
    else:
        return await event.edit("This is not how it works..\nUse ```.help spam``` for help.")
    sleep(2)
    await event.delete()

syntax.update({
    "spam": "\
```.spam <number of msgs> <text>```\
\nUsage: Spams the given text.\
```.spam <number of msgs> (as a reply to a message)```\
\nUsage: Spams the replied message.\
"
})
