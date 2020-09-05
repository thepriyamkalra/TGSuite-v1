# For The-TG-Bot v3
# Syntax (.pin <loud (optional)>, .promote <optional_rank>, .demote, .ban, .unban, .mute, .unmute, .kick as a reply to a user's msg)

from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

SUDO_STR = "**That guy is my friend, not going to touch him!**"
NO_USER = "Who do you want me to {0}?!"


@client.on(events("pin ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    silent = True
    cmd = event.pattern_match.group(0)
    if "ping" in cmd:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "loud":
        silent = False
    if event.message.reply_to_msg_id is not None:
        message_id = event.message.reply_to_msg_id
        try:
            await client(UpdatePinnedMessageRequest(
                event.chat_id,
                message_id,
                silent
            ))
        except Exception as e:
            await event.edit(str(e))
        else:
            await event.delete()
    else:
        await event.edit("Reply to a message to pin it.")

admin_rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=False,
    invite_users=True,
    pin_messages=True,
    add_admins=False
)


@client.on(events(pattern="promote ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    admin_rank = "admeme"
    to_promote_id = None
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_promote_id = r_mesg.sender_id
        admin_rank = input_str
    elif input_str:
        to_promote_id = input_str
    else:
        await event.edit(NO_USER.format("promote"))
    try:
        to_promote_id = int(to_promote_id)
    except:
        pass
    try:
        await client(EditAdminRequest(event.chat_id, to_promote_id, admin_rights, admin_rank))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Say hello to ```{to_promote_id}```, our new admeme!")


banned_rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)


@client.on(events("(ban) ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = banned_rights
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str in input_str:
        to_ban_id = input_str
    else:
        await event.edit(NO_USER.format("ban"))
    if to_ban_id in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            to_ban_id = int(to_ban_id)
        except:
            pass
        try:
            await client(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Gone, ```{to_ban_id}``` is gone!")


demoted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=True,
    send_gifs=None,
    send_games=True,
    send_inline=None,
    embed_links=None
)


@client.on(events("(demote) ?(.*)"))
async def handler(event):

    if event.fwd_from:
        return
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "demote":
        rights = demoted_rights
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str:
        to_ban_id = input_str
    else:
        await event.edit(NO_USER.format("demote"))
    if to_ban_id in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            to_ban_id = to_ban_id
        except:
            pass
        try:
            await client(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Oh boy, ```{to_ban_id}``` has been demoted!")

muted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)


@client.on(events("(mute) ?(.*)"))
async def handler(event):

    if event.fwd_from:
        return
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "mute":
        rights = muted_rights

    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str:
        to_ban_id = input_str
    else:
        await event.edit(NO_USER.format("mute"))
    if to_ban_id in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            to_ban_id = int(to_ban_id)
        except:
            pass
        try:
            await client(EditBannedRequest(event.chat_id, to_ban_id, rights))
        except (Exception) as exc:
            await event.edit(str(exc))
        else:
            await event.edit(f"Successfully taped ```{to_ban_id}```!")


unmuted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@client.on(events("(unmute) ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "unmute":
        rights = unmuted_rights
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str:
        to_ban_id = input_str
    else:
        await event.edit(NO_USER.format("unmute"))
    try:
        to_ban_id = int(to_ban_id)
    except:
        pass
    try:
        await client(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Okay, ```{to_ban_id}``` is no longer taped!")

unbanned_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@client.on(events("(unban) ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "unban":
        rights = unbanned_rights
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str:
        to_ban_id = input_str
    else:
        await event.edit(NO_USER.format("unban"))
    try:
        to_ban_id = int(to_ban_id)
    except:
        pass
    try:
        await client(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"Well, ```{to_ban_id}``` can join now!")


@client.on(events("(kick) ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    cmd = event.pattern_match.group(0)
    if "me" in cmd:
        user = "me"
    input = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply:
        user = reply.from_id
    elif input:
        user = input
    else:
        await event.edit(NO_USER.format("kick"))
    if user in ENV.SUDO_USERS:
        return await event.edit(SUDO_STR)
    else:
        try:
            user = int(user)
        except:
            pass
        try:
            await client.kick_participant(event.chat_id, user)
            await event.edit(f"`{user}` has been yeeted!")
        except (Exception) as exc:
            await event.edit(str(exc))


ENV.HELPER.update({
    "admin": "\
```.ban <userid>``` (or as a reply to a message of targer user)\
\nUsage: bans target user.\
\n\n```.unban <userid>``` (or as a reply to a message of targer user)\
\nUsage: unbans target user.\
\n\n```.mute <userid>``` (or as a reply to a message of targer user)\
\nUsage: mutes target user.\
\n\n```.unmute <userid>``` (or as a reply to a message of targer user)\
\nUsage: unmutes target user.\
\n\n```.promote <optional_rank>``` (must be a reply to a message of targer user)\
\nUsage: promotes target user.\
\n\n```.demote <userid>``` (or as a reply to a message of targer user)\
\nUsage: demotes target user.\
\n\n```.kick <userid>``` (or as a reply to a message of targer user)\
\nUsage: kicks target user.\
\n\n```.pin``` (as a reply to a message)\
\nUsage: pins target msg.\
"
})
