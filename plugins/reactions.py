# For The-TG-Bot-3.0
# By Priyam Kalra & Techy05
# Syntax .oof, .sed, .emo, .wtf, .gei <thing>

import asyncio

emojis = {
    "yee": "ツ",
    "happy": "(ʘ‿ʘ)",
    "veryhappy": "=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾",
    "amazed": "ヾ(o✪‿✪o)ｼ",
    "crying": "༎ຶ︵༎ຶ",
    "dicc": "╰U╯☜(◉ɷ◉ )",
    "fek": "╰U╯\n(‿ˠ‿)",
    "ded": "✖‿✖",
    "sad": "⊙︿⊙",
    "lenny": "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
    "idc": "¯\_(ツ)_/¯",
    "F": "😂😂😂😂😂😂😂😂\n😂😂😂😂😂😂😂😂\n😂😂\n😂😂\n😂😂😂😂😂😂\n😂😂😂😂😂😂\n😂😂\n😂😂\n😂😂\n😂😂\n😂😂",
}


unpacked_emojis = ""
for emoji in emojis:
    unpacked_emojis += f"`{emoji}`\n"

ascii = {
    "mf": "'                            / ¯͡  ) \n                           /...../ \n                         /´¯´/ \n                       /¯..../ \n                    /....  / \n             /´¯/'...' /´¯¯·¸ \n          / '/.../..../..../.. /¨¯\ \n        ('(...´...´.... ¯~'/...')  /\n         \.................'..... /´ \n          \................ _.·´\n            \..............( \n'             \.............\ ",
    "dislike": "███████▄▄███████████▄\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀░░█░░░░██████▀\n░░░░░░░░░█░░░░█\n░░░░░░░░░░█░░░█\n░░░░░░░░░░░█░░█\n░░░░░░░░░░░█░░█\n░░░░░░░░░░░░▀▀ ",
    "music": "╔══╗ \n║██║ \n║(O)║♫ ♪ ♫ ♪\n╚══╝\n▄ █ ▄ █ ▄ ▄ █ ▄ █ ▄ █\n\nVol- --------------------------● Vol+ ",
    "chess": "♜♞♝♚♛♝♞♜\n♟♟♟♟♟♟♟♟\n▓░▓░▓░▓░\n░▓░▓░▓░▓\n▓░▓░▓░▓░\n░▓░▓░▓░▓\n♙♙♙♙♙♙♙♙\n♖♘♗♔♕♗♘♖ ",
    "shitos": "╭━━━┳╮╱╱╭╮╱╭━━━┳━━━╮\n┃╭━╮┃┃╱╭╯╰╮┃╭━╮┃╭━╮┃\n┃╰━━┫╰━╋╮╭╯┃┃╱┃┃╰━━╮\n╰━━╮┃╭╮┣┫┃╱┃┃╱┃┣━━╮┃\n┃╰━╯┃┃┃┃┃╰╮┃╰━╯┃╰━╯┃\n╰━━━┻╯╰┻┻━╯╰━━━┻━━━╯ ",
    "qrcode": "█▀▀▀▀▀█░▀▀░░░█░░░░█▀▀▀▀▀█\n█░███░█░█▄░█▀▀░▄▄░█░███░█\n█░▀▀▀░█░▀█▀▀▄▀█▀▀░█░▀▀▀░█\n▀▀▀▀▀▀▀░▀▄▀▄▀▄█▄▀░▀▀▀▀▀▀▀\n█▀█▀▄▄▀░█▄░░░▀▀░▄█░▄▀█▀░▀\n░█▄▀░▄▀▀░░░▄▄▄█░▀▄▄▄▀▄▄▀▄\n░░▀█░▀▀▀▀▀▄█░▄░████ ██▀█▄\n▄▀█░░▄▀█▀█▀░█▄▀░▀█▄██▀░█▄\n░░▀▀▀░▀░█▄▀▀▄▄░▄█▀▀▀█░█▀▀\n█▀▀▀▀▀█░░██▀█░░▄█░▀░█▄░██\n█░███░█░▄▀█▀██▄▄▀▀█▀█▄░▄▄\n█░▀▀▀░█░█░░▀▀▀░█░▀▀▀▀▄█▀░\n▀▀▀▀▀▀▀░▀▀░░▀░▀░░░▀▀░▀▀▀▀` ",
    "join": "━━━━━┓ \n┓┓┓┓┓┃\n┓┓┓┓┓┃　ヽ○ノ ⇦ Me When \n┓┓┓┓┓┃.      /　        You Joined\n┓┓┓┓┓┃  ノ) \n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃ "
}

unpacked_ascii = ""
for art in ascii:
    unpacked_ascii += f"{art}\n"

from userbot import syntax


@bot.on(command(pattern="oof ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    oof = event.pattern_match.group(1)
    if not oof:
        oof = 10
    try:
        oof = int(oof)
    except:
        return await event.edit("Count must be an integer!")
    oof = int(oof/2)
    output = ""
    for _ in range(oof):
        output += "Oo"
        await event.edit(output)
    output += "f"
    await event.edit(output)


@bot.on(command(pattern="hek ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    for _ in range(5):
        await event.edit(";_;")
        await event.edit("_;;")
        await event.edit(";;_")
    await event.edit(";_;")


@bot.on(command(pattern="sed ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    for _ in range(4):
        await event.edit(":/")
        await event.edit(":|")
        await event.edit(":\\")
        await event.edit(":|")
    await event.edit(":/")


@bot.on(command(pattern="emo ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        req_emoji = emojis[str(input_str)]
        await event.edit(req_emoji)
    except KeyError:
        await event.edit("Emoji not found!")


@bot.on(command(pattern="ascii ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        req_ascii = ascii[str(input_str)]
        await event.edit(req_ascii)
    except KeyError:
        await event.edit("ASCII art not found!")


@bot.on(command("wtf ?(.*)"))
async def func(tf):
    if tf.fwd_from:
        return
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    animation_chars = [
        "**What**",
        "**What The**",
        "**What The F**",
        "**What The F**, __Brah ?__"
    ]

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await tf.edit(animation_chars[i % 4])


@bot.on(command("gei ?(.*)"))
async def func(event):
    if event.fwd_from:
        return
    thing = event.pattern_match.group(1)
    if not thing:
        ton = await event.get_reply_message()
        thing = ton.text
    animation_interval = 0.2
    animation_ttl = range(0, 4)
    animation_chars = [
        f"**“{thing}**",
        f"**“{thing} Is**",
        f"**“{thing} Is Gei”**",
        f"**“{thing} Is Gei”** __- Priyam Kalra__"
    ]

    for i in animation_ttl:
        	
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


syntax.update({
    "reactions": f"\
Just some funny little animations ;)\
\n\n**List of reactions:**\
\n• `.oof <real number>`\
\n• `.sed`\
\n• `.hek`\
\n• `.wtf`\
\n• `.gei <text>`\
\n\n• `.emo <emoji_name>`\
\n__List of included emoji(s):__\
\n{unpacked_emojis}\
\n\n• `.ascii <art_name>`\
\n__List of included ASCII arts:__\
\n{unpacked_ascii}\
"
})
