# For The-TG-Bot v3
# Syntax (.afk <optional reason>)"

import asyncio
import datetime
from telethon.tl import functions, types


client.storage.USER_AFK = {}
client.storage.afk_time = None
client.storage.last_afk_message = {}
@client.on(events(outgoing=True))
async def set_not_afk(event):
    current_message = event.message.message
    if "afk" not in current_message.lower() and "yes" in client.storage.USER_AFK:
        client.storage.USER_AFK = {}
        client.storage.afk_time = None


@client.on(events(pattern="afk ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not client.storage.USER_AFK:
        last_seen_status = await client(
            functions.account.GetPrivacyRequest(
                types.InputPrivacyKeyStatusTimestamp()
            )
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            client.storage.afk_time = datetime.datetime.now()
        client.storage.USER_AFK.update({"yes": reason})
        if reason:
            await event.edit(f"**I'm goin' afk cuz {reason}.**")
        else:
            await event.edit(f"**I'm goin' afk.**")
        await asyncio.sleep(5)


@client.on(events(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk(event):
    if event.fwd_from:
        return
    afk_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        return False
    if client.storage.USER_AFK and not (await event.get_sender()).bot:
        reason = client.storage.USER_AFK["yes"]
        if client.storage.afk_time:
            now = datetime.datetime.now()
            datime_since_afk = now - client.storage.afk_time
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                afk_since = f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = f"**I have been AFK since** {afk_since} " + \
            f"**cuz {reason}, feel free to chat with this bot as long as you like, it will keep repeating itself tho.**" \
            if reason \
            else f"**I have been AFK since** {afk_since}, feel free to chat with this bot as long as you like, it will keep repeating itself tho."
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in client.storage.last_afk_message:
            await client.storage.last_afk_message[event.chat_id].delete()
        client.storage.last_afk_message[event.chat_id] = msg


ENV.HELPER.update({
    "afk": "\
```.afk <optional_reason>```\
\nUsage: Automatically replies to pms and mentions while your away.\
\nTIP: You need to set `LOGGER_GROUP` ENV variable for proper fucntioning.\
"
})
