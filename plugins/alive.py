from telethon import events
from datetime import datetime
from userbot import syntax
    
    
@bot.on(command(pattern="alive ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Yeah!")
    await event.edit("Yeah! 👍🏻 I'm Alive 🍻")

                     
syntax.update({
    "alive": "\
**Checks if The-TG-Bot is working or not!!**\
\n\n `.alive`\
\nUsage: __Checks if userbot is alive__\
"
})
