# For The-TG-Bot-3.0
# By Priyam Kalra

import os
from userbot import syntax


@bot.on(command(pattern="help ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    key = event.pattern_match.group(1)
    if not key:
        msg = "Available Modules:"
        title = ""
        for key, value in sorted(syntax.items()):
            new_title = f"\n\n{key[0].upper()}\n\n"
            if new_title == title:
                title = "\n"
            else:
                title = new_title
                msg += f"{title}~ {key}"
                title = new_title
        msg += f"\n\nSend {Config.COMMAND_HANDLER}help <module_name> to get help regarding a module."
        await event.edit(msg)
    else:
        msg += f"**{key}**\n"
        msg = syntax[key]
        await event.edit(msg)
