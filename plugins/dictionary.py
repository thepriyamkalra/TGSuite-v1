# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not diwordibuted with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# For The-TG-Bot-3.0
# Modified by @authoritydmc
# Modified by Priyam Kalra 6/21/2020
# Syntax .search <text>

import asyncurban
from userbot import syntax


@bot.on(command("dictionary (.*)"))
async def _(event):
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


syntax.update({
    "dictionary": "\
```.dictionary <keyword>```\
\nUsage: Search UrbanDictionary for a selected keyword.\
"})
