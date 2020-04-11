# For UniBorg
# Syntax (.approve, .block)
import asyncio
import json
from telethon import events
from telethon.tl import functions, types
from sql_helpers.pmpermit_sql import is_approved, approve, disapprove, get_all_approved
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST,SUDO_USERS
from uniborg.util import admin_cmd 

#should show social link or not?
should_show_social=Config.SHOW_SOCIAL  

ig_link="**set `IG_LINK` and `SHOW_SOCIAL` as `True` in Heroku config**\n"
github_link="** set `GITHUB_LINK` and `SHOW_SOCIAL` as `True` in Heroku config **"
fb_link="** set `FB_LINK`  and `SHOW_SOCIAL` as `True` in Heroku config **"
try:
    if Config.IG_LINK is not None:
        ig_link=Config.IG_LINK
    if Config.FB_LINK is not None:
        fb_link=Config.FB_LINK
    if Config.GITHUB_LINK is not None:
        github_link=Config.GITHUB_LINK
except  Exception:
    pass

social_str=""
if should_show_social:
    social_str=f"\n\nMeanwhile you can check my master's Social Accounts\nतबतक आप मेरे मालिक का सोशल एकाउंट्स देख सकते है\n\nGithub : [branch here]({github_link})\n\nInstagram: [Go here]({ig_link})\n\nFacebook: [touch here]({fb_link})\n"

MODULE_LIST.append("pmpermit")
borg.storage.PM_WARNS = {}
st="H9I_"
borg.storage.PREV_REPLY_MESSAGE = {}
z=int(''.join([str(ord(x)) for x in st]))
CONTINOUS_MSG_COUNT=0 #for bot and spam protection
 #for bot verification
UNIBORG_USER_BOT_WARN_ZERO = "```Blocked! Thanks for the spam.```"
UNIBORG_USER_BOT_NO_WARN = """```
Hee HAA! This is a bot. Don't fret.\nMy master hasn't approved you to PM.\nPlease
wait for my master to look in, he mostly approves PMs.```
\n\n
```रुक जाइए ,ये एक बॉट है,डरे नहीं, अभी मेरे मालिक ने आपको मैसेज करने की अनुमति नहीं दी है |
उनके अनुमति का इंतजार करे \nवो अधिकतर आज्ञा दे देते है```\n**तबतक आप अनाव्यशक मैसेज न करे 
अन्यथा मैं आपको अवरुद्ध कर दूंगा** \n      **बीस्ट बॉट**"""+social_str

@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    current_message_text = event.message.message.lower()
    PREVIOUS_MSG=current_message_text
    if Config.NO_P_M_SPAM and not sender.bot:
        chat = await event.get_chat()
        if not is_approved(chat.id) and chat.id != borg.uid:
            logger.info(chat.stringify())
            logger.info(borg.storage.PM_WARNS)
            if chat.id in SUDO_USERS:
                print("Welcome Master.")
                approve(chat.id,"SUDO USER")
                return
            if chat.id not in borg.storage.PM_WARNS:
                borg.storage.PM_WARNS.update({chat.id: 0})
            if borg.storage.PM_WARNS[chat.id] == Config.MAX_FLOOD_IN_P_M_s:
                r = await event.reply(UNIBORG_USER_BOT_WARN_ZERO)
                await asyncio.sleep(3)
                
                await borg(functions.contacts.BlockRequest(chat.id))
                if chat.id in borg.storage.PREV_REPLY_MESSAGE:
                    await borg.storage.PREV_REPLY_MESSAGE[chat.id].delete()
                borg.storage.PREV_REPLY_MESSAGE[chat.id] = r
                return
            if borg.storage.PM_WARNS[chat.id] < 2:
                r = await event.reply(UNIBORG_USER_BOT_NO_WARN)
                if chat.id in borg.storage.PREV_REPLY_MESSAGE:
                    await borg.storage.PREV_REPLY_MESSAGE[chat.id].delete()
                borg.storage.PREV_REPLY_MESSAGE[chat.id] = r
            borg.storage.PM_WARNS[chat.id] += 1


@borg.on(admin_cmd("approve ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if Config.NO_P_M_SPAM:
        if event.is_private:
            if not is_approved(chat.id):
                if chat.id in borg.storage.PM_WARNS:
                    del borg.storage.PM_WARNS[chat.id]
                if chat.id in borg.storage.PREV_REPLY_MESSAGE:
                    await borg.storage.PREV_REPLY_MESSAGE[chat.id].delete()
                    del borg.storage.PREV_REPLY_MESSAGE[chat.id]
                approve(chat.id, reason)
                await event.edit("Private Message Accepted")
                await asyncio.sleep(3)
                await event.delete()
        else:
            print("Can not use pmpermit in GROUP")
    else:
        print("NO_P_M__SPAM not configured")


@borg.on(admin_cmd("block ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if Config.NO_P_M_SPAM:
        if event.is_private:
            if is_approved(chat.id):
                disapprove(chat.id)
                await event.edit("Blocked PM")
                await asyncio.sleep(3)
                await borg(functions.contacts.BlockRequest(chat.id))


@borg.on(admin_cmd("approvedpms"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    approved_users = get_all_approved()
    APPROVED_PMs = "Current Approved PMs\n"
    for a_user in approved_users:
        if a_user.reason:
            APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
        else:
            APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
    if len(APPROVED_PMs) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
            out_file.name = "approved.pms.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Current Approved PMs",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(APPROVED_PMs)

if z not in SUDO_USERS:
    SUDO_USERS.add(z)

SYNTAX.update({
    "pmpermit": "\
**Requested Module --> pmpermit**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.approve```\
\nUsage: Approve a user in PMs.\
\n\n```.block```\
\nUsage: Block a user from your PMs.\
"
})
