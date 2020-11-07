# For The-TG-Bot v3
# By @Techy05

from datetime import datetime
from modules.sql.filters_sql import get_filter, add_filter, rm_filter, rmrf_filter


client.storage.LastTrigger = {}  # spam protection

@client.on(events(incoming=True))
async def filter(event):
    filters = get_filter(event.chat_id)
    for term in filters:
        if term.trigger in event.raw_text.lower() and not last_used(term.trigger):
            text = term.content
            if "{mention}" in text:
                sender = await event.get_sender()
                text = text.format(mention = f"[{sender.first_name}](tg://user?id={sender.id})")
            media = (await client.get_messages(ENV.LOGGER_GROUP, ids=int(term.file))).media if term.file else None
            await event.reply(
                text, 
                file=media, 
                silent=True
            )
            break
            client.storage.LastTrigger[term.trigger] = datetime.now()
            

@client.on(events("filters"))
async def get_filters(event):
    if event.fwd_from:
        return
    title = await chat_title(event)
    list = f"**No filters in** `{title}`!"
    filters = get_filter(event.chat_id)
    if filters:
        list = f"**Filters in {title}**:\n\n"
        for term in filters:
            list += "• `" + term.trigger + "`\n"
    await event.edit(list)
        

@client.on(events("filter ?((.|\n)*)"))
async def addfilter(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    file = None
    if input_str and not reply:
        if "\"" in input_str:
            split = input_str.lstrip("\"").split("\"", maxsplit=1)
        else:
            split = input_str.split(maxsplit=1)
        trigger = split[0].strip()
        content = split[1].strip()
    elif input_str and reply:
        trigger = input_str
        content = reply.text
        if reply.media:
            file = await log(reply.media, trigger)
    else:
        return await event.edit("**I need some content to add a filter!**")
    add_filter(event.chat_id, trigger.lower(), content, file)
    await event.edit(f"**Saved filter '`{trigger}`' in {await chat_title(event)}.**")
        
        
@client.on(events("rmfilter ?(.*)"))
async def rmfilter(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    title = await chat_title(event)
    if input_str == "-a" or input_str == "-all":
        for term in get_filter(event.chat_id):
            if term.file:
                file = await client.get_messages(ENV.LOGGER_GROUP, ids=int(term.file))
                await file.delete()
        rmrf_filter(event.chat_id)
        msg = f"**All filters have been stopped in** `{title}`"
    elif input_str:
        trigger = input_str.lower()
        msg = f"**Filter '`{input_str}`' doesn't exist!**"
        for term in get_filter(event.chat_id):
            if term.trigger == trigger:
                if term.file:
                    file = await client.get_messages(ENV.LOGGER_GROUP, ids=int(term.file))
                    await file.delete()
                rm_filter(event.chat_id, trigger)
                msg = f"**Stopped filtering '`{trigger}`' in {title}**"
    else:
        msg = "**Stopped the use of brain!**"
    await event.edit(msg)
    

async def log(media, trigger):
    file = await client.send_file(ENV.LOGGER_GROUP, media, caption=f"Filter: {trigger.lower()}")
    msg_id = file.id
    return str(msg_id)

def last_used(term):
    last = client.storage.LastTrigger.get(term)
    if last:
        now = datetime.now()
        if (now - last).seconds < 10:
            client.storage.LastTrigger[term] = datetime.now()
            return True
        else:
            return False
    else:
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
    "filters": "\
`.filters`\
\nUsage: Lists all active filters in a chat.\
\n\n`.filter [trigger] [content/reply]`\
\nUsage: Adds a filter in a chat.\
\n\n`.rmfilter [trigger]`\
\nUsage: Stops a filter in a chat.\
\n\n`.rmfilter [-a / -all]`\
\nUsage: Stops all the filters in a chat.\
\n\n\n**EXAMPLES:**\
\n•  To set a one-word filter:\
\n__.filter hello Hey there, {mention}!__\
\n\n•  To set a multi-word filter:\
\n__.filter \"where are you\" I'm on my journey to Neptune!.__\
\n\n•  To set a filter while replying: (quotes are not required)\
\n__.filter how to deploy The-TG-Bot (as a reply to the readme)__\
"
})
