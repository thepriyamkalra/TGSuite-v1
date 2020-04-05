# For UniBorg
# Syntax .alive
import sys
from telethon import events, functions, __version__,utils
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, BUILD

MODULE_LIST.append("alive")




# if Config.BOT_USER is not None:
#     username=Config.BOT_USER
user_first_name=""
user_last_name=""
try:
    userobj=  await borg.get_me()
    user_last_name=userobj.last_name
except:
    user_last_name="error getting lastName @getme"

@borg.on(admin_cmd(pattern="alive ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    re=await event.get_reply_message()

    try:
        obj_user = await event.client(
                 GetFullUserRequest(
                    re.chat_id
                )
            )
        user_first_name=obj_user.first_name
    except :
        user_first_name="Error at getting User Firstname"

 
    help_string = f"BEASTBOT-REBORN v 1.3 is running for **{user_first_name}** \t{user_last_name}.\n```Python {sys.version}```\n```Telethon {__version__}```\n```Build: {BUILD}```\nBy: @beast0110\nDeploy Code [@Github](https://github.com/authoritydmc/BEASTBOT-REBORN)"
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
