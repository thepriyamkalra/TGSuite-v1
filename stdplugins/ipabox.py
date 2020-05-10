# For The-TG-Bot 2.0
# By Priyam Kalra
# Syntax .ipadrop <ipa_direct_link> [or as a reply to IPA file]


import os
import math
import time
import asyncio
import httplib2
import requests
from random import randint
from telethon import events
from dropbox import dropbox
from datetime import datetime
from mimetypes import guess_type
from telethon.tl import functions
from oauth2client.file import Storage
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client import file, client, tools
from uniborg.util import admin_cmd, progress
from apiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, LOGGER

# Global Variables
MODULE_LIST.append("ipadrop")
G_DRIVE_TOKEN_FILE = Config.TMP_DOWNLOAD_DIRECTORY + "/auth_token.txt"
CLIENT_ID = Config.G_DRIVE_CLIENT_ID
CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
folder_link = Config.IPABOX_FOLDER
folder_id = None
if folder_link is not None:
    if folder_link.endswith("?usp=sharing"):
        folder_link = folder_link[:-12]
    link_split = folder_link.split("/")
    link = link_split[-1]
    if link.startswith("open?id="):
        link = link[8:]
    folder_id = link
G_DRIVE_F_PARENT_ID = folder_id
token_file = Config.DROPBOX_TOKEN
drive_acc = Config.G_DRIVE_ACCOUNT


# Select a mode - dbx or drive
@borg.on(admin_cmd(pattern="ipabox"))
async def drive(event):
    message = "Please specify as valid mode:\nUse .ipadrive to use google drive or .ipadrop to use dropbox for hosting installations."
    await event.edit(message)
    return

@borg.on(admin_cmd(pattern="ipadrop ?(.*)"))
async def dbx(event):
    if token_file is None:
        return await event.edit(f"You need to set `DROPBOX_TOKEN` enviroment variable!")
    host = "dbx"
    await main(host, event)

@borg.on(admin_cmd(pattern="ipadrive ?(.*)"))
async def drive(event):
    if drive_acc is None:
        return await event.edit(f"You need to set `G_DRIVE_ACCOUNT` enviroment variable!")
    host = "drive"
    await main(host, event)

# Main function that connects everything else together
async def main(mode, msg):
    event = msg
    args = event.pattern_match.group(1)
    idnum = randint(101, 9999999999)
    ipa = await download(args, event, idnum)
    if not os.path.exists(ipa):
        await event.edit("404: IPA not found!")
        return
    else:
        ipa_link = await upload(mode, ipa, event)
        ipa_dl_link = get_dl_link(mode, ipa_link)
    get_plist(ipa_dl_link, ipa)
    manifest = f"manifest_{name}.plist"
    with open(manifest, "w") as f:
        f.write(plist)
    manifest_link = await upload(mode, manifest, event, idnum)
    manifest_dl_link = get_dl_link(mode, manifest_link)
    final_link = get_itunes_link(manifest_dl_link)
    message = f"\nRun this link in safari to install `{name}`:\n`{final_link}`\nIf the app icon is grey after installation, the IPA file has expired."
    if G_DRIVE_F_PARENT_ID is None:
        tip = "\n\nTIP: To store all the IPAbox files in one folder, create a folder named \"IPAbox\" in the root of your drive, copy its link and paste it in env variable \"IPABOX_FOLDER\"."
        message += tip 
    await event.edit(message)
    await log(message)
    clean(ipa, manifest)


# Simple userbot logging
async def log(text):
    await borg.send_message(LOGGER, text)


# Cleans the files
def clean(*args):
    for i in args:
        try:
            os.remove(i)
        except FileNotFoundError:
            pass


# Returns an itunes link which can be used for on-air installation
def get_itunes_link(link):
    itunes_prefix = "itms-services://?action=download-manifest&url="
    itunes_link = itunes_prefix + link
    return itunes_link


# Converts dropbox sharing link into usercontent link
def get_dl_link(mode, link):
    if mode == "drive":
        drivetw_url = f"https://drv.tw/~{drive_acc}/gd/{link}"
        return drivetw_url
    elif mode == "dbx":
        if not link.startswith("https://www.dropbox.com/s/"):
            return link
        link = link[26:]
        if link.endswith("?dl=0"):
            link = link[:-5]
        dl_link = "https://dl.dropboxusercontent.com/s/" + link
        return dl_link


# Downloads data to local server and returns path
async def download(url, msg, id):
    idnum = id
    args = url
    event = msg
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                "/app/",
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "Downloading IPA..")
                )
            )
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.edit(f"Downloaded IPA to `{downloaded_file_name}`.")
            ipa_split = downloaded_file_name.split("/")
            ipa_full = ipa_split[-1]
            ipa_noext = ipa_full[:-4]
            ipa = f"{ipa_noext}_{idnum}.ipa"
            os.rename(ipa_full, ipa)
            return ipa
    elif args.startswith("http"):
        if not args.endswith(".ipa"):
            return await event.edit("Unsupported link!\nPlease provide a direct link to the IPA file.")
        ipa_split = args.split("/")
        ipa = ipa_split[-1]
        ipa_noext = ipa[:-4]
        ipa = f"{ipa_noext}_{idnum}.ipa"
        await event.edit(f"Downloading IPA: `{ipa}`")
        request = requests.get(args)
        with open(ipa, "wb") as f:
            f.write(request.content)
        return ipa


