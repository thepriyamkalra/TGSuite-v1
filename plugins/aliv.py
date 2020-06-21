from telethon import events
from datetime import datetime
from userbot import syntax
    
    
@bot.on(command(pattern="alive ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Yeah!")
    end = datetime.now()
    await event.edit("Yeah! 👍🏻 I'm Alive 🍻")

@bot.on(command(pattern="ping ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))

                     
syntax.update({
    "alive": "\
**Checks if The-TG-Bot is working or not!!**\
\n\n `.alive`\
\nUsage: __Checks if userbot is alive__\
\n\n  `.ping`\
\nUsage: __Ping-Pong!!__\
"
})
