# For The-TG-Bot-3.0
# Syntax (.purge as a reply to a msg)

import asyncio
from userbot import syntax


@bot.on(command("wipe ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        count = 0
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await bot.get_entity(input_str)
            logger.info(from_user)
        async for message in bot.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            count = count + 1
            msgs.append(message)
            if len(msgs) == 100:
                await bot.delete_messages(event.chat_id, msgs)
                msgs = []
        if len(msgs) <= 100:
            await bot.delete_messages(event.chat_id, msgs)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")


@bot.on(command("purge ?(.*)"))
async def fastpurger(event):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await event.get_input_chat()
    msgs = []
    count = 0

    async for msg in event.client.iter_messages(chat,
                                               min_id=event.reply_to_msg_id):
        msgs.append(msg)
        count = count + 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await event.client.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await event.client.delete_messages(chat, msgs)


@bot.on(command("edit ?(.*)"))
@errors_handler
async def editer(edit):
    """ For .edit command, edit your last message. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id('me')
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "Edit query was executed successfully")


@bot.on(command("sd ?(.*)"))
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID,
                                         

syntax.update({
    "purge": "\
• ```.purge <as a reply to a msg>```\
\nUsage: Purge all msgs until the target message.\
\n\n• `.sd <time> <message>`\
\nUsage: Creates a message that deletes automatically. <time> must be an integar <100\
\n\n•  `.edit <message>`\
\nUsage: Edits the last message.\
"
})
