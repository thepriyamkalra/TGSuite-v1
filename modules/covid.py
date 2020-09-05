# For The-TG-Bot v3

from telethon.errors.rpcerrorlist import YouBlockedUserError

@client.on(events(pattern="covid ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return 
    country = event.pattern_match.group(1)
    if not country:
        await event.edit("Thats not how it works. Use `.help covid` for more info.")
        return
    await event.edit("`Fetching information..`")
    bot = "@HarukaAyaBot"
    async with client.conversation(bot) as bot_conv:
        try:
            response = await silently_send_message(bot_conv, "/covid " + country)
            await client.send_message(event.chat_id, response.text)
            await event.delete()
        except YouBlockedUserError:
            await event.edit("`Start` @HarukaAyaBot `for proper functioning.`")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response

ENV.HELPER.update({"covid": "\
`.covid <country>`\
\n\nUsage: Fetches latest covid19 statistics for a specific country using @HarukaAyaBot\
"})
