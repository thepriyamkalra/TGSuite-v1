from os import path, remove
from random import randint
import time
from dropbox import dropbox
import asyncio
from telethon.tl import functions
from uniborg.util import admin_cmd
from datetime import datetime
from telethon import events
from uniborg.util import admin_cmd, progress
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, LOGGER

MODULE_LIST.append("ipadrop")
token_file = Config.DROPBOX_TOKEN


@borg.on(admin_cmd(pattern="ipadrop ?(.*)"))
async def ipadrop(event):
    if event.fwd_from:
        return
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
            await event.edit(f"Downloaded IPA to {downloaded_file_name}.")
            ipa_split = downloaded_file_name.split("/")
            ipa = ipa_split[2]
    if not path.exists(ipa):
        await event.edit("404: IPA not found!")
        return
    else:
        ipa_link = await upload(ipa, mesg=event)
        ipa_dl_link = get_dl_link(ipa_link)
        get_plist(ipa_dl_link, ipa)
        idnum = randint(101, 9999999999)
        manifest = f"manifest_{idnum}.plist"
        with open(manifest, "w") as f:
            f.write(plist)
        manifest_link = await upload(manifest, mesg=event, num=idnum)
        manifest_dl_link = get_dl_link(manifest_link)
        final_link = "itms-services://?action=download-manifest&url=" + manifest_dl_link
        message = f"\nRun this link in safari to install {ipa[:-4]}:\n`{final_link}`"
        await event.edit(message)
        await log(message)
        remove(manifest)
        remove(ipa)


async def log(text):
    await borg.send_message(LOGGER, text)


def get_dl_link(link):
    if not link.startswith("https://www.dropbox.com/s/"):
        return link
    link = link[26:]
    if link.endswith("?dl=0"):
        link = link[:-5]
    dl_link = "https://dl.dropboxusercontent.com/s/" + link
    return dl_link


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
                CHUNK_SIZE = 1 * 1024 * 1024
                if file_size <= CHUNK_SIZE:
                    await msg.edit(f"Processing {filename}..")
                    dbx.files_upload(f.read(), dest_path)
                else:
                    upload_session_start_result = dbx.files_upload_session_start(
                        f.read(CHUNK_SIZE))
                    progress = int(CHUNK_SIZE/file_size*100)
                    if msg != None:
                        await msg.edit(f"Processing {filename}: {progress}%")
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id, offset=f.tell())
                    commit = dropbox.files.CommitInfo(path=dest_path)
                    while f.tell() < file_size:
                        if ((file_size - f.tell()) <= CHUNK_SIZE):
                            dbx.files_upload_session_finish(
                                f.read(CHUNK_SIZE), cursor, commit)
                            await msg.edit(f"Processing {filename}: 100%")
                        else:
                            dbx.files_upload_session_append(
                                f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                            cursor.offset = f.tell()
                            progress = int(f.tell()/file_size*100)
                            await msg(f"Processing {filename}: {progress}%")
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                dest_path)
            link = shared_link_metadata.url
            return link
        except FileNotFoundError:
            return False


async def upload(ipa_path, mesg, num=None):
    access_token = token_file
    transferData = TransferData(access_token)
    file_from = ipa_path
    file_to = f"/IPAdropTG/{file_from}"
    link = await transferData.upload_file(file_from, file_to, msg=mesg, idnum=num)
    return link


def get_plist(ipaurl, ipaname):
    global plist, name
    if "/" in ipaname:
        name_split = name.split("/")
        name = name_split[-1]
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
\n\n```.ipadrop <as a reply to IPA file>```\
\nUsage: Reply to an ipa file to get an OTA installation link.\
"
})
