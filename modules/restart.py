# For The-TG-Bot v3
# Syntax .restart

import os
import sys
import asyncio


@client.on(events(pattern="restart ?(.*)", allow_sudo=True))
async def handler(message):
    await message.edit("The-TG-Bot v3 has been restarted.\nTry .alive or .ping to check if its alive.")
    run_async(restart)


async def restart():
    await client.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
