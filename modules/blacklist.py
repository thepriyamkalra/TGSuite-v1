# For The-TG-Bot v3
# By @Techy05

from modules.sql.blacklist_sql import get_bl, add_bl, rm_bl, rmrf_bl
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator


@client.on(events(incoming=True))
async def blacklist(event):
    if await admin(event):
        return
    blacklist = get_bl(event.chat_id)
    for term in blacklist:
        if term.trigger in event.raw_text.lower():
            await event.delete()
            

@client.on(events(pattern="addblacklist ?(.*)"))
async def addblacklist(event):
    if event.fwd_from:
        return
    if not event.is_private and not await admin(event):
        return await event.edit("`Earn admin rights! Nub`")
    input_str = event.pattern_match.group(1)
    if input_str:
        trigger = input_str.lower()
        title = await chat_title(event)
        blocked = get_bl(event.chat_id)
        blacklist = ""
        for term in blocked:
            blacklist += term.trigger
        if trigger not in blacklist:
            add_bl(event.chat_id, trigger)
            msg = f"`Blacklisted \"{input_str}\" in {title}`"
        else: 
            msg = f"`Trigger \"{input_str}\" is already blacklisted in {title}`"
    else:
        msg = "`What am I supposed to blacklist!?`"
    await event.edit(msg)
        
        
@client.on(events(pattern="rmblacklist ?(.*)"))
async def unblacklist(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    title = await chat_title(event)
    if input_str:
        if input_str == "--all":
            rmrf_bl(event.chat_id)
            return await event.edit(f"`All triggers have been removed from {title}`")
        trigger = input_str.lower()
        chat = event.chat_id
        blocked = get_bl(chat)
        blacklist = ""
        for term in blocked:
            blacklist += term.trigger
        if trigger in blacklist:
            rm_bl(chat, trigger)
            msg = f"`Unblacklisted \"{input_str}\" in {title}`"
        else:
            msg = f"`Trigger \"{input_str}\" doesn't exist!`"
    else:
        msg = "`What do you want to remove from blacklist!?`"
    await event.edit(msg)
    

@client.on(events(pattern="blacklist"))
async def get_blacklist(event):
    if event.fwd_from:
        return
    title = await chat_title(event)
    blacklist = f"`No blacklist triggers in {title}`"
    blocked = get_bl(event.chat_id)
    if blocked:
        blacklist = f"**Blacklist triggers in {title}**\n\n"
        for term in blocked:
            blacklist += "• `" + term.trigger + "`\n"
    await event.edit(blacklist)
        

async def admin(event):
    try:
        if str(event.chat_id).startswith("-100"):
            sender = await event.get_sender()
            member = await client(GetParticipantRequest(
                channel=event.chat_id, 
                user_id=event.from_id
            ))
            if isinstance(member.participant, (ChannelParticipantAdmin,
                    ChannelParticipantCreator)) and not sender.bot:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

async def chat_title(event):
    chat = await event.get_chat()
    if event.is_private:
        firstname = chat.first_name
        lastname = f" {chat.last_name}" if chat.last_name else ""
        title = firstname + lastname
    else:
        title = chat.title
    return title
        
        
ENV.HELPER.update({
    "blacklist": "\
`.blacklist`\
\nUsage: Lists active blacklist triggers in a chat.\
\n\n`.addblacklist <trigger>`\
\nUsage: Adds a trigger in a chat.\
\n\n`.rmblacklist <trigger>`\
\nUsage: Removes a trigger from a chat.\
\n\n`.rmblacklist --all`\
\nUsage: Removes all triggers from a chat.\
"
})