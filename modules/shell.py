# For The-TG-Bot v3
# Syntax .shell <cmd>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import io
import asyncio
import time


@client.on(events(pattern="\$(.*)", no_handler=True))
async def handler(event):
    if event.fwd_from:
        return
    cmd = event.text[1:]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    stdout, stderr =  await client.shell(cmd)
    OUTPUT = f"**Query:**\n`{cmd}`\n\n**Errors (stderr):** \n`{stderr}`\n\n**Output (stdout):**\n`{stdout}`"
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
```$<code>```\
\nUsage: Your own personal 'cloud' shell, all inputs are evaluated asynchronously with subprocess.\
"
})
