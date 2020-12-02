# Taken from Uniborg

import io
import os
import requests
from datetime import datetime
from PIL import Image

Rmbgkey = os.environ.get("RMBG_API_KEY", None)

@client.on(events(pattern="rmbg ?(.*)"))
async def _(event):
    HELP_STR = "`.rmbg as reply to a media, or give a link as an argument to this command`"
    if event.fwd_from:
        return
    if Rmbgkey is None:
        return await event.edit("`You need API token from remove.bg to use this plugin.`")
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    reply_message = await event.get_reply_message()
    if reply_message:
        if reply_message.photo or reply_message.sticker:
            await event.edit("`Sharpening the scissors.`")
            try:
                downloaded_file_name = await client.download_media(
                    reply_message, os.path.join(ENV.DOWNLOAD_DIRECTORY, "rmbg.webp")
                )
                downloaded_file_name = convert(downloaded_file_name)
            except Exception as e:
                await event.edit(str(e))
                return
            else:
                await event.edit("`Cutting the image..`")
                output_file_name = ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("`Cutting the image..`")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.edit(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "nobg.png"
            await client.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=reply_message
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(f"`Snapped the image's Background in {ms} seconds`")
    else:
        await event.edit(f"Remove.BG API returned Errors. DO NOT REPORT IN @The_TG_Bot_Support IF YOU DONT WANT A FREE BAN!\n\n`{str(output_file_name.content)}`")


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Rmbgkey,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r

def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Rmbgkey,
    }
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r
    
def convert(webp):
    Image.open(webp).save(webp, "PNG")
    path = os.path.splitext(webp)[0] + ".png"
    os.rename(webp, path)
    return path

ENV.HELPER.update({
    "rmbg": "\
```.rmbg <in reply to image/sticker>```\
\nUsage: Removes the background of image/sticker.\
"
})
