# For The-TG-Bot-3.0
# Syntax .restart
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html

import asyncio
import os
import sys
import time
from userbot import syntax


@bot.on(command("restart"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Restarting...\n█████░░░")
    time.sleep(1)
    await event.edit("Restarting...\n████████")
    time.sleep(1)
    await event.edit("Restart Complete!\nSend .alive or .ping to check if i am online.")
    await bot.disconnect()
    # https://archive.is/im3rt
    os.execl(sys.executable, sys.executable, *sys.argv)
    # You probably don't need it but whatever
    quit()


syntax.update({
    "restart": "\
```.restart```\
\nUsage: Restart your userbot.\
"
})
