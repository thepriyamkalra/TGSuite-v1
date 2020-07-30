# For The-TG-Bot v3
# By Priyam Kalra

import time



@client.on(register(pattern="log ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    rep = await event.get_reply_message()
    msg = rep.text
    await log(msg)
    await event.delete()


async def log(text):
    LOGGER = Config.LOGGER_GROUP
    await client.send_message(LOGGER, text)

Config.HELPER.update({
    "log": "\
```.log (as a reply to target message)```\
\nUsage:  Simply log the replied msg to logger group.\
"
})
