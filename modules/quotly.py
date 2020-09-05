# For The-TG-Bot v3
# By Priyam Kalra
# Syntax (.quotly <text_to_quote>)

from io import BytesIO
from PIL import Image
import telethon


@client.on(events(pattern="quotly ?(.*)"))
async def handler(event):
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
    async with client.conversation(username, timeout=10) as bot_conv:
        try:
            if input_str:
                response = await silently_send_message(bot_conv, quote)
            elif reply:
                response = bot_conv.wait_event(telethon.events.NewMessage(
                    incoming=True, from_users=1031952739))
                await client.forward_messages(username, quote)
                response = await response
                response = response.message
            if response.text.startswith("Command"):
                await event.edit(f"Invalid message type.")
                return
            await event.reply(response)
            await event.delete()
        except:
            return await event.edit("`@QuotLyBot doesn't want to talk to me, try again later.`")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


ENV.HELPER.update({
    "quotly": "\
```.quotly <text_to_quote> [or as a reply to a message to quote]```\
\nUsage: Quotes the target message.\nUses @QuotLyBot.\
"
})
