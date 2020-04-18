# For UniBorg
# Syntax .alive
import sys
from telethon import events, functions, __version__,utils
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST
import platform
import psutil
import os
MODULE_LIST.append("alive")


BUILD="-69x71"





@borg.on(admin_cmd(pattern="alive ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_first_name="set Firstname in your Profile"
    user_last_name="set lastName in your profile"
    userobj=None
    user_name=""
    try:
        userobj= await borg.get_me()
    except:
        userobj=None
    try:
        user_name=userobj.username
        user_first_name=userobj.first_name
        if user_first_name is None:
            user_first_name=""
    except:
        user_first_name=""
    try:
        user_last_name=userobj.last_name
        if user_last_name is None :
            user_last_name=""
    except:
        user_last_name=""


    uname = platform.uname()
    memory = psutil.virtual_memory()
    specs = f"```System: {uname.system}```\n```Release: {uname.release}```\n```Version: {uname.version}```\n```Processor: {uname.processor}```\n```Memory [RAM]: {get_size(memory.total)}```"
    help_string = f":-> \t\t          **BEASTBOT-REBORN v 2.01**\t\t          <-:\n\n\
    \n**Owner** : [{user_first_name} {user_last_name}](https://t.me/{user_name}).\n\
    \n**Build** : ```{user_first_name}{BUILD}```\n**By** : @beast0110\
    \n**Deploy Code** : [@Github](https://github.com/authoritydmc/BEASTBOT-REBORN)\n\
    \n**System Information** : \n{specs}\
    \n**Python** : ```{sys.version[:5]}```\n**Telethon** : ```{__version__}```\n"
    
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
        # await event.reply(help_string + "\n\n")
        await event.delete()
        await borg.send_message(event.chat_id,help_string+"\n\n",silent=True
        ,link_preview=False
        )
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

SYNTAX.update({
    "alive": "\
**Requested Module --> alive**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.alive```\
\nUsage: Returns BEASTBOT-REBORN's system stats, user's name (only if set).\
"
})
