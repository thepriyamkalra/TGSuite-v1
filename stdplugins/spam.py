# For UniBorg
# By Priyam Kalra
# Syntax (.spam <number of msgs [limit = 999]> <text>)

from asyncio import wait
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


MODULE_LIST.append("spam")


@borg.on(events.NewMessage(pattern=r"\.spam", outgoing=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        if type(message[8]) == str:
            counter = int(message[6:8])
            spam_message = str(e.text[8:])
        else:
            counter = int(message[6:9])
            spam_message = str(e.text[9:])
    for spam in range(counter):
        await e.delete()
        await e.reply(spam_message)



SYNTAX.update({
    "spam": "\
**Requested Module --> spam**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.spam <number of msgs> <text>```\
\nUsage: Spam a specified message upto 999 times.\
"
})