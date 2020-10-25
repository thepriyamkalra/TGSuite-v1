# For The-TG-Bot v3
# By @Techy05

import asyncio
from telethon.tl.functions.users import GetFullUserRequest


@client.on(events("(gban|ungban) ?(.*)"))
async def ungban(event):
    cmd = event.pattern_match.group(1)
    user = await get_user(event)
    if user is None:
        return await event.edit(f"`Who do you want me to {cmd}!?`")
    await event.edit("`Globally {}ning this person..`".format(cmd.replace("g", "")))
    chats = await editperms(user, view_messages=False) if cmd == "gban" else await editperms(user)
    mention = await fulluser(user)
    await event.edit("**{0}ned** {1} **in** {2} **chats!**".format(
        cmd.replace("g", "").capitalize(), mention, len(chats)))
    await asyncio.sleep(2)
    await client.send_message(ENV.LOGGER_GROUP, "**{0}ned** {1} **in:**\n\n{2}".format(cmd.capitalize(), mention, "\n".join(chats)))


@client.on(events("(gmute|ungmute) ?(.*)"))
async def ungban(event):
    cmd = event.pattern_match.group(1)
    user = await get_user(event)
    if user is None:
        return await event.edit(f"`Who do you want me to {cmd}!?`")
    await event.edit("`Globally {}ing this person..`".format(cmd.replace("g", "").strip("e")))
    chats = await editperms(user, send_messages=False) if cmd == "gmute" else await editperms(user)
    mention = await fulluser(user)
    await event.edit("**{0}d** {1} **in** {2} **chats!**".format(
        cmd.replace("g", "").capitalize(), mention, len(chats)))
    await asyncio.sleep(2)
    await client.send_message(ENV.LOGGER_GROUP, "**{0}d** {1} **in:**\n\n{2}".format(cmd.capitalize(), mention, "\n".join(chats)))



async def get_user(event):
    reply = await event.get_reply_message()
    input = event.pattern_match.group(2)
    user = reply.from_id if reply else (input if input else None)
    return user

async def editperms(user, send_messages=True, view_messages=True):
    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            try:
                if dialog.entity.admin_rights:
                    await client.edit_permissions(dialog.id, user, send_messages=send_messages, view_messages=view_messages)
                    chats.append(dialog.name)
            except:
                continue
    return chats

async def fulluser(id):
    user = await client(GetFullUserRequest(id))
    link = f"[{user.user.first_name}](tg://user?id={user.user.id})"
    return link


ENV.HELPER.update({"gban": "\
`.gban [user/reply]`\
\nUsage: Bans someone in all the chats in which you are admin.\
\n\n`.ungban [user/reply]`\
\nUsage: Unbans someone in all the chats in which you are admin.\
\n\n`.gmute [user/reply]`\
\nUsage: Mutes someone in all the chats in which you are admin.\
\n\n`.ungmute [user/reply]`\
\nUsage: Unmutes someone in all the chats in which you are admin.\
"})
