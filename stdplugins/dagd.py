# For UniBorg
# Syntax shorten, unshorten

from telethon import events
import os
import requests
import json
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("dagd")


@borg.on(admin_cmd(pattern="shorten (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("Generated {} for {}.".format(response_api, input_str))
    else:
        await event.edit("Error! Please try again later")


@borg.on(admin_cmd(pattern="unshorten (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith('3'):
        await event.edit("Input URL: {}\nReDirected URL: {}".format(input_str, r.headers["Location"]))
    else:
        await event.edit("Input URL {} returned status_code {}".format(input_str, r.status_code))


SYNTAX.update({
    "dagd": "\
**Requested Module --> dagd**\
\nDetailed usage of fuction(s):\
\n\n```.shorten <input_link>```\
\nUsage: Create a shortened da.gd link using <input_link>.\
\n\n```.unshorten <da.gd link>```\
\nUsage: Unshorten a da.gd link.\
"
})
