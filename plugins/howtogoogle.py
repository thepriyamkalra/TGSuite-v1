#Modded from dagd.py
"""
Animate How To Google
Command .ggl Search Query
By @loxxi
"""

from telethon import events
import os
import requests
import json
from userbot import syntax


@bot.on(command("ggl ?(.*)"))
async def func(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(input_str.replace(" ","+"))
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("[{}]({})\n`Thank me Later 🙃` ".format(input_str,response_api.rstrip()))
    else:
        await event.edit("something is wrong. please try again later.")
        
        
syntax.update({
    "howtogoogle": "\
• `.ggl <query>`\
\nUsage: A guide on how to search on google.\
"
})
