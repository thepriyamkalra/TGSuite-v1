# For The-TG-Bot v3
# Syntax (.purge as a reply to a msg)

import asyncio



@client.on(events("purge ?(.*)"))
async def purge(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await client.get_entity(input_str)
            logger.info(from_user)
        async for message in client.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await client.delete_messages(event.chat_id, msgs)
                msgs = []
        msgs.append(reply)        
        if len(msgs) <= 100:
            await client.delete_messages(event.chat_id, msgs)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")


ENV.HELPER.update({
    "purge": "\
```.purge (as a reply to a msg)```\
\nUsage: Purge all msgs until the target message.\
"
})
