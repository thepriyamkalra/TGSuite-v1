# For UniBorg
# Syntax .alive
import sys
from telethon import events, functions, __version__
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


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
    help_string = """BEAST bot is running.
```Python {}```
```Telethon {}```
<<<<<<< HEAD
``` Made With Love :) ```
=======
``` Made With Love :) ```\n
Deploy Code [@Github](https://github.com/authoritydmc/The-TG-Bot-2.0)
>>>>>>> new_mod
""".format(
        sys.version,
        __version__
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
\nUsage: Returns userbot's system stats.\
"
})
