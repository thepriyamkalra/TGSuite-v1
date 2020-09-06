# For The-TG-Bot v3
# By Priyam Kalra
# Based on the insult module made by Hackintosh for friendly telegram bot (https://da.gd/RG2hfe)
# Syntax (.insult <no_of_times_to_insult>)

import asyncio
import random
import sys
import time

insult_strings = ("Owww ... Such a stupid idiot.",
    "Don't drink and type.",
    "I think you should go home or better a mental asylum.",
    "Command not found. Just like your brain.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "You can type better than that.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Sorry, we do not sell brains.",
    "Believe me you are not normal.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "Zombies eat brains... you're safe.",
    "You didn't evolve from apes, they evolved from you.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "Stupidity is not a crime so you are free to go.",
    "You are proof that evolution CAN go in reverse.",
    "I would ask you how old you are but I know you can't count that high.",
    "As an outsider, what do you think of the human race?",
    "Brains aren't everything. In your case they're nothing.",
    "Ordinarily people live and learn. You just live.",
    "I don't know what makes you so stupid, but it really works.",
    "Keep talking, someday you'll say something intelligent! (I doubt it though)",
    "Shock me, say something intelligent.",
    "Your IQ's lower than your shoe size.",
    "Alas! Your neurotransmitters are no more working.",
    "Are you crazy you fool.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
    "You should try tasting cyanide.",
    "Your enzymes are meant to digest rat poison.",
    "You should try sleeping forever.",
    "Pick up a gun and shoot yourself.",
    "You could make a world record by jumping from a plane without parachute.",
    "Stop talking BS and jump in front of a running bullet train.",
    "Try bathing with Hydrochloric Acid instead of water.",
    "Try this: if you hold your breath underwater for an hour, you can then hold it forever.",
    "Go Green! Stop inhaling Oxygen.",
    "God was searching for you. You should leave to meet him.",
    "give your 100%. Now, go donate blood.",
    "Try jumping from a hundred story building but you can do it only once.",
    "You should donate your brain seeing that you never used it.",
    "Volunteer for target in an firing range.",
    "Head shots are fun. Get yourself one.",
    "You should try swimming with great white sharks.",
    "You should paint yourself red and run in a bull marathon.",
    "You can stay underwater for the rest of your life without coming back up.",
    "How about you stop breathing for like 1 day? That'll be great.",
    "Try provoking a tiger while you both are in a cage.",
    "Have you tried shooting yourself as high as 100m using a canon.",
    "You should try holding TNT in your mouth and igniting it.",
    "Try playing catch and throw with RDX its fun.",
    "I heard phogine is poisonous but i guess you wont mind inhaling it for fun.",
    "Launch yourself into outer space while forgetting oxygen on Earth.",
    "You should try playing snake and ladders, with real snakes and no ladders.",
    "Dance naked on a couple of HT wires.",
    "Active Volcano is the best swimming pool for you.",
    "You should try hot bath in a volcano.",
    "Try to spend one day in a coffin and it will be yours forever.",
    "Hit Uranium with a slow moving neutron in your presence. It will be a worthwhile experience.",
    "You can be the first person to step on sun. Have a try."
)

adjectives_start = ["salty", "fat", "fucking", "shitty",
                        "stupid", "retarded", "self conscious", "tiny"]
adjectives_mid = ["little", "vitamin D deficient",
                    "idiotic", "incredibly stupid"]
nouns = ["cunt", "pig", "pedophile", "beta male", "bottom", "retard", "ass licker", "cunt nugget",
            "PENIS", "dickhead", "flute", "idiot", "motherfucker", "loner", "creep"]
starts = ["You're a", "You", "Fuck off you", "Actually die you", "Listen up you",
            "What the fuck is wrong with you, you"]
ends = ["!!!!", "!", ""]

def get_strong_insult():
    start = random.choice(starts)
    adjective_start = random.choice(adjectives_start)
    adjective_mid = random.choice(adjectives_mid)
    noun = random.choice(nouns)
    end = random.choice(ends)
    insult = start + " " + adjective_start + " " + \
        adjective_mid + (" " if adjective_mid else "") + noun + end
    return insult

@client.on(events(pattern="insult ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return

    args = str(event.pattern_match.group(1)).split()
    insType, n = (0, 0)
    if not args:
        insType, n = (1, 1)
    else:
        try: 
            args = list(map(int, args))
        except Exception as error:
            await event.edit(error)
        insType, n = args if len(args) == 2 else (1, args[0])
    log_insults = ""

    for _ in range(n):
        insult = random.choice(insult_strings) if insType == 1 else get_strong_insult()
        log_insults += f"```{insult}```\n\n"
        reply_msg = await event.get_reply_message()
        if reply_msg:
            user_id = f"```{reply_msg.from_id}```"
            noformat_userid = reply_msg.from_id
        else:
            user_id = "Unknown user"
            noformat_userid = "Unknown user"
        if noformat_userid in ENV.SUDO_USERS:
            await event.edit("**Wait! WHAT?!\nDid you just try to insult my creator?!?!\nBYE!**")
            sys.exit()
            # probably not needed but meh
            break
        else:
            await event.edit(insult)
            time.sleep(2)
            status = f"Insulted [{user_id}] with:\n\n{log_insults}"
            await log(status)


async def log(text):
    LOGGER = ENV.LOGGER_GROUP
    await client.send_message(LOGGER, text)

ENV.HELPER.update({
    "insult": "\
    ```.insult <type(optional), no. of insults(optional)>```[as a reply to target user]\n[types-> 1. soft insults\t 2. hard insults]\n[default (type, no. of insults) = (1,1)]\
\nUsage: Insults target user.\
"
})
