# For The-TG-Bot v3
# Syntax .ping

from datetime import datetime


@client.on(events("ping"))
async def handler(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))


ENV.HELPER.update({
    "ping": "\
```.ping```\
\nUsage: Check your internet connection's ping speed.\
"
})
