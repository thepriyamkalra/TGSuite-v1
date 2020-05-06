from os import system, path, remove
from getpass import getpass
from subprocess import run, DEVNULL
from random import randint
from time import sleep
from dropbox import dropbox
import asyncio
from telethon.tl import functions
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST, DL, LOGGER

token_file = Config.DROPBOX_TOKEN
temp_dir = DL


@borg.on(admin_cmd(pattern="ipadrop ?(.*)"))
async def ipadrop(event):
    if event.fwd_from:
        return
    ipa = event.pattern_match.group(1)
    if not path.exists(ipa):
        await event.edit("404: File not found!")
        return
    else:
        ipa_link = await upload(ipa, mesg=event)
        ipa_dl_link = get_dl_link(ipa_link)
        get_plist(ipa_dl_link, ipa)
        idnum = randint(101, 9999999999)
        manifest = f"{temp_dir}IPAdrop/manifest_{idnum}"
        with open(manifest) as f:
            f.write(plist)
        manifest_link = await upload(manifest, mesg=event)
        manifest_dl_link = get_dl_link(manifest_link)
        final_link = "itms-services://?action=download-manifest&url=" + manifest_dl_link
        message = f"\nRun this link in safari to install your app:\n{final_link}"
        await event.edit(message)
        await log(message)


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


async def log(text):
    # LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
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

    async def upload_file(self, file_path, dest_path, msg):
        dbx = dropbox.Dropbox(self.access_token, timeout=None)
        try:
            with open(file_path, "rb") as f:
                file_size = path.getsize(file_path)
                CHUNK_SIZE = 1 * 1024 * 1024
                if file_size <= CHUNK_SIZE:
                    await msg.edit(f"Processing..")
                    dbx.files_upload(f.read(), dest_path)
                else:
                    upload_session_start_result = dbx.files_upload_session_start(
                        f.read(CHUNK_SIZE))
                    progress = int(CHUNK_SIZE/file_size*100)
                    if msg != None:
                        await msg.edit(f"Processing IPA: {progress}%")
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id, offset=f.tell())
                    commit = dropbox.files.CommitInfo(path=dest_path)
                    while f.tell() < file_size:
                        if ((file_size - f.tell()) <= CHUNK_SIZE):
                            dbx.files_upload_session_finish(
                                f.read(CHUNK_SIZE), cursor, commit)
                            await msg.edit(f"Processing IPA: 100%")
                        else:
                            dbx.files_upload_session_append(
                                f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                            cursor.offset = f.tell()
                            progress = int(f.tell()/file_size*100)
                            await msg(f"Processing IPA: {progress}%")
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                dest_path)
            link = shared_link_metadata.url
            return link
        except FileNotFoundError:
            return False


async def upload(ipa_path, mesg=None):
    access_token = token_file
    transferData = TransferData(access_token)
    file_from = ipa_path
    file_to = f"/IPAdrop_TG/{file_from}"
    link = await transferData.upload_file(file_from, file_to, msg=mesg)
    return link
