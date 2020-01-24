# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
# For UniBorg
# Syntax .file <location>, .dir <location>
import asyncio
import os
import subprocess
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeAudio
from uniborg.util import progress, admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


MODULE_LIST.append("upload")


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


@borg.on(admin_cmd("dir (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        # await event.edit("Processing...")
        lst_of_files = sorted(get_lst_of_files(input_str, []))
        logger.info(lst_of_files)
        u = 0
        await event.edit(
            "Found {} files. ".format(len(lst_of_files)) +
            "Uploading will start soon. " +
            "Please wait!"
        )
        thumb = None
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                width = 0
                height = 0
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                if single_file.endswith((".mkv", ".mp4", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                    supports_streaming = True
                    force_document = False
                if single_file.endswith((".mp3", ".flac", ".wav")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    title = ""
                    artist = ""
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if metadata.has("title"):
                        title = metadata.get("title")
                    if metadata.has("artist"):
                        artist = metadata.get("artist")
                    document_attributes = [
                        DocumentAttributeAudio(
                            duration=duration,
                            voice=False,
                            title=title,
                            performer=artist,
                            waveform=None
                        )
                    ]
                    supports_streaming = True
                    force_document = False
                try:
                    await borg.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        thumb=thumb,
                        attributes=document_attributes,
                        # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        #     progress(d, t, event, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await borg.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
                u = u + 1
                # await event.edit("Uploaded {} / {} files.".format(u, len(lst_of_files)))
                # @ControllerBot was having issues,
                # if both edited_updates and update events come simultaneously.
                await asyncio.sleep(5)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded {} files in {} seconds.".format(u, ms))
    else:
        await event.edit("404: Directory Not Found")


@borg.on(admin_cmd(pattern="file (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file")
    input_str = event.pattern_match.group(1)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(input_str):
        start = datetime.now()
        c_time = time.time()
        await borg.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            thumb=thumb,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "")
            )
        )
        end = datetime.now()
        # os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit(f"Uploaded {input_str} in {ms} seconds.")
    else:
        await mone.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)
                       [metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output


SYNTAX.update({
    "upload": "\
**Requested Module --> upload**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.file <file_location>```\
\nUsage: Upload a file from your local machine.\
\n\n```.dir <dir_location>```\
\nUsage: Upload a directory from your local machine.\
"
})
