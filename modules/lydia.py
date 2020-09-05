# For The-TG-Bot v3
# Syntax
# .enableai [as a reply to user's message] // Turns AI on For that user.
# .disableai [as a reply to user's message] // Turns AI off For that user.
# .listai // Outputs List Of Currently added Users in AI Auto-Chat.
# Credits:
# @Hackintosh5 (for inspiring me to write this module)
# @Zero_cool7870 (For Writing The Original Module)
# Zi Xing (For CoffeeHouse API)
# Modified by @authoritydmc for v2.2.2 compatibility
# Modified by Priyam Kalra 6/19/2020

from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
import asyncio
import io
from modules.sql.lydia_ai_sql import get_s, get_all_s, add_s, remove_s
from time import time

# Global Variables
api_key = ""
api_client = ""
lydia = None
session = None
if ENV.LYDIA_API is not None:
    api_key = ENV.LYDIA_API
    api_client = API(api_key)
    lydia = LydiaAI(api_client)



@client.on(events(pattern="(enable|disable|list)ai"))
async def lydia_disable_enable(event):
    if event.fwd_from:
        return
    if ENV.LYDIA_API is None:
        await event.edit("Please add required `LYDIA_API` enviroment variable.")
        return
    else:
        api_key = ENV.LYDIA_API
        api_client = API(api_key)
        lydia = LydiaAI(api_client)

    input_str = event.pattern_match.group(1)

    if event.reply_to_msg_id is not None or input_str == "list" or event.is_private:
        reply_msg = None
        user_id = None
        chat_id = event.chat_id
        if event.is_private:
            user_id = event.chat_id
        if event.reply_to_msg_id is not None:
            reply_msg = await event.get_reply_message()
            user_id = reply_msg.from_id
        # await event.edit("Processing...")
        if input_str == "enable":
            session = lydia.create_session()
            logger.info(session)
            logger.info(add_s(user_id, chat_id, session.id, session.expires))
            await event.edit(f"Hello there!")
        elif input_str == "disable":
            logger.info(remove_s(user_id, chat_id))
            await event.edit(f"No, no, no, i am out.")
        elif input_str == "list":
            lsts = get_all_s()
            if len(lsts) > 0:
                output_str = "AI enabled users:\n\n"
                for lydia_ai in lsts:
                    output_str += f"[user](tg://user?id={lydia_ai.user_id}) in chat `{lydia_ai.chat_id}`\n"
            else:
                output_str = "No Lydia AI enabled users / chats. Start by replying `.enableai` to any user in any chat!"
            if len(output_str) > ENV.MAX_MESSAGE_SIZE_LIMIT:
                with io.BytesIO(str.encode(output_str)) as out_file:
                    out_file.name = "lydia_ai.text"
                    await borg.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="Lydia AI enabled users",
                        reply_to=event
                    )
            else:
                await event.edit(output_str)
        else:
            await event.edit("Reply to a user's message to add / delete them from lydia ai-chat.")
    else:
        await event.edit("Reply to a user's message to add / delete them from Lydia ai-chat.")


@client.on(events(incoming=True))
async def on_new_message(event):
    if event.chat_id in ENV.BLACK_LIST:
        return
    if ENV.LYDIA_API is None:
        return
    if not event.media:
        user_id = event.from_id
        chat_id = event.chat_id
        s = get_s(user_id, chat_id)
        if s is not None:
            session_id = s.session_id
            session_expires = s.session_expires
            query = event.text
            # session=None # Making a global session id.
            # Check if the session is expired
            # If this method throws an exception at this point,
            # then there's an issue with the API, Auth or Server.
            if session_expires < time():
                # re-generate session
                session = lydia.create_session()
                logger.info(session)
                session_id = session.id
                session_expires = session.expires
                logger.info(
                    add_s(user_id, chat_id, session_id, session_expires))
            # Try to think a thought.
            try:
                async with event.client.action(event.chat_id, "typing"):
                    await asyncio.sleep(1)
                    output = lydia.think_thought(session_id, query)
                    await event.reply(output)
            except Exception as e:
                logger.info(str(e))

ENV.HELPER.update({
    "lydia": "\
```.enableai (as a reply to target user)```\
\nUsage: Enables LydiaAI for the target user in the current chat.\
\n\n```.disableai (as a reply to target user)```\
\nUsage: Disables LydiaAI for the target user in the current chat.\
\n\n```.listai```\
\nUsage: Lists all users on which LydiaAI is enabled.\
"
})
