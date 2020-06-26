# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
#

""" Userbot module for having some fun with people. """

import asyncio
import random
import re
import time

from collections import deque
from cowpy import cow
import requests

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.types import ChannelParticipantsAdmins

from userbot import YOUTUBE_API_KEY
from userbot import syntax

botuser = await bot.get_me()
botuser = f"@{botuser.username}"



# ================= CONSTANT =================
NOOBSTR = [
    "`YOU PRO NIMBA DONT MESS WIDH MEH`",
    "`NOOB NIMBA TRYING TO BE FAMOUS KEK`",
    "`Some Nimbas need to open their small minds instead of their big mouths`",
    "`UH DONT KNOW MEH SO STAY AWAY LAWDE`",
    "`Kysa kysaaaa haaan? Phir MAAR nhi Khayega tu?`",
    "`Zikr Jinka hota hai galiyo meh woh bhosdika ajj paya gya naliyo me`",
]
ZALG_LIST = [["̖",
              " ̗",
              " ̘",
              " ̙",
              " ̜",
              " ̝",
              " ̞",
              " ̟",
              " ̠",
              " ̤",
              " ̥",
              " ̦",
              " ̩",
              " ̪",
              " ̫",
              " ̬",
              " ̭",
              " ̮",
              " ̯",
              " ̰",
              " ̱",
              " ̲",
              " ̳",
              " ̹",
              " ̺",
              " ̻",
              " ̼",
              " ͅ",
              " ͇",
              " ͈",
              " ͉",
              " ͍",
              " ͎",
              " ͓",
              " ͔",
              " ͕",
              " ͖",
              " ͙",
              " ͚",
              " ",
              ],
             [" ̍",
              " ̎",
              " ̄",
              " ̅",
              " ̿",
              " ̑",
              " ̆",
              " ̐",
              " ͒",
              " ͗",
              " ͑",
              " ̇",
              " ̈",
              " ̊",
              " ͂",
              " ̓",
              " ̈́",
              " ͊",
              " ͋",
              " ͌",
              " ̃",
              " ̂",
              " ̌",
              " ͐",
              " ́",
              " ̋",
              " ̏",
              " ̽",
              " ̉",
              " ͣ",
              " ͤ",
              " ͥ",
              " ͦ",
              " ͧ",
              " ͨ",
              " ͩ",
              " ͪ",
              " ͫ",
              " ͬ",
              " ͭ",
              " ͮ",
              " ͯ",
              " ̾",
              " ͛",
              " ͆",
              " ̚",
              ],
             [" ̕",
              " ̛",
              " ̀",
              " ́",
              " ͘",
              " ̡",
              " ̢",
              " ̧",
              " ̨",
              " ̴",
              " ̵",
              " ̶",
              " ͜",
              " ͝",
              " ͞",
              " ͟",
              " ͠",
              " ͢",
              " ̸",
              " ̷",
              " ͡",
              ]]


EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
     "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 420 section 69 prevents me from replying to a stupid like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`I would ask you how old you are but I know you can't count that high.`",
    "`As an outsider, what do you think of the human race?`",
    "`Ordinarily people live and learn. You just live.`",
    "`Keep talking, someday you'll say something intelligent!.......(I doubt it though)`",
    "`Everyone has the right to be stupid but you are abusing the privilege.`",
    "`I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.`",
    "`You should try tasting cyanide.`",
    "`You should try sleeping forever.`",
    "`Pick up a gun and shoot yourself.`",
    "`Try bathing with Hydrochloric Acid instead of water.`",
    "`Go Green! Stop inhaling Oxygen.`",
    "`God was searching for you. You should leave to meet him.`",
    "`You should Volunteer for target in an firing range.`",
    "`Try playing catch and throw with RDX its fun.`",
    "`When your mom dropped you off at the school, she got a ticket for littering.`",
    "`You’re so ugly that when you cry, the tears roll down the back of your head…just to avoid your face.`",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

