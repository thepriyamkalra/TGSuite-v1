# For The-TG-Bot v3
# Syntax .restart

import os
import sys
import asyncio


@client.on(register(pattern="restart ?(.*)", allow_sudo=True))
async def handler(message):
    await message.edit("The-TG-Bot v3 has been restarted.\nTry .alive to if its alive")
    asyncio.get_event_loop().create_task(restart())


async def restart():
    await client.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
