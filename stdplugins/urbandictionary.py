# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# For UniBorg
# Syntax .search <text>
from telethon import events
import urbandict
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("urbandictionary")


@borg.on(admin_cmd("search (.*)"))
async def _(event):
    if event.fwd_from:
        return
    str = event.pattern_match.group(1)
    await event.edit(f"Searching UrbanDictionary for ```{str}```..")
    try:
        mean = urbandict.define(str)
        if len(mean) > 0:
            await event.edit(
                'Text: **' +
                str +
                '**\n\nMeaning: **' +
                mean[0]['def'] +
                '**\n\n' +
                'Example: \n__' +
                mean[0]['example'] +
                '__'
            )
        else:
            await event.edit("No result found for **" + str + "**")
    except:
        await event.edit("No result found for **" + str + "**")


SYNTAX.update({
    "urbandictionary": "\
**Requested Module --> urbandictionary**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.search <keyword>```\
\nUsage: Search UrbanDictionary for a selected keyword.\
"
})
