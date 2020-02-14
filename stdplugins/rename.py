# For UniBorg
# Syntax .rename <new_file_name>

import aiohttp
import asyncio
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import json
import os
import requests
import subprocess
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError
import time
from uniborg.util import progress, humanbytes, time_formatter, admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("rename")


@borg.on(admin_cmd("rename (.*)"))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    await event.edit(f"Downloading file to local machine..\nThis may take a while depending on the file size.")
    time.sleep(1)
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        await event.edit(f"Download complete!\nRenaming downloaded file to {input_str}..")
        time.sleep(0.25)
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        await event.edit("File renamed successfully!\nUploading renamed file..\nThis may take a while depending on the file size.")
        time.sleep(.35)
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                )
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            total_ms = int(ms_one) + int(ms_two)
            await event.edit(f"Uploaded renamed file ```{input_str}``` in {ms_two} seconds!")

        else:
            await event.edit("File {} not found.".format(input_str))
    else:
        await event.edit("Syntax // .rnupload file.name as reply to a Telegram media")


SYNTAX.update({
    "rename": "\
**Requested Module --> rename**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.rename <new_file_name>``` [as a reply to a target file]\
\nUsage: Renames the target file to <new_file_name>.\
"
})
