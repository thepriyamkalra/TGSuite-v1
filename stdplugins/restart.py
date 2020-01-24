# For UniBorg
# Syntax .restart
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
from telethon import events
import asyncio
import os
import sys
from uniborg.util import admin_cmd
import time
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("restart")


@borg.on(admin_cmd("restart"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Restarting...\n█████░░░")
    time.sleep(1)
    await event.edit("Restarting...\n████████")
    time.sleep(1)
    await event.edit("Restart Complete!\nSend .alive or .ping to check if i am online.")
    await borg.disconnect()
    # https://archive.is/im3rt
    os.execl(sys.executable, sys.executable, *sys.argv)
    # You probably don't need it but whatever
    quit()


SYNTAX.update({
    "restart": "\
**Requested Module --> restart**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.restart```\
\nUsage: Restart your userbot.\
"
})
