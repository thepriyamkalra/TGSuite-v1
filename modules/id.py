# For The-TG-Bot v3
# Syntax .id

from telethon.utils import pack_bot_file_id



@client.on(events(pattern="id"))
async def handler(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        chat = await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await event.edit("Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(str(event.chat_id), str(r_msg.from_id), bot_api_file_id))
        else:
            await event.edit("Current Chat ID: `{}`\nFrom User ID: `{}`".format(str(event.chat_id), str(r_msg.from_id)))
    else:
        await event.edit("Current Chat ID: `{}`".format(str(event.chat_id)))


ENV.HELPER.update({
    "id": "\
```.id (as a reply to target user)```\
\nUsage: Prints the current chat id and target user id.\
"
})