RUNSREACTS = [
    "`Runs far, far away from earth`",
    "`Running faster than supercomputer, cuzwhynot`",
    "`ZZzzZZzz... Huh? what? oh, just them again, nevermind.`",
    "`Look out for the wall!`",
    "Don't leave me alone with them!!",
    "`You run, you die.`",
    "`Jokes on you, I'm everywhere`",
    "You could also try /kickme, I hear that's fun.",
    "You could also try /banme, I hear that's fun.",
    "`You can run, but you can't hide.`",
    "We can do this the easy way, or the hard way.",
    "You just don't get it, do you?",
    "Yeah, you better run!",
    "I'd run faster if I were you.",
    "May the odds be ever in your favour.",
    "Famous last words.",
    "And they disappeared forever, never to be seen again.",
    "\"Oh, look at me! I'm so cool, I can run from a bot!\" - this person",
    "Yeah yeah, just tap /kickme already.",
    "Here, take this ring and head to Mordor while you're at it.",
    "Legend has it, they're still running...",
    "Unlike Harry Potter, your parents can't protect you from me.",
    "Fear leads to anger. Anger leads to hate. Hate leads to suffering. If you keep running in fear, you might "
    "be the next Vader.",
    "Keep it up, not sure we want you here anyway.",
    "You're a wiza- Oh. Wait. You're not Harry, keep moving.",
    "NO RUNNING IN THE HALLWAYS!",
    "Hasta la vista, baby.",
    "My milkshake brings all the boys to yard... So run faster!",
    "A long time ago, in a galaxy far far away... Someone would've cared about that. Not anymore though.",
    "Hey, look at them! They're running from the inevitable banhammer... Cute.",
    "What are you running after, a white rabbit?",
    "As The Doctor would say... RUN!",
    "`Running a marathon...there's an app for that.`",
]

PRO_STRINGS = [
     "`This gey is pro as phack.`",
     "`Proness Lebel: 6969696969`",
     "`U iz pro but i iz ur DAD, KeK`",
     "`NOOB NIMBA TRYING TO BE FAMOUS KEK`",
     "`Sometimes one middle finger isnâ€™t enough to let someone know how you feel. Thatâ€™s why you have two hands`",
     "`Some Nimbas need to open their small minds instead of their big mouths`",
     "`UH DONT KNOW MEH SO STAY AWAY LAWDE`",
     "`Kysa kysaaaa haaan? Phir MAAR nhi Khayega tu?`",
     "`Zikr Jinka hota hai galiyo meh woh bhosdika ajj paya gya naliyo me`",

]
HELLOSTR = [
    "`Hi !`",
    "`‘Ello, gov'nor!`",
    "`What’s crackin’?`",
    "`‘Sup, homeslice?`",
    "`Howdy, howdy ,howdy!`",
    "`Hello, who's there, I'm talking.`",
    "`You know who this is.`",
    "`Yo!`",
    "`Whaddup.`",
    "`Greetings and salutations!`",
    "`Hello, sunshine!`",
    "`Hey, howdy, hi!`",
    "`What’s kickin’, little chicken?`",
    "`Peek-a-boo!`",
    "`Howdy-doody!`",
    "`Hey there, freshman!`",
    "`I come in peace!`",
    "`Ahoy, matey!`",
    "`Hiya!`",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "ლ(ﾟдﾟლ)",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "ლ｜＾Д＾ლ｜",
    "ლ（╹ε╹ლ）",
    "ლ(ಠ益ಠ)ლ",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "乁༼☯‿☯✿༽ㄏ",
    "ʅ（´◔౪◔）ʃ",
    "ლ(•ω •ლ)",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    "¯\_(ツ)_/¯",
    "¯\_(⊙_ʖ⊙)_/¯",
    "乁ʕ •̀ ۝ •́ ʔㄏ",
    "¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

SLAP_TEMPLATES = [
    "{hits} {victim} with a {item}.",
    "{hits} {victim} in the face with a {item}.",
    "{hits} {victim} around a bit with a {item}.",
    "{throws} a {item} at {victim}.",
    "grabs a {item} and {throws} it at {victim}'s face.",
    "launches a {item} in {victim}'s general direction.",
    "starts slapping {victim} silly with a {item}.",
    "pins {victim} down and repeatedly {hits} them with a {item}.",
    "grabs up a {item} and {hits} {victim} with it.",
    "ties {victim} to a chair and {throws} a {item} at them.",
    "gave a friendly push to help {victim} learn to swim in lava."
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    "baseball bat",
    "cricket bat",
    "wooden cane",
    "printer",
    "shovel",
    "CRT monitor",
    "physics textbook",
    "toaster",
    "portrait of Richard Stallman",
    "television",
    "five ton truck",
    "roll of duct tape",
    "book",
    "laptop",
    "old television",
    "sack of rocks",
    "rainbow trout",
    "spiked bat",
    "fire extinguisher",
    "heavy rock",
    "chunk of dirt",
    "beehive",
    "piece of rotten meat",
    "bear",
    "ton of bricks",
]

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "fek ke maari",
    "slaps",
    "smacks",
    "bashes",
]

