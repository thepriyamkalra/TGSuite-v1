# For The-TG-Bot v3
# Syntax (.promote <optional_rank>, .demote, .ban, .unban, .mute, .unmute, .kick, .kickme, .pin)

from telethon.tl.functions.users import GetFullUserRequest

SUDO_STR = "**That guy is my friend, not going to touch him!**"
NO_USER = "Who do you want me to {0}?!"

@client.on(events(pattern="promote ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        user = reply.from_id
        rank = input_str if input_str else None
    else:
        if input_str:
            user = input_str.split()[0]
            try:
                rank = input_str.split()[1]
            except:
                rank = None
        else:
            return await event.edit("`You deserve a demotion!`")
    try:
        await client.edit_admin(event.chat_id, user,
            is_admin=True, title=rank, ban_users=False, add_admins=False)
        await event.edit(f"`Say hello to` {await user_entity(user)}`, our new \"{rank}\"!`")
    except (Exception) as exc:
        await event.edit(str(exc))

@client.on(events(pattern="demote ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    user = await get_user(event)
    if not user:
        return await event.edit(NO_USER.format("demote"))
    elif user in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            await client.edit_admin(event.chat_id, user, is_admin=False)
            await event.edit(f"Oh boy, {await user_entity(user)} has been demoted!")
        except (Exception) as exc:
            await event.edit(str(exc))


@client.on(events(pattern="ban ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    participant = await get_user(event)
    if not participant:
        return await event.edit(NO_USER.format("ban"))
    elif participant in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            await client.edit_permissions(event.chat_id, participant, view_messages=False)
            await event.edit(f"Gone, {await user_entity(participant)} is gone!")
        except (Exception) as exc:
            await event.edit(str(exc))

@client.on(events("unban ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    participant = await get_user(event)
    if not participant:
        return await event.edit(NO_USER.format("unban"))
    else:
        try:
            await client.edit_permissions(event.chat_id, participant)
            await event.edit(f"Well, {await user_entity(participant)} can join now!")
        except (Exception) as exc:
            await event.edit(str(exc))


@client.on(events("mute ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    participant = await get_user(event)
    if not participant:
        return await event.edit(NO_USER.format("mute"))
    elif participant in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            await client.edit_permissions(event.chat_id, participant, send_messages=False)
            await event.edit(f"Successfully taped {await user_entity(participant)}!")
        except (Exception) as exc:
            await event.edit(str(exc))

@client.on(events("unmute ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    participant = await get_user(event)
    if not participant:
        return await event.edit(NO_USER.format("unmute"))
    else:
        try:
            await client.edit_permissions(event.chat_id, participant)
            await event.edit(f"Okay, {await user_entity(participant)} is no longer taped!")
        except (Exception) as exc:
            await event.edit(str(exc))


@client.on(events("kick ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    participant = await get_user(event)
    if not participant:
        return await event.edit(NO_USER.format("kick"))
    elif participant == "me":
        await event.edit("`Sayonara, cruel world!`")
        await client.kick_participant(event.chat_id, "me")
    elif participant in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            await client.kick_participant(event.chat_id, participant)
            await event.edit(f"{await user(participant)} has been yeeted!")
        except (Exception) as exc:
            await event.edit(str(exc))


@client.on(events("pin ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    if event.text.split()[0][1:] != "pin":
        return
    reply = await event.get_reply_message()
    silent = False if "loud" in event.text else True
    if reply:
        try:
            await reply.pin(notify=silent)
            await event.delete()
        except Exception as error:
            await event.edit(str(error))
    else:
        return await event.edit("`Reply to a message to pin it.`")


# Helpers
async def get_user(event):
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if reply:
        user = reply.from_id
    elif input_str:
        user = input_str
    else:
        user = None
    return user

async def user_entity(id):
    entity = await client(GetFullUserRequest(id))
    name = entity.user.first_name
    user_id = entity.user.id
    USER = f"[{name}](tg://user?id={user_id})"
    return USER


ENV.HELPER.update({
    "admin": "\
`.promote <user/reply> <optional_title>`\
\nUsage: Promotes target user.\
\n\n`.demote <user/reply>`\
\nUsage: Demotes target user.\
\n\n`.ban <user/reply>`\
\nUsage: Bans target user.\
\n\n`.unban <user/reply>`\
\nUsage: Unbans target user.\
\n\n`.mute <user/reply>`\
\nUsage: Mutes target user.\
\n\n`.unmute <user/reply>`\
\nUsage: Unmutes target user.\
\n\n`.kick <user/reply>`\
\nUsage: Kicks target user.\
\n\n`.kickme`\
\nUsage: Kicks yourself.\
\n\n`.pin` (as a reply to a message)\
\nUsage: Pins target msg.\
"
})
