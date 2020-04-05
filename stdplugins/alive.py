# For UniBorg
# Syntax .alive
import sys
from telethon import events, functions, __version__,utils
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, BUILD

MODULE_LIST.append("alive")
username="set USER_NAME in Heroku Config"

# if Config.BOT_USER is not None:
#     username=Config.BOT_USER

@borg.on(admin_cmd(pattern="alive ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    try:
        username=await  utils.get_display_name()
    except :
        username="Failed to get userName from getme()"
    help_string = f"BEASTBOT-REBORN v 1.3 is running for **{username}**.\n```Python {sys.version}```\n```Telethon {__version__}```\n```Build: {BUILD}```\nBy: @beast0110\nDeploy Code [@Github](https://github.com/authoritydmc/BEASTBOT-REBORN)"
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
\nUsage: Returns BEASTBOT-REBORN's system stats, user's name (only if set).\
"
})
