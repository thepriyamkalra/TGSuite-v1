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
from sql_helpers.global_variables_sql import SYNTAX, MODULES_LIST


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst



@borg.on(admin_cmd(pattern="share (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file")
    input_str = event.pattern_match.group(1)
    plugin = f"stdplugins/{input_str}.py"
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(plugin):
        start = datetime.now()
        c_time = time.time()
        await borg.send_file(
            event.chat_id,
            plugin,
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
        await mone.edit("404: Module not found")


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
    "share": "\
**Requested Module --> share**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.share <module_name>```\
\nUsage: Share a specified module.\
"
})

MODULES_LIST.append("share")
