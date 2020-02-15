# For UniBorg
# By authoritydmc
# Based on the insult module made by Hackintosh for friendly telegram bot (https://da.gd/RG2hfe)
# Syntax (.gali <no_of_times_to_insult>)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
import random
from sql_helpers.global_variables_sql import LOGGER, SUDO_USERS, SYNTAX, MODULE_LIST
import sys
import time

MODULE_LIST.append("gali")

@borg.on(admin_cmd(pattern="gali ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1)
    animal = ["मच्छर ","\
हाथी","गिरगिट", "गैंडा","खरगोश","बंदर ","लंगूर","सॉढ","सियार","बतख","गोरिल्ला"," नेवला","खटमल","घोंघा","छछून्‍दर"]
    parts=["लुंड ","झाट","चुत","गांड ","गांड का कीड़ा","औलाद","दामाद","भाई"]
    man_slang=["बहनचोद","मादरचोद","बहिन के लौड़े","बहिन के टक्के","बेटीचोद "]
    starts = ["क्या रे", "तुम", "अबे सुन चूतिये ", "साले ",
              "वो उलटी दिमाग के पैदाइश साले "]
    ends = ["!!!!", "!", ""]
    log_insults = ""
    insults=""
    if args:
        pass
    else:
        args = 1
    try:
        args = int(args)
    except Exception as error:
        await event.edit(error)
    reply_msg = await event.get_reply_message()
    if reply_msg:
        user_id = f"```{reply_msg.from_id}```"
        noformat_userid = reply_msg.from_id
    else:
        user_id = "Unknown user"
        noformat_userid = "Unknown user"
    if noformat_userid in SUDO_USERS:
        await event.edit("**Wait! WHAT?!\nDid you just try to insult my creator?!?!\nBYE!**")
        sys.exit()


    for insulting in range(args):
        start = random.choice(starts)
        parts_ch = random.choice(parts)
        animal_ch=random.choice(animal)
        man_slang_ch = random.choice(man_slang)
        end = random.choice(ends)
        insult = start+","+animal_ch+" के "+parts_ch+"\n"+man_slang_ch+" "+end
        insults+="\n"+insult
        log_insults += f"```{insult}```\n\n"
    #send message now
    await event.edit(insults)
    time.sleep(2)
    await borg.send_message(
            LOGGER,
            f"Insulted [{user_id}] with:\n\n{log_insults}"
       )
       
       
       
SYNTAX.update({
    "gali": "\
**Requested Module --> gali**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.gali <optional_number_of_insults>``` [optionally as a reply to target user][default = 1]\
\nUsage: टारगेट यूजर को गाली दे :>: .\
"
})
