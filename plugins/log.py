# For The-TG-Bot-3.0
# By Priyam Kalra

import time
from userbot import syntax


@bot.on(command(pattern="log ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    rep = await event.get_reply_message()
    msg = rep.text
    await log(msg)
    await event.delete()


async def log(text):
    LOGGER = Config.LOGGER_GROUP
    await bot.send_message(LOGGER, text)

syntax.update({
    "log": "\
```.log (as a reply to target message)```\
\nUsage:  Simply log the replied msg to logger group.\
"
})
