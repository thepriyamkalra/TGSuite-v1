# For The-TG-Bot v3
# By Priyam Kalra

import os
from asyncio import sleep
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, FloodWaitError
from telethon.errors import ChannelPrivateError

if not hasattr(client.storage, "MESSAGE_REPO"):
    client.storage.MESSAGE_REPO = False


async def authorize(event):
	try:
		chat = await event.get_chat()
		tag = f"@{chat.username}"
		if tag in ENV.UNLOCKED_CHATS:
			if event.sticker:
				return True
			elif event.gif:
				return True
	except:
		pass
	return False


@client.on(events(outgoing=True, func=authorize))
async def sticker_unlock(event):
    chat = "@msgrepo"
    reply = await event.get_reply_message()
    media_repr = "GIF" if event.gif else "Sticker"
    media = event.message
    if not client.storage.MESSAGE_REPO:
        try:
            await client(JoinChannelRequest(channel=chat))
        except ChannelPrivateError:
            return await event.edit(f"Chat not found!")
        except FloodWaitError as e:
            return await event.reply(f"Too many requests, try again after {e.seconds} seconds.")
        finally:
            client.storage.MESSAGE_REPO = True
    try:
        message = await client.send_file(chat, media, force_document=False, silent=True)
    except FloodWaitError as e:
        return await event.reply(f"Too many requests, try again after {e.seconds} seconds.")
    await client.send_message(event.chat_id, f"[{media_repr}](t.me/{chat[1:]}/{message.id})", reply_to=reply, link_preview=True)
    await event.delete()
    await sleep(2)
    await message.delete()

# Keep the chat clean
@client.on(events(incoming=True, func=lambda e: e.chat_id == -1001333923754))
async def clean_chat(e):
    if e.sticker or e.gif:
        await sleep(2)
    await e.delete()

ENV.HELPER.update({
    "unlocker": "\
Usage: Worksaround bot \"admin-only\" locks in chats.\
\nNote: This will only work if links arent filtred.\
\nWhat can be sent in chats where its locked (for now):\
\n- Stickers\
\n- GIFS\
\n\nYou need to add a chat to `UNLOCKED_CHATS` enviroment variable for this to take effect in those chats.\
"
})
