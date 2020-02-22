# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
# For UniBorg

import aria2p
import asyncio
import json
import math
import os
import time
import subprocess
import httplib2
from telethon import events
from datetime import datetime
from telethon import events
from uniborg.util import admin_cmd, progress, humanbytes
from mimetypes import guess_type
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import file, client, tools
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeAudio
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("leech")
MODULE_LIST.append("leech2drive")
MODULE_LIST.append("leech2tg")

cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(aria2p.Client(
    host="http://localhost", port=6800, secret=""))

EDIT_SLEEP_TIME_OUT = 10

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
# Path to token json file, it should be in same directory as script
G_DRIVE_TOKEN_FILE = f"./{Config.TMP_DOWNLOAD_DIRECTORY}/auth_token.txt"
# Copy your credentials from the APIs Console
CLIENT_ID = Config.G_DRIVE_CLIENT_ID
CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# global variable to set Folder ID to upload to
G_DRIVE_F_PARENT_ID = None
# global variable to indicate mimeType of directories in gDrive
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


@borg.on(admin_cmd(pattern="leech ?(.*)"))
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


@borg.on(admin_cmd("l2tg (.*)"))
async def leech2tg(event):
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
            msg = "**Leeching:** "+req_file + "\n**Speed:** " + str(file.download_speed_string())+"\n**Progress:** "+str(
                file.progress_string())+"\n**Total Size:** "+str(file.total_length_string())+"\n**ETA:**  "+str(file.eta_string())+"\n\n"
            await event.edit(msg)
            await asyncio.sleep(10)
        except Exception as e:
            await log(str(e))
            pass
        # TG UPLOAD
        to_upload = f"./{req_file}"
    if os.path.isdir(to_upload):
        input_str = to_upload
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
                        metadata = extractMetadata(
                            createParser(thumb_image_path))
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
            await event.edit("Oh snap! Something went wrong!")
    elif os.path.isfile(to_upload):
        mone = await event.edit("Uploading required file..")
        input_str = to_upload
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
            await mone.edit("Oh snap! Something went wrong!")
    else:
        await ("Oh snap! Something went wrong!")


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


@borg.on(admin_cmd(pattern="l2d ?(.*)"))
async def leech2drive(event):
    if event.fwd_from:
        return
    var = event.pattern_match.group(1)
    if not var:
        rep = event.get_reply_message()
        var = rep.text
    if str(var) == "setup":
        telegraph = "https://telegra.ph/Leech2Drive-Setup-Tutorial-02-21"
        return await event.edit(f"Find gdrive setup instructions for leech2drive [here]({telegraph}).")
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
        torrent = str(file.name)
        if torrent.startswith("[METADATA]"):
            torrent = torrent[10:]
        complete = file.is_complete
        try:
            msg = "**Leeching:** "+req_file + "\n**Speed:** " + str(file.download_speed_string())+"\n**Progress:** "+str(
                file.progress_string())+"\n**Total Size:** "+str(file.total_length_string())+"\n**ETA:**  "+str(file.eta_string())+"\n\n"
            await event.edit(msg)
            await asyncio.sleep(10)
        except Exception as e:
            await log(str(e))
            pass
    # GDRIVE UPLOAD
    input_str = req_file
    required_file = req_file
    await event.delete()
    mone = await event.reply(f"Uploading files to Gdrive...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit(f"Find gdrive setup instructions for leech2drive [here]({telegraph}).")
        return
    if Config.PRIVATE_GROUP_BOT_API_ID is None:
        await mone.edit(f"Find gdrive setup instructions for leech2drive [here]({telegraph}).")
        return
    if os.path.isfile(input_str):
        # Check if token file exists, if not create it by requesting authorization code
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            await mone.edit("Please follow instructions sent logger group.\nTimeout = 60seconds.")
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL for download
        # http = authorize(G_DRIVE_TOKEN_FILE, None)
        file_name, mime_type = file_ops(required_file)
        # required_file_name will have the full path
        # Sometimes API fails to retrieve starting URI, we wrap it.
        try:
            g_drive_link = await upload_file(http, required_file, file_name, mime_type, mone, None)
            await mone.edit(f"Required file: {g_drive_link}")
        except Exception as e:
            await mone.edit(f"Oh snap! Looks like something went wrong!")
        return
    elif os.path.isdir(input_str):
        # TODO: remove redundant code
        #
        if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
        # Check if token file exists, if not create it by requesting authorization code
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            await mone.edit("Please follow instructions sent in logger group.\nTimeout = 60seconds.")
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL for download
        # first, create a sub-directory
        dir_id = await create_directory(http, os.path.basename(os.path.abspath(input_str)), G_DRIVE_F_PARENT_ID)
        await DoTeskWithDir(http, input_str, mone, dir_id)
        dir_link = "https://drive.google.com/folderview?id={}".format(dir_id)
        await mone.edit(f"Done! Click [here]({dir_link}) to download the file from gdrive.")

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
    async with event.client.conversation(Config.PRIVATE_GROUP_BOT_API_ID) as conv:
        await conv.send_message(f"Go to the following link in your browser: {authorize_url} and reply the code")
        response = conv.wait_event(events.NewMessage(
            outgoing=True,
            chats=Config.PRIVATE_GROUP_BOT_API_ID
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
        "description": "Uploaded using @UniBorg gDrive v2",
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
    LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
    await borg.send_message(LOGGER, text)


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

SYNTAX.update({
    "leech2drive": "\
**Requested Module --> leech2drive**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.l2d <magnet-link> (or as a reply to a magnet link)```\
\nUsage: Mirrors the torrent to gdrive.\
\n\n```.l2d setup```\
\nUsage: Get gdrive setup guide.\
"
})

SYNTAX.update({
    "leech": "\
**Requested Module --> leech**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.leech <magnet-link> (or as a reply to a magnet link)```\
\nUsage: Downloads the torrent to the local machine.\
"
})

SYNTAX.update({
    "leech2tg": "\
**Requested Module --> leech2tg**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.l2tg <magnet-link> (or as a reply to a magnet link)```\
\nUsage: Uploads the torrent to telegram (TG API limitations might cause problems, don't blame me :P)..\
"
})
