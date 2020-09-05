# For The-TG-Bot v3
# By Priyam Kalra
# Syntax .oof, .sed, .emoji, .ascii



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
    "mf": "......................................../´¯/) \n......................................,/¯../ \n...................................../..../ \n..................................../´.¯/ \n..................................../´¯/ \n..................................,/¯../ \n................................../..../ \n................................./´¯./ \n................................/´¯./ \n..............................,/¯../ \n............................./..../ \n............................/´¯/ \n........................../´¯./ \n........................, /¯.. / \n......................./.... / \n...................... /´¯/ \n...................., /¯.. / \n.................../.... / \n............. /´¯/\'...' /´¯¯·¸ \n.......... / '/.../..../....... /¨¯\ \n........('(...´...´.... ¯~/'...') \n.........\.................'..... / \n..........''...\.......... _.·´\n............\..............( \n..............\.............\...",
    "f" : "\n\n⠀⠀⢀⡤⢶⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⢀⣠⣤⣤⣤⣿⣧⣀⣀⣀⣀⣀⣀⣀⣀⣤⡄⠀ ⢠⣾⡟⠋⠁⠀⠀⣸⠇⠈⣿⣿⡟⠉⠉⠉⠙⠻⣿⡀ ⢺⣿⡀⠀⠀⢀⡴⠋⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠙⠇ ⠈⠛⠿⠶⠚⠋⣀⣤⣤⣤⣿⣿⣇⣀⣀⣴⡆⠀⠀⠀ ⠀⠀⠀⠀⠠⡞⠋⠀⠀⠀⣿⣿⡏⠉⠛⠻⣿⡀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠈⠁⠀⠀ ⠀⠀⣠⣶⣶⣶⣶⡄⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀ ⠀⢰⣿⠟⠉⠙⢿⡟⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀ ⠀⢸⡟⠀⠀⠀⠘⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀ ⠀⠈⢿⡄⠀⠀⠀⠀⠀⣼⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠙⠷⠶⠶⠶⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀\n\n"
}    

unpacked_ascii = ""
for art in ascii:
    unpacked_ascii += f"`{art}`\n"


@client.on(events(pattern="oof ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    oof = event.pattern_match.group(1)
    if not oof:
        oof = 10
    try:
        oof = int(oof)
    except:
        oof = 10
    oof = int(oof/2)
    output = ""
    for _ in range(oof):
        output += "oo"
        await event.edit(output)
    output += "f"
    await event.edit(output)


@client.on(events(pattern="hek ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    for _ in range(5):
        await event.edit(";_;")
        await event.edit("_;;")
        await event.edit(";;_")
    await event.edit(";_;")


@client.on(events(pattern="sed ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    for _ in range(4):
        await event.edit(":/")
        await event.edit(":|")
        await event.edit(":\\")
        await event.edit(":|")
    await event.edit(":/")


@client.on(events(pattern="emoji ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        req_emoji = emojis[str(input_str)]
        await event.edit(req_emoji)
    except KeyError:
        await event.edit("Emoji not found!")


@client.on(events(pattern="ascii ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        req_ascii = ascii[str(input_str)]
        await event.edit(req_ascii)
    except KeyError:
        await event.edit("ASCII art not found!")


ENV.HELPER.update({
    "reactions": f"\
Just some funny little animations ;)\
\nList of reactions:\
`\
\n.oof\
\n.sed\
\n.hek\
`\
\n\n .emoji <emoji_name>\
\nUsage: Prints the target emoji.\
\nList of included emoji(s):\
\n{unpacked_emojis}\
\n.ascii <art_name>\
\nUsage: Prints the target ascii art.\
\nList of included ASCII arts:\
\n{unpacked_ascii}\
"
})