# ===========================================

@bot.on(command("slap ?(.*)"))
async def who(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        """ slaps a user, or get slapped if not a reply. """
        if event.fwd_from:
            return

        replied_user = await get_user(event)
        caption = await slap(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id

        if not message_id_to_reply:
            message_id_to_reply = None

        try:
            await event.edit(caption)

        except:
            await event.edit("`Can't slap this person, need to fetch some sticks and stones !!`")

async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None

    return replied_user

async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    caption = "..." + temp.format(victim=slapped, item=item, hits=hit, throws=throw)

    return caption

@bot.on(command("-_- ?(.*)"))
async def lol(lel):
    if not lel.text[0].isalpha() and lel.text[0] not in ("/", "#", "@", "!"):
        """ Ok... """
        okay = "-_-"
        for _ in range(10):
            okay = okay[:-1] + "_-"
            await lel.edit(okay)

@bot.on(command("decide ?(.*)"))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        r = requests.get("https://yesno.wtf/api").json()
        await event.client.send_message(
            event.chat_id,
            str(r["answer"]).upper(),
            reply_to=message_id,
            file=r["image"]
        )
        await event.delete()

@bot.on(command("insult ?(.*)"))
async def insult(e):
    """ I make you cry !! """
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(random.choice(INSULT_STRINGS))

@bot.on(command("vapor ?(.*)"))
async def vapor(vpr):
    """ Vaporize everything! """
    if not vpr.text[0].isalpha() and vpr.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await vpr.get_reply_message()
        message = vpr.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
            return

        for charac in message:
            if 0x21 <= ord(charac) <= 0x7F:
                reply_text.append(chr(ord(charac) + 0xFEE0))
            elif ord(charac) == 0x20:
                reply_text.append(chr(0x3000))
            else:
                reply_text.append(charac)

        await vpr.edit("".join(reply_text))

			  
@bot.on(command("repo ?(.*)"))
async def source(rep):
        await rep.edit("Click [here](https://github.com/Techy05/The-TG-Bot-3.0) to open this lit af repo.")
			  
			  
@bot.on(command("stretch ?(.*)"))
async def stretch(stret):
    """ Stretch it."""
    if not stret.text[0].isalpha() and stret.text[0] not in ("/", "#", "@", "!"):
        textx = await stret.get_reply_message()
        message = stret.text
        message = stret.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await stret.edit("`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")
            return

        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
            (r"\1"*count),
            message
        )
        await stret.edit(reply_text)


@bot.on(command("zalgofy ?(.*)"))
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    if not zgfy.text[0].isalpha() and zgfy.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await zgfy.get_reply_message()
        message = zgfy.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await zgfy.edit(
                "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
            )
            return

        for charac in message:
            if not charac.isalpha():
                reply_text.append(charac)
                continue

            for _ in range(0, 3):
                randint = random.randint(0, 2)

                if randint == 0:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[0]).strip()
                elif randint == 1:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[1]).strip()
                else:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[2]).strip()

            reply_text.append(charac)

        await zgfy.edit("".join(reply_text))


@bot.on(command("hi ?(.*)"))
async def hoi(hello):
    """ Greet everyone! """
    if not hello.text[0].isalpha() and hello.text[0] not in ("/", "#", "@", "!"):
        await hello.edit(random.choice(HELLOSTR))
			  
