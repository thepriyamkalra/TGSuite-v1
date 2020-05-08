# For The-TG-Bot 2.0
# By Priyam Kalra
# Syntax .ipadrop <ipa_direct_link> [or as a reply to IPA file]


import time
import requests
import asyncio
from random import randint
from telethon import events
from os import path, remove
from dropbox import dropbox
from datetime import datetime
from telethon.tl import functions
from uniborg.util import admin_cmd, progress
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, LOGGER

# Global Variables
MODULE_LIST.append("ipadrop")
token_file = Config.DROPBOX_TOKEN

# Driver code
@borg.on(admin_cmd(pattern="ipadrop ?(.*)"))
async def ipadrop(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1)
    idnum = randint(101, 9999999999)
    ipa = await download(args, event, idnum)
    if not path.exists(ipa):
        await event.edit("404: IPA not found!")
        return
    else:
        ipa_link = await upload(ipa, event)
        ipa_dl_link = get_dl_link(ipa_link)
    get_plist(ipa_dl_link, ipa)
    manifest = f"manifest_{name}.plist"
    with open(manifest, "w") as f:
        f.write(plist)
    manifest_link = await upload(manifest, event, idnum)
    manifest_dl_link = get_dl_link(manifest_link)
    final_link =  get_itunes_link(manifest_dl_link)
    message = f"\nRun this link in safari to install `{name}`:\n`{final_link}`\nIf the app icon is grey after installation, the IPA file has expired."
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
            remove(i)
        except FileNotFoundError:
            pass


# Returns an itunes link which can be used for on-air installation
def get_itunes_link(link):
    itunes_prefix = "itms-services://?action=download-manifest&url="
    itunes_link = itunes_prefix + link
    return itunes_link


# Converts dropbox sharing link into usercontent link
def get_dl_link(link):
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
            ipa = ipa_split[2]
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


# Uploads data to dropbox and returns sharing link
class TransferData:
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
                file_size = path.getsize(file_path)
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


# Initialization for dropbox upload
async def upload(ipa_path, mesg, num=None):
    access_token = token_file
    transferData = TransferData(access_token)
    file_from = ipa_path
    file_to = f"/IPAdropTG/{file_from}"
    link = await transferData.upload_file(file_from, file_to, msg=mesg, idnum=num)
    return link


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
					<string>https://raw.githubusercontent.com/Priyam005/IPAdrop/master/icon.png</string>
				</dict>
               <dict>
                   <key>kind</key>
                   <string>display-image</string>
                   <key>needs-shine</key>
                   <true/>
                   <key>url</key>
                   <string>https://raw.githubusercontent.com/Priyam005/IPAdrop/master/icon.png</string>
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
    "ipadrop": "\
**Requested Module --> ipadrop**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.ipadrop <ipa_direct_link> [or as a reply to IPA file]```\
\nUsage: Provide a direct link or reply to an IPA file to get an OTA app installation link.\
"
})
