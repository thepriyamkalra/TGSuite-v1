# For UniBorg
# By Priyam Kalra
# Syntax (.quotly <text_to_quote>)
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST
from telethon import events
from telethon.tl import functions, types
from uniborg.util import admin_cmd
from io import BytesIO
from PIL import Image

MODULE_LIST.append("quotly")


@borg.on(admin_cmd(pattern="quotly ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        quote = input_str
    elif reply:
        quote = reply
    else:
        return
    bot = "@QuotLyBot"
    await event.edit(f"```Quoting this message...```")

    async with borg.conversation(bot) as bot_conv:
        if True:
            response = await silently_send_message(bot_conv, "/start")
            if not response.text.startswith("**Hi!**"):
                await event.edit(f"{response.text}")
                return
            if input_str:
              response = await silently_send_message(bot_conv, quote)
            elif reply:
              response = bot_conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
              await borg.forward_messages(bot, quote)
              response = await response
              response = response.message
            if response.text.startswith("Command"):
                await event.edit(f"Invalid message type.")
                return
            await event.reply(response)
            await event.delete()


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


SYNTAX.update({
    "quotly": "\
**Requested Module --> quotly**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.quotly <text_to_quote> [or as a reply to a message to quote]```\
\nUsage: Quotes the target message.\nUses @QuotLyBot.\
"
})
