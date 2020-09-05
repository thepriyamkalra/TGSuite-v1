# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not diwordibuted with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# For The-TG-Bot v3
# Modified by @authoritydmc
# Modified by @justaprudev 30/08/2020
# Syntax .ud <text>

import asyncurban


@client.on(events("ud (.*)"))
async def handler(event):
    if event.fwd_from:
        return
    word = event.pattern_match.group(1)
    urbandict = asyncurban.UrbanDictionary()
    await event.edit(f"Searching UrbanDictionary for ```{word}```..")
    try:
        mean = await urbandict.get_word(word)
        await event.edit("Text: **{}**\n\nMeaning: **{}**\n\nExample: __{}__".format(mean.word, mean.definition, mean.example))
    except asyncurban.WordNotFoundError:
        await event.edit("No result found for **" + word + "**")


ENV.HELPER.update({
    "ud": "\
```.ud <keyword>```\
\nUsage: Search UrbanDictionary for a selected keyword.\
"})
