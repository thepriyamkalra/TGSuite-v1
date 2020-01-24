# For UniBorg
# Syntax (.purge as a reply to a msg)

from telethon import events
import asyncio
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST


MODULE_LIST.append("purge")


@borg.on(admin_cmd("purge ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await borg.get_entity(input_str)
            logger.info(from_user)
        async for message in borg.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await borg.delete_messages(event.chat_id, msgs)
                msgs = []
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")


SYNTAX.update({
    "purge": "\
**Requested Module --> purge**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.purge (as a reply to a msg)```\
\nUsage: Purge all msgs until the target message.\
"
})
