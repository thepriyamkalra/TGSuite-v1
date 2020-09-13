# For The-TG-Bot v3
# By @Techy05

from datetime import datetime
from modules.sql.filters_sql import get_filter, add_filter, rm_filter, rmrf_filter


client.storage.LastTrigger = {}

@client.on(events(incoming=True))
async def filter(event):
    filters = get_filter(event.chat_id)
    for term in filters:
        if term.trigger in event.raw_text.lower():
            if new_trigger(term.trigger):
                await client.send_message(
                    event.chat_id,
                    term.reply,
                    reply_to=event,
                    silent=True
                )
                client.storage.LastTrigger[term.trigger] = datetime.now()
            

@client.on(events(pattern="addfilter ?(.*)"))
async def addfilter(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if input_str and reply:
        trigger = input_str.lower()
        title = await chat_title(event)
        add_filter(event.chat_id, trigger, reply.text)
        msg = f"**Saved filter** \"`{input_str}`\" **in {title}**"
    else:
        msg = "**Reply to something to add filter**"
    await event.edit(msg)
        
        
@client.on(events(pattern="stopfilter ?(.*)"))
async def stopfilter(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    title = await chat_title(event)
    if input_str:
        if input_str == "--all":
            rmrf_filter(event.chat_id)
            return await event.edit(f"**All filters have been stopped in** `{title}`")
        trigger = input_str.lower()
        filters = get_filter(event.chat_id)
        list = ""
        for term in filters:
            list += term.trigger
        if trigger in list:
            rm_filter(event.chat_id, trigger)
            msg = f"**Stopped filtering** \"`{input_str}`\" **in {title}**"
        else:
            msg = f"**Filter \"`{input_str}`\" **doesn't exist!**"
    else:
        msg = "**Stopped the use of brain!**"
    await event.edit(msg)
    

@client.on(events(pattern="filters"))
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
        
        
def new_trigger(term):
    last = client.storage.LastTrigger.get(term)
    if last:
        now = datetime.now()
        if (now - last).seconds < 10:
            client.storage.LastTrigger[term] = datetime.now()
            return False
        else:
            return True
    else:
        return True

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
\n\n`.addfilter <trigger>`\
\nUsage: Adds a filter in a chat.\
\n\n`.stopfilter <trigger>`\
\nUsage: Stops a filter in a chat.\
\n\n`.stopfilter --all`\
\nUsage: Stops all the filters in a chat.\
"
})