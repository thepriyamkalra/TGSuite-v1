# For UniBorg
# Syntax .alive
import sys
from telethon import events, functions, __version__
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST
import os
import re

MODULE_LIST.append("alive")


@borg.on(admin_cmd(pattern="alive ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    splugin_name = event.pattern_match.group(1)
    if splugin_name in borg._plugins:
        s_help_string = borg._plugins[splugin_name].__doc__
    else:
        s_help_string = ""
    PYTHON_version=""
    
    z=os.popen("pip  --version")
    sr=z.read()
    x = re.search(r"(\d+)\.(\d+)\.(\d+)", sr)
    PIP_version=x.group()
    for z in range(3):
        PYTHON_version+=str(sys.version_info[z])+("." if z <2 else "")
    help_string = """BEAST bot is running.\n```Python {}\n``````Telethon {}\n``````\n``````Pip {}\n``````\nMade With Love :) v1.1 ```\n
    Deploy Code [@Github](https://github.com/authoritydmc/BEASTBOT-REBORN)
    """.format(
        PYTHON_version,
        __version__,
        PIP_version

    )
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(  # pylint:disable=E0602
            tgbotusername,
            help_string + "\n\n" + s_help_string
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.reply(help_string + "\n\n" + s_help_string)
        await event.delete()


SYNTAX.update({
    "alive": "\
**Requested Module --> alive**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.alive```\
\nUsage: Returns userbot's system stats..   .\
"
})
