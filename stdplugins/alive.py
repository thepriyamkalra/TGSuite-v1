# For UniBorg
# Syntax .alive
import sys
import os
import platform
from telethon import events, functions, __version__
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, BUILD


MODULE_LIST.append("alive")


@borg.on(admin_cmd(pattern="alive ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if Config.USER is not None:
        user = f"\n```User: {Config.USER}```"
    else:
        user = " "
    uname = platform.uname()
    specs = f"System: {uname.system}\nRelease: {uname.release}\nVersion: {uname.version}\nProcessor: {uname.processor}"
    help_string = f"Your bot is running.\n```Python {sys.version}```\n```Telethon {__version__}```\n```Build: {BUILD}```{str(user)}\n```By: @A_FRICKING_GAMER```\n\nSystem Specifications:\n{specs}"
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(  # pylint:disable=E0602
            tgbotusername,
            help_string + "\n\n"
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.reply(help_string + "\n\n")
        await event.delete()


SYNTAX.update({
    "alive": "\
**Requested Module --> alive**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.alive```\
\nUsage: Returns userbot's system stats, user's name (only if set).\
"
})
