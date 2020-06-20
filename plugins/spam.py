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
    input = str(event.pattern_match.group(1))
    input_split = input.split()
    chat = event.chat_id
    try:
        count = str(input_split[0])
    except ValueError:
        await event.edit("Invalid Syntax!\nTip: Use ```.syntax spam``` for help.")
        return
    if input.startswith(count):
        strip = len(count)
        text = input[strip:]
    else:
        await event.edit("Fatal Error!\nPlease contact the developer of this module [@A_FRICKING_GAMER] for support.")
        return
    if text and count != None:
        await event.delete()
        for spam in range(int(count)):
            await event.reply(text)
        msg = await event.reply(f"Task complete, spammed input text {count} times!")
        sleep(5)
        await msg.delete()
        status = f"SPAMMED\n```{text}```\n in ```{chat}``` ```{count}``` times."
        await log(status)
    else:
        await event.edit("Unexpected Error! Aborting..")
        return

async def log(text):
    LOGGER = Config.LOGGER_GROUP
    await bot.send_message(LOGGER, text)

syntax.update({
    "spam": "\
```.spam <number of msgs> <text>```\
\nUsage: Spam a specified message upto the TG API limit (probably non existent but meh).\
"
})
