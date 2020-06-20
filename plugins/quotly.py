# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax (.quotly <text_to_quote>)

from io import BytesIO
from PIL import Image
from telethon import events 
from userbot import syntax


@bot.on(command(pattern="quotly ?(.*)"))
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
    username = "@QuotLyBot"
    await event.edit(f"```Quoting this message...```")
    async with bot.conversation(username) as bot_conv:
        if True:  # lazy indentation workaround xD
            if input_str:
                response = await silently_send_message(bot_conv, quote)
            elif reply:
                response = bot_conv.wait_event(events.NewMessage(
                    incoming=True, from_users=1031952739))
                await bot.forward_messages(username, quote)
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


syntax.update({
    "quotly": "\
```.quotly <text_to_quote> [or as a reply to a message to quote]```\
\nUsage: Quotes the target message.\nUses @QuotLyBot.\
"
})