@bot.on(command("kill ?(.*)"))
async def killing (killed):
    if not killed.text[0].isalpha() and killed.text[0] not in ("/", "#", "@", "!"):
        if await killed.get_reply_message():
            await killed.edit(
                "`Targeted user killed by Headshot 😈......`\n"
		f"Respect +69 for {botuser}\n"
            )
			  			  
@bot.on(command("pro ?(.*)"))
async def proo (pros):
    """ String for Pros only -_-"""
    if not pros.text[0].isalpha() and pros.text[0] not in ("/", "#", "@", "!"):
        index = random.randint(0, len(PRO_STRINGS) - 1)
        reply_text = PRO_STRINGS[index]
        await pros.edit(reply_text)


@bot.on(command("owo ?(.*)"))
async def faces(owo):
    """ UwU """
    if not owo.text[0].isalpha() and owo.text[0] not in ("/", "#", "@", "!"):
        textx = await owo.get_reply_message()
        message = owo.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await owo.edit("` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await owo.edit(reply_text)


@bot.on(command("shruggie ?(.*)"))
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    if not shg.text[0].isalpha() and shg.text[0] not in ("/", "#", "@", "!"):
        await shg.edit(random.choice(SHGS))


@bot.on(command("runs ?(.*)"))
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if not run.text[0].isalpha() and run.text[0] not in ("/", "#", "@", "!"):
        await run.edit(random.choice(RUNSREACTS))

@bot.on(command("noob ?(.*)"))
async def metoo(hahayes):
    """ Haha yes """
    if not hahayes.text[0].isalpha() and hahayes.text[0] not in ("/", "#", "@", "!"):
        await hahayes.edit(random.choice(NOOBSTR))
			  
@bot.on(command("moon ?(.*)"))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
	    if event.fwd_from:
		    return
	    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
	    for _ in range(32):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)

@bot.on(command("earth ?(.*)"))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
	for _ in range(48):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(1)
    
@bot.on(command("clock ?(.*)"))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
	    if event.fwd_from:
		    return
	    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
	    for _ in range(32):
		    await asyncio.sleep(0.1)
		    await event.edit("".join(deq))
		    deq.rotate(1)

@bot.on(command("mock ?(.*)"))
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    if not mock.text[0].isalpha() and mock.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await mock.get_reply_message()
        message = mock.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await mock.edit("".join(reply_text))


@bot.on(command("clap ?(.*)"))
async def claptext(memereview):
    if not memereview.text[0].isalpha() and memereview.text[0] not in ("/", "#", "@", "!"):
        textx = await memereview.get_reply_message()
        message = memereview.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await memereview.edit("`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await memereview.edit(reply_text)


@bot.on(command("f ?(.*)"))
async def payf(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        paytext = e.pattern_match.group(1)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*5, paytext*1,paytext*1, paytext*4, paytext*1, paytext*1, paytext*1)
        await e.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)",)
