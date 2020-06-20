# For The-TG-Bot-3.0
# Syntax .ping

from datetime import datetime

from userbot import syntax


@bot.on(command("ping"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))


syntax.update({
    "ping": "\
```.ping```\
\nUsage: Check your internet connection's ping speed.\
"
})
