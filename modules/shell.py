# For The-TG-Bot v3
# Syntax .shell <cmd>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import io
import asyncio
import time


@client.on(events(pattern="shell ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    o = ""
    e = ""
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    proc = subprocess.run(cmd, capture_output=True, shell=True)
    out = [str(proc.stdout)[2:][:-1], str(proc.stderr)[2:][:-1]]
    stdout = out[0] if out[0] else "None"
    for l in stdout.split("\\n"):
        o += f"{l}\n"
    stderr = out[1] if out[1] else "None"
    for l in stderr.split("\\n"):
        e += f"{l}\n"
    OUTPUT = f"**Query:**\n`{cmd}`\n\n**Errors (stderr):** \n`{e}`\n**Output (stdout):**\n`{o}`"
    if len(OUTPUT) > ENV.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "shell.txt"
            await client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            return await event.delete()
    await event.edit(OUTPUT)


ENV.HELPER.update({
    "shell": "\
```.shell <code>```\
\nUsage: Your own personal shell, all inouts are evaluated with subprocess.run().\
"
})
