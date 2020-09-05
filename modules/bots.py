# For The-TG-Bot v3
# Syntax .bots

from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantsBots



@client.on(events("bots ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    mentions = "**Bots in this Channel**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Bots in {} channel: \n".format(input_str)
        try:
            chat = await client.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in client.iter_participants(chat, filter=ChannelParticipantsBots):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id)
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.edit(mentions)


ENV.HELPER.update({
    "bots": "\
```.bots```\
\nUsage: Returns all the bots in the current chat.\
"
})
