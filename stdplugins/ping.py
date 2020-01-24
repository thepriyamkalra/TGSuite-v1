from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("ping")


@borg.on(admin_cmd("ping"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))


SYNTAX.update({
    "ping": "\
**Requested Module --> ping**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.ping```\
\nUsage: Check your internet connection's ping speed.\
"
})
