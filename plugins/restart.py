import os
import sys
import asyncio
from userbot import syntax


@bot.on(command(pattern="restart ?(.*)", allow_sudo=True))
async def handler(message):
    await message.edit("The-TG-Bot has been restarted.\nTry .alive to if its alive")
    asyncio.get_event_loop().create_task(restart())
    

async def restart():
    await bot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)