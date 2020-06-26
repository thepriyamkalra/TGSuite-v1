#By @XtraModZ geng
"""Emoji

Available Commands:
.WTF
.gei"""

import asyncio

@bot.on(command("WTF ?(.*)"))
async def _(tf):
    if tf.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    animation_chars = [
        "**What**",
        "**What The**",
        "**What The F**",
        "**What The F**, __Brah__?"
    ]

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await tf.edit(animation_chars[i % 4])



#Module made for mocking Priyam.
#Sorry Priyam, Don't take it seriously XD
#Syntax .gei"""

import asyncio

@bot.on(command("gei ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    thing = event.pattern_match.group(1)
    if not thing:
        ton = await event.get_reply_message()
        thing = ton.text
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    animation_chars = [
        f"**“{thing}**",
        f"**“{thing} Is**",
        f"**“{thing} Is Gei”**",
        f"**“{thing} Is Gei”** __- Priyam Kalra__"
    ]

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])
