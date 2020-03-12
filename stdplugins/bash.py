# For UniBorg
# Syntax .bash <code>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST,SUDO_USERS

MODULE_LIST.append("bash")
@borg.on(admin_cmd(pattern="bash ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    arg = event.pattern_match.group(1)
    if not arg:
    	arg="@@@" 
    cmd = await event.get_reply_message()
    if "f" in arg:
    	arg=True
    else:
    	arg=False
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`Use .syntax bash to get help regarding this module.`"
    else:
        _o = o.split("\n")
        o = "\n".join(_o)
    OUTPUT="NULL"
    if arg==True:
    	if not "No Error" in e:
    		o="\n**stderror**:\n"+e+"\n**OUTPUT**\n"+o
    		OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n**stderr**\n`{e}`\n**OUTPUT**\n`{o}`"
    	else:
    		OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n**OUTPUT**\n`{o}`"
    else:
    	if not "No Error" in e:
    	    OUTPUT=f"\n**stderror**\n{e}\n **OUTPUT**\n `{o}`"
    	else:
    	    OUTPUT=f"**OUTPUT**\n`{o}`"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    await event.edit(OUTPUT)
SYNTAX.update({
    "bash": "\
**Requested Module --> bash**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.bash <code>```\
\nUsage: Evaluate bash code.\
"
})
