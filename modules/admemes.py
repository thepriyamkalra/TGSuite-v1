# For The-TG-Bot v3
# Syntax .admemes

from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator


@client.on(events("admemes ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    mentions = "Look at these admins who havent banned me yet:\n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "loud" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    chat = await event.get_input_chat()
    async for x in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if not x.deleted:
            if isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id)
    mentions += "\n"
    async for x in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if not x.deleted:
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id)
        else:
            mentions += "\n `{}`".format(x.id)
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await event.edit(mentions)


ENV.HELPER.update({
    "admemes": "\
```.admemes [OPTIONAL argument: loud, this will notify the admins.]```\
\nUsage: Mention admins in the current chat.\
"
})
