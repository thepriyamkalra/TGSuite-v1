
import asyncio
from datetime import datetime
from telethon.tl.types import User, Chat, Channel



@client.on(events(pattern="stat", outgoing=True))
async def handler(event):
    if event.fwd_from:
        return
    start = datetime.now()
    pm = 0
    grps = 0
    supergrps = 0
    chnls = 0
    bots = 0
    dialogs = await client.get_dialogs(
        limit=None,
        ignore_migrated=True
    )
    for d in dialogs:
        currrent_entity = d.entity
        if type(currrent_entity) is User:
            if currrent_entity.bot:
                bots += 1
            else:
                pm += 1
        elif type(currrent_entity) is Chat:
            grps += 1
        elif type(currrent_entity) is Channel:
            if currrent_entity.broadcast:
                chnls += 1
            else:
                supergrps += 1
        else:
            print(d)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(f"**Your stats obtained in {ms} second(s).\nYou have {pm} private messages.\nYou are in {grps} groups.\nYou are in {supergrps} super groups.\nYou are in {chnls} channels.\nYou have chats with {bots} bots.**")


ENV.HELPER.update({
    "stat": "\
```.stat```\
\nUsage: Print your own use statistics.\
"
})
