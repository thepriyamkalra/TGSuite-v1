# For The-TG-Bot-3.0
# By Priyam Kalra
# Syntax .oof, .sed, .emoji

import asyncio

emojis = {
    "yee": "ツ",
    "happy": "(ʘ‿ʘ)",
    "veryhappy": "=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾",
    "amazed": "ヾ(o✪‿✪o)ｼ",
    "crying": "༎ຶ‿༎ຶ",
    "dicc": "╰U╯☜(◉ɷ◉ )",
    "fek": "╰U╯\n(‿ˠ‿)",
    "ded": "✖‿✖",
    "sad": "⊙︿⊙",
    "lenny": "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
    "idc": "¯\_(ツ)_/¯"
}

unpacked_emojis = ""
for emoji in emojis:
    unpacked_emojis += f"`{emoji}`\n"

ascii = {
    "mf": "......................................../´¯/) \n......................................,/¯../ \n...................................../..../ \n..................................../´.¯/ \n..................................../´¯/ \n..................................,/¯../ \n................................../..../ \n................................./´¯./ \n................................/´¯./ \n..............................,/¯../ \n............................./..../ \n............................/´¯/ \n........................../´¯./ \n........................, /¯.. / \n......................./.... / \n...................... /´¯/ \n...................., /¯.. / \n.................../.... / \n............. /´¯/\'...' /´¯¯·¸ \n.......... / '/.../..../....... /¨¯\ \n........('(...´...´.... ¯~/'...') \n.........\.................'..... / \n..........''...\.......... _.·´\n............\..............( \n..............\.............\..."
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


@bot.on(command(pattern="emoji ?(.*)"))
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


syntax.update({
    "reactions": f"\
Just some funny little animations ;)\
\nList of reactions:\
\n.oof\
\n.sed\
\n.hek\
\n.emoji <emoji_name>\
\nUsage: Prints the target emoji.\
\nList of included emoji(s):\
\n{unpacked_emojis}\
\n.ascii <art_name>\
\nUsage: Prints the target ascii art.\
\nList of included ASCII arts:\
\n{unpacked_ascii}\
"
})
