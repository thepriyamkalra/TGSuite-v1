# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

from userbot import syntax
from telethon import events
import re
from requests import get
from bs4 import BeautifulSoup

GITHUB = 'https://github.com'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@bot.on(command("magisk ?(.*)"))
async def magisk(event):
    if event.fwd_from:
        return
    """ magisk latest releases """
    magisk_dict = {
        "Stable":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta":
        "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json"
    }
    releases = 'Latest Magisk Releases:\n'
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]})  |  ' \
                    f'[APK v{data["app"]["version"]}]({data["app"]["link"]})  |  ' \
                    f'[Uninstaller]({data["uninstaller"]["link"]})\n'
    await event.edit(releases)



@borg.on(events.NewMessage(pattern=r"\.twrp", outgoing=True))
async def twrp(event):
    if event.fwd_from:
        return
    """ get android device twrp """
    textx = await event.get_reply_message()
    device = event.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(' ')[0]
    else:
        await event.edit("`Usage: .twrp <codename>`")
        return
    url = get(f'https://dl.twrp.me/{device}/')
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await event.edit(reply)
        return
    page = BeautifulSoup(url.content, 'lxml')
    download = page.find('table').find('tr').find('a')
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = f'**Latest TWRP for {device}:**\n' \
        f'[{dl_file}]({dl_link}) - __{size}__\n' \
        f'**Updated:** __{date}__\n'
    await event.edit(reply)


syntax.update({
    "android": "\
**Requested module --> Android**\
\n\n```.magisk```\
\nUsage: Get latest Magisk releases\
\n\n```.twrp <codename>```\
\nUsage: Get latest twrp download for android device.\
"
})