# Prepare enviroment for drive upload and return sharing link after completion
class DriveUpload:
    def __init__(self, file):
        self.file = file

    async def upload_file(self, event, idnum=None):
        filename = self.file
        filepath = filename
        if G_DRIVE_F_PARENT_ID is not None:
            filepath = f"IPAbox/{filename}"
        if filename.startswith("manifest_"):
            display_name = filename[:int(f"-{len(str(idnum))+7}")]
        elif filename.endswith(".ipa"):
            display_name = filename[:-4]
        if not filename:
            return await event.edit("404: IPA not found")
        if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        mime_type = file_ops(filename)
        try:
            await event.edit(f"Processing `{display_name}`: 0%")
            await upload_to_drive(http, filename, filename, mime_type, event, G_DRIVE_F_PARENT_ID)
            await event.edit(f"Processing `{display_name}`: 100%")
            return filepath
        except Exception as e:
            await event.edit(f"Looks like something went wrong while uploading `{display_name}` to drive: {e}")
            return


# Uploads data to dropbox and returns sharing link
class DropboxUpload:
    def __init__(self, access_token):
        self.access_token = access_token

    async def upload_file(self, file_path, dest_path, msg, idnum=None):
        dbx = dropbox.Dropbox(self.access_token, timeout=None)
        filename = file_path
        if filename.startswith("manifest_"):
            filename = filename[:int(f"-{len(str(idnum))+7}")]
        elif filename.endswith(".ipa"):
            filename = filename[:-4]
        try:
            with open(file_path, "rb") as f:
                file_size = os.path.getsize(file_path)
                CHUNK_SIZE = 5 * 1024 * 1024
                if file_size <= CHUNK_SIZE:
                    await msg.edit(f"Processing `{filename}`..")
                    dbx.files_upload(f.read(), dest_path)
                else:
                    upload_session_start_result = dbx.files_upload_session_start(
                        f.read(CHUNK_SIZE))
                    progress = int(CHUNK_SIZE/file_size*100)
                    if msg != None:
                        await msg.edit(f"Processing `{filename}`: {progress}%")
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id, offset=f.tell())
                    commit = dropbox.files.CommitInfo(path=dest_path)
                    while f.tell() < file_size:
                        if ((file_size - f.tell()) <= CHUNK_SIZE):
                            dbx.files_upload_session_finish(
                                f.read(CHUNK_SIZE), cursor, commit)
                            await msg.edit(f"Processing `{filename}`: 100%")
                        else:
                            dbx.files_upload_session_append(
                                f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                            cursor.offset = f.tell()
                            progress = int(f.tell()/file_size*100)
                            await msg.edit(f"Processing `{filename}`: {progress}%")
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                dest_path)
            link = shared_link_metadata.url
            return link
        except FileNotFoundError:
            return False


# Initialization for upload
async def upload(mode, ipa_path, mesg, num=None):
    if mode == "drive":
        origin = ipa_path
        driveupload = DriveUpload(ipa_path)
        link = await driveupload.upload_file(mesg, num)
        return link
    elif mode == "dbx":
        access_token = token_file
        dropboxupload = DropboxUpload(access_token)
        file_from = ipa_path
        file_to = f"/IPAdropTG/{file_from}"
        link = await dropboxupload.upload_file(file_from, file_to, msg=mesg, idnum=num)
        return link

# Upload data to drive
async def upload_to_drive(http, file_path, file_name, mime_type, event, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Used for hosting OTA Installations - IPAbox",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"] = [{"id": parent_id}]
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    file = drive_service.files().insert(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk()
        await asyncio.sleep(1)
        if status:
            percentage = int(status.progress() * 100)
            if display_message != percentage:  
                try:
                    await event.edit(f"Processing `{file_name}`: {percentage}%")
                    display_message = percentage
                except Exception as e:
                    logger.info(str(e))
                    pass
    file_id = response.get("id")
    try:
        drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    except:
        pass
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return file_id

# Get mime type and name of given file
def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    return mime_type

# Run through the OAuth flow and retrieve credentials
async def create_token_file(token_file, event):
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

# Get credentials
def authorize(token_file, storage):
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http

# Returns manifest/plist for app
def get_plist(ipaurl, ipaname):
    global plist, name
    name = ipaname
    if name.endswith(".ipa"):
        name = name[:-4]
    plist = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
   <key>items</key>
   <array>
       <dict>
           <key>assets</key>
           <array>
               <dict>
                   <key>kind</key>
                   <string>software-package</string>
                   <key>url</key>
                   <string>{ipaurl}</string>
               </dict>
				<dict>
					<key>kind</key>
					<string>full-size-image</string>
					<key>needs-shine</key>
					<true/>
					<key>url</key>
					<string>https://raw.githubusercontent.com/PriyamKalra/IPAbox/master/icon.png</string>
				</dict>
               <dict>
                   <key>kind</key>
                   <string>display-image</string>
                   <key>needs-shine</key>
                   <true/>
                   <key>url</key>
                   <string>https://raw.githubusercontent.com/PriyamKalra/IPAbox/master/icon.png</string>
               </dict>
           </array><key>metadata</key>
           <dict>
               <key>bundle-identifier</key>
               <string>com.{name}.app</string>
               <key>bundle-version</key>
               <string>v1.0.0</string>
               <key>kind</key>
               <string>software</string>
               <key>subtitle</key>
               <string>{name}</string>
               <key>title</key>
               <string>{name}</string>
           </dict>
       </dict>
   </array>
</dict>
</plist>
"""


SYNTAX.update({
    "ipabox": "\
**Requested Module --> ipabox**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.ipadrop <ipa_direct_link> [or as a reply to IPA file]```\
\nUsage: Provide a direct link or reply to an IPA file to host an OTA installation via dropbox.\
\n\n```.ipadrive <ipa_direct_link> [or as a reply to IPA file]```\
\nUsage: Provide a direct link or reply to an IPA file to host an OTA installation via google drive.\
"
})