async def let_me_google_that_for_you(lmgtfy_q):
    if not lmgtfy_q.text[0].isalpha() and lmgtfy_q.text[0] not in ("/", "#", "@", "!"):
        textx = await lmgtfy_q.get_reply_message()
        query = lmgtfy_q.text
        if query[5:]:
            query = str(query[5:])
        elif textx:
            query = textx
            query = query.message
        query_encoded = query.replace(" ", "+")
        lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
        payload = {'format': 'json', 'url': lfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        await lmgtfy_q.edit(f"[{query}]({r.json()['shorturl']})")
        if BOTLOG:
            await bot.send_message(
                BOTLOG_CHATID,
                "LMGTFY query `" + query + "` was executed successfully",
            )


@bot.on(command("yt_dl ?(.*)"))
async def download_video(v_url):
    """ For .yt_dl command, download videos from YouTube. """
    if not v_url.text[0].isalpha() and v_url.text[0] not in ("/", "#", "@", "!"):
        url = v_url.pattern_match.group(1)
        quality = v_url.pattern_match.group(2)

        await v_url.edit("**Fetching...**")

        video = YouTube(url)

        if quality:
            video_stream = video.streams.filter(
                progressive=True,
                subtype="mp4",
                res=quality
            ).first()
        else:
            video_stream = video.streams.filter(
                progressive=True,
                subtype="mp4"
            ).first()

        if video_stream is None:
            all_streams = video.streams.filter(
                progressive=True,
                subtype="mp4"
            ).all()
            available_qualities = ""

            for item in all_streams[:-1]:
                available_qualities += f"{item.resolution}, "
            available_qualities += all_streams[-1].resolution

            await v_url.edit(
                "**A stream matching your query wasn't found. Try again with different options.\n**"
                "**Available Qualities:**\n"
                f"{available_qualities}"
            )
            return

        video_size = video_stream.filesize / 1000000

        if video_size >= 50:
            await v_url.edit(
                ("**File larger than 50MB. Sending the link instead.\n**"
                 f"Get the video [here]({video_stream.url})\n\n"
                 "**If the video plays instead of downloading, right click(or long press on touchscreen) and "
                 "press 'Save Video As...'(may depend on the browser) to download the video.**")
            )
            return

        await v_url.edit("**Downloading...**")

        video_stream.download(filename=video.title)

        url = f"https://img.youtube.com/vi/{video.video_id}/maxresdefault.jpg"
        resp = get(url)
        with open('thumbnail.jpg', 'wb') as file:
            file.write(resp.content)

        await v_url.edit("**Uploading...**")
        await v_url.client.send_file(
            v_url.chat_id,
            f'{safe_filename(video.title)}.mp4',
            caption=f"{video.title}",
            thumb="thumbnail.jpg"
        )

        os.remove(f"{safe_filename(video.title)}.mp4")
        os.remove('thumbnail.jpg')
        await v_url.delete()
			  
@bot.on(command("type ?(.*)"))
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    if not typew.text[0].isalpha() and typew.text[0] not in ("/", "#", "@", "!"):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.005
        typing_symbol = " ❘"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)
            
@bot.on(command("cmd ?(.*)"))
async def typewriter(typew):
    """ Just a small command to make your keyboard become a terminal!"""
    if not typew.text[0].isalpha() and typew.text[0] not in ("/", "#", "@", "!"):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a command to execute!`")
            return
        sleep_time = 0.008
        typing_symbol = "_"
        old_text = ''
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)            


syntax.update({
    "memes": "\
**A page of Dictionary for memes module**\
\n\n• ```.-_-```\
\nUsage: Ok...\
\n\n• ```.vapor```\
\nUsage: Vaporize everything!\
\n\n• ```.stretch```\
\nUsage: Stretch it.\
\n\n• ```.zalgofy```\
\nUsage: Invoke the feeling of chaos.\
\n\n• ```.moon```\
\nUsage: kensar moon animation.\
\n\n• ```.clock```\
\nUsage: kensar clock animation.\
\n\n• ```.solarsystem```\
\nUsage: kensar solar system animation.\
\n\n• ```.earth```\
\nUsage: kensar earth animation.\
\n\n• ```.hi```\
\nUsage: Greet everyone!\
\n\n• ```.owo```\
\nUsage: UwU\
\n\n• ```.slap```\
\nUsage: reply to slap them with random objects !!\
\n\n• ```.cry```\
\nUsage: y u du dis, i cri evrytiem\
\n\n• ```.shruggie```\
\nUsage: Shrug at it !!\
\n\n• ```.runs```\
\nUsage: Run, run, RUNNN! [`.disable runs`: disable | `.enable runs`: enable]\
\n\n• ```.metoo```\
\nUsage: Haha yes\
\n\n• ```.mock```\
\nUsage: Do it and find the real fun.\
\n\n• ```.clap```\
\nUsage: Praise people!\
\n\n• ```.f <emoji/character>```\
\nUsage: Pay Respects.\
\n\n• ```.type <text>```\
\nUsage: Just a small command to make your keyboard become a typewriter!\
\n\n• ```.cmd <text>```\
\nUsage: Just a small command to make your keyboard become a terminal!\
\n\n• ```.decide```\
\nUsage: Make a quick decision.\
\n\n• ```.noob```\
\nUsage: Whadya want to know? Are you a NOOB?\
\n\n• ```.pro```\
\nUsage: If you think you're pro, try this.\
\n\n• ```.repo```\
\nUsage: A link to this Powerful Bot's Repo.\
"
})
