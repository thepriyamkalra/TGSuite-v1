# For UniBorg
# By Priyam Kalra
# Based on the insult module made by Hackintosh for friendly telegram bot (https://da.gd/RG2hfe)
# Syntax (.insult <no_of_times_to_insult>)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types
import random
from sql_helpers.global_variables_sql import LOGGER
import time


@borg.on(admin_cmd(pattern="insult ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1)
    adjectives_start = ["salty", "fat", "fucking", "shitty",
                        "stupid", "retarded", "self conscious", "tiny"]
    adjectives_mid = ["little", "vitamin D deficient",
                      "idiotic", "incredibly stupid"]
    nouns = ["cunt", "pig", "pedophile", "beta male", "bottom", "retard", "ass licker", "cunt nugget",
             "PENIS", "dickhead", "flute", "idiot", "motherfucker", "loner", "creep"]
    starts = ["You're a", "You", "Fuck off you", "Actually die you", "Listen up you",
              "What the fuck is wrong with you, you"]
    ends = ["!!!!", "!", ""]
    log_insults = ""
    if args:
        pass
    else:
        args = 5
    try:
        args = int(args)
    except Exception as error:
        await event.edit(error)
    for insulting in range(args):
        start = random.choice(starts)
        adjective_start = random.choice(adjectives_start)
        adjective_mid = random.choice(adjectives_mid)
        noun = random.choice(nouns)
        end = random.choice(ends)
        insult = start + " " + adjective_start + " " + \
            adjective_mid + (" " if adjective_mid else "") + noun + end
        log_insults += f"```{insult}```\n\n"
        reply_msg = await event.get_reply_message()
        if reply_msg:
            user_id = f"```{reply_msg.from_id}```"
        else:
            user_id = "Unknown user"
        await event.edit(insult)
        time.sleep(2)
    await borg.send_message(
        LOGGER,
        f"Insulted [{user_id}] with:\n\n{log_insults}"
    )
