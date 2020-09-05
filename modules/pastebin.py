# For The-TG-Bot v3
# Syntax .paste

import asyncio
from datetime import datetime
import os
import requests


def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(
        current, total, (current / total) * 100))


@client.on(events("paste ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(ENV.DOWNLOAD_DIRECTORY):
        os.makedirs(ENV.DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await client.download_media(
                previous_message,
                ENV.DOWNLOAD_DIRECTORY,
                progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await event.edit("Pasted to {} in {} seconds. Goto Original URL: {}".format(url, ms, nurl))
    else:
        await event.edit("Pasted to {} in {} seconds".format(url, ms))


ENV.HELPER.update({
    "pastebin": "\
```.paste (as a reply to the msg you want to paste)```\
\nUsage: Pastes the target message to del.dog.\
"
})
