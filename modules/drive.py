# The entire code given below is verbatim copied from
# https://github.com/cyberboysumanjay/Gdrivedownloader/blob/master/gdrive_upload.py
# there might be some changes made to suit the needs for this repository
# Licensed under MIT License
# For The-TG-Bot v3
# Modified by Priyam Kalra 6/21/2020
# Syntax: .drive

import asyncio
import json
import math
import os
import time
from datetime import datetime
import telethon
from mimetypes import guess_type
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import file, tools
import httplib2


G_DRIVE_TOKEN_FILE = ENV.DOWNLOAD_DIRECTORY + "/auth_token.txt"
CLIENT_ID = ENV.DRIVE_CLIENT_ID
CLIENT_SECRET = ENV.DRIVE_CLIENT_SECRET
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
G_DRIVE_F_PARENT_ID = None
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
TELEGRAPH_LINK = "https://da.gd/drive"


@client.on(events(pattern="drive ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    mone = await event.edit("Uploading file to Google Drive..")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit(f"This module requires credentials from https://da.gd/so63O. Aborting!\nVisit {TELEGRAPH_LINK} for more info.")
        return
    if ENV.LOGGER_GROUP is None:
        await event.edit("Please set the required environment variable `LOGGER_GROUP` for this plugin to work.")
        return
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(ENV.DOWNLOAD_DIRECTORY):
        os.makedirs(ENV.DOWNLOAD_DIRECTORY)
    required_file_name = None
    start = datetime.now()
    if event.reply_to_msg_id and not input_str:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await client.download_media(
                reply_message,
                ENV.DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:
            await mone.edit(str(e))
            return False
        else:
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = downloaded_file_name
            await mone.edit("Downloaded file to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = input_str
            # await mone.edit("Found `{}` in {} seconds.".format(input_str, ms))
        else:
            await mone.edit("404: File not found!")
            return False
    if required_file_name:
        if ENV.DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(ENV.DRIVE_AUTH_TOKEN_DATA)
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        file_name, mime_type = file_ops(required_file_name)
        try:
            g_drive_link = await upload_file(http, required_file_name, file_name, mime_type, mone, G_DRIVE_F_PARENT_ID)
            await mone.edit(f"File sucessfully uploaded to Google Drive.\nDownload link: {g_drive_link}")
        except Exception as e:
            await mone.edit(f"Oh snap looks like something went wrong:\n{e}")
    else:
        await mone.edit("404: File not found.")


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
        response = conv.wait_event(telethon.events.NewMessage(
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
        "description": "Uploaded using @The_TG_Bot v3",
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

ENV.HELPER.update({"drive": f"\
```.drive (as a reply to a file on telegram)```\
\nUsage: Upload a file on telegram to your google drive.\
\n\nYou need DRIVE_CLIENT_ID and DRIVE_CLIENT_SECRET env variables for this to work.\
\nGet them client id and secret from https://console.developers.google.com/\
\nVisit {TELEGRAPH_LINK} for more information about how to set this up.\
"})
