# For The-TG-Bot v3
# By Priyam Kalra


@client.on(events(pattern="log$"))
async def handler(event):
    if event.fwd_from:
        return
    rep = await event.get_reply_message()
    msg = rep.text
    await log(msg)
    await event.delete()

async def log(text):
    LOGGER = ENV.LOGGER_GROUP
    await client.send_message(LOGGER, text)


ENV.HELPER.update({
    "log": "\
```.log (as a reply to target message)```\
\nUsage:  Simply log the replied msg to logger group.\
"
})
