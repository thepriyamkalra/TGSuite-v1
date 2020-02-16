# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# For UniBorg
# Syntax .search <text>
from telethon import events
import asyncurban
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("ud (urbandictionary)")

@borg.on(admin_cmd("ud (.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("processing...")
    word = event.pattern_match.group(1)
    urban = asyncurban.UrbanDictionary()
    try:
        mean = await urban.get_word(word)
        await event.edit("Text: **{}**\n\nMeaning: **{}**\n\nExample: __{}__".format(mean.word, mean.definition, mean.example))
    except asyncurban.WordNotFoundError:
        await event.edit("No result found for **" + word + "**")

SYNTAX.update({
    "ud": "\
**Requested Module --> urbandictionary**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.ud <keyword>```\
\nUsage: Search UrbanDictionary for a selected keyword.\
"
})
