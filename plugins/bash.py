# For The-TG-Bot-3.0
# Syntax .bash <code>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time
from userbot import syntax


@bot.on(command(pattern="bash ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
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
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n`{o}`"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    await event.edit(OUTPUT)


syntax.update({
    "bash": "\
```.bash <code>```\
\nUsage: Evaluate bash code.\
"
})
