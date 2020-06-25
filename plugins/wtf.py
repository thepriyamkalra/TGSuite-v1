#By X-tra-Telegram Modz Geng
"""Emoji

Available Commands:

.WTF

.gei"""

from telethon import events

import asyncio

from userbot.utils import admin_cmd

@borg.on(admin_cmd("(.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    input_str = event.pattern_match.group(1)
    if input_str == "WTF":
        await event.edit(input_str)
        animation_chars = [
            "**What**",
            "**What The**",
            "**What The F**",
            "**What The F**, __Dude__?"
        ]

        for i in animation_ttl:
        	
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])



#Module made for mocking Priyam.
#Sorry Priyam, Don't take it seriously XD
#Syntax .gei"""

from telethon import events

import asyncio

from userbot.utils import admin_cmd

@borg.on(admin_cmd("(.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    input_str = event.pattern_match.group(1)
    if input_str == "gei":
        await event.edit(input_str)
        animation_chars = [
            "**“It**",
            "**“It Is**",
            "**“It Is Gei”**",
            "**“It Is Gei”** __- Priyam Kalra__"
        ]

        for i in animation_ttl:
        	
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])
