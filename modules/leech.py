# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
# For The-TG-Bot-3.0

import aria2p
import asyncio
import json
import math
import os
import time
import subprocess
import httplib2
from datetime import datetime
from mimetypes import guess_type
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.errors import ResumableUploadError
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeAudio



cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"
aria2_is_running = os.system(cmd)
aria2 = aria2p.API(aria2p.Client(
    host="http://localhost", port=6800, secret=""))
EDIT_SLEEP_TIME_OUT = 10
thumb_image_path = ENV.DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
G_DRIVE_F_PARENT_ID = None
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


@client.on(events(pattern="leech ?(.*)"))
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.pattern_match.group(1)
    if not var:
        rep = event.get_reply_message()
        var = rep.text
    # print(var)
    uris = [var]
    # Add URL Into Queue
    try:
        download = aria2.add_uris(uris, options=None, position=None)
    except Exception as e:
        await log(str(e))
        return await event.delete()

    gid = download.gid
    complete = None
    await progress_status(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid, event=event, previous=None)
    while complete != True:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            msg = "**Leeching:** "+str(file.name) + "\n**Speed:** " + str(file.download_speed_string())+"\n**Progress:** "+str(
                file.progress_string())+"\n**Total Size:** "+str(file.total_length_string())+"\n**ETA:**  "+str(file.eta_string())+"\n\n"
            await event.edit(msg)
            await asyncio.sleep(10)
        except Exception as e:
            await log(str(e))
            pass

    await event.edit(f"```{file.name}``` leeched successfully!")


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


# Get mime type and name of given file
def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(
        CLIENT_ID,
        CLIENT_SECRET,
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI
    )
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(ENV.LOGGER_GROUP) as conv:
        await conv.send_message(f"Go to the following link in your browser: {authorize_url} and reply the code")
        response = conv.wait_event(events.NewMessage(
            outgoing=True,
            chats=ENV.LOGGER_GROUP
        ))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    # Get credentials
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    # Create Google Drive service instance
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    # File body description
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Uploaded using @Unibot gDrive v2",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"] = [{"id": parent_id}]
    # Permissions body description: anyone who has link can upload
    # Other permissions can be found at https://developers.google.com/drive/v2/reference/permissions
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    # Insert a file
    file = drive_service.files().insert(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk()
        await asyncio.sleep(1)
        if status:
            percentage = int(status.progress() * 100)
            progress_str = "[{0}{1}]\nProgress: {2}%\n".format(
                "".join(["█" for i in range(math.floor(percentage / 5))]),
                "".join(["░" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2)
            )
            current_message = f"uploading to gDrive\nFile Name: {file_name}\n{progress_str}"
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception as e:
                    logger.info(str(e))
                    pass
    file_id = response.get("id")
    try:
        # Insert new permissions
        drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    except:
        pass
    # Define file instance and get url for download
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return download_url


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE
    }
    if parent_id is not None:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    try:
        drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    except:
        pass
    logger.info("Created Gdrive Folder:\nName: {}\nID: {} ".format(
        file.get("title"), file_id))
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name, parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event, current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            # current_file_name will have the full path
            g_drive_link = await upload_file(http, current_file_name, file_name, mime_type, event, parent_id)
            r_p_id = parent_id
    # TODO: there is a #bug here :(
    return r_p_id


async def log(text):
    LOGGER = ENV.LOGGER_GROUP
    await client.send_message(LOGGER, text)


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    logger.info("Changing GID "+gid+" to "+new_gid)
    return new_gid


async def progress_status(gid, event, previous):
    global req_file
    try:
        file = aria2.get_download(gid)
        req_file = str(file.name)
        if not file.is_complete:
            if not file.error_message:
                msg = "**Leeching**: `"+str(file.name) + "`\n**Speed**: " + str(file.download_speed_string())+"\n**Progress**: "+str(file.progress_string(
                ))+"\n**Total Size**: "+str(file.total_length_string())+"\n**Status**: "+str(file.status)+"\n**ETA**:  "+str(file.eta_string())+"\n\n"
                if previous != msg:
                    await event.edit(msg)
                    previous = msg
            else:
                logger.info(str(file.error_message))
                await log("Error : `{}`".format(str(file.error_message)))
                return
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await progress_status(gid, event, previous)
        else:
            await event.edit(f"```{file.name}``` leeched successfully!")
            return
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await log(str(e))
            return await event.delete()
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await log(str(e))
        else:
            await log(str(e))
            return await event.delete()

ENV.HELPER.update({
    "leech": "\
```.leech <magnet-link> (or as a reply to a magnet link)```\
\nUsage: Downloads the torrent to the local machine.\
"
})
