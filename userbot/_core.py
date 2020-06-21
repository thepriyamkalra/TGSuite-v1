# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import time
import sys
import psutil
import asyncio
import platform
import traceback
from datetime import datetime
from userbot import util, syntax
from telethon import __version__

DELETE_TIMEOUT = 5
@bot.on(command(pattern="reload (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def reload_plug_in(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in bot._plugins:  # pylint:disable=E0602
            bot.remove_plugin(shortname)  # pylint:disable=E0602
        bot.load_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Successfully reloaded {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load {shortname}: {e}")


@bot.on(command(pattern="(?:unload) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove_plug_in(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"{shortname} can not be removed!")
    elif shortname in bot._plugins:  # pylint:disable=E0602
        bot.remove_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Unloaded {shortname}")
    else:
        msg = await event.respond(f"{shortname} is not loaded!")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


@bot.on(command(pattern="load"))  # pylint:disable=E0602
async def install_plug_in(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await bot.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                bot._plugin_path  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                bot.load_plugin_from_file(
                    downloaded_file_name)  # pylint:disable=E0602
                await event.edit("Loaded `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Module already exists!")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@bot.on(command(pattern="share (.*)"))
async def share_plug_in(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file..")
    input_str = event.pattern_match.group(1)
    plugin = f"plugins/{input_str}.py"
    if os.path.exists(plugin):
        start = datetime.now()
        c_time = time.time()
        await bot.send_file(
            event.chat_id,
            plugin,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                util.progress(d, t, mone, c_time, "Sharing module..")
            )
        )
        end = datetime.now()
        # os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit(f"Uploaded {input_str} in {ms} seconds.")
    else:
        await mone.edit("404: Module not found")


@bot.on(command(pattern="nuke (.*)"))
async def nuke_plug_in(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file..")
    input_str = event.pattern_match.group(1)
    dest_dir = "plugins/nuked"
    plugin = f"plugins/{input_str}.py"
    plugin_split = plugin.split("/")
    plugin_split.insert(1, dest_dir)
    plugin_split.remove(plugin_split[0])
    plugin_dest = "/".join(plugin_split)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if os.path.exists(plugin):
        try:
            if os.path.exists(plugin_dest):
                os.remove(plugin_dest)
            bot.remove_plugin(input_str)
            os.rename(plugin, plugin_dest)
            await mone.edit(f"{input_str} has been nuked!")
        except Exception as e:
            await mone.edit(f"Unexpected error occured: {e}")
    else:
        await mone.edit("404: Module not found")


@bot.on(command(pattern="recover (.*)"))
async def recover_plug_in(event):
    if event.fwd_from:
        return
    mone = await event.edit("Searching for required file..")
    input_str = event.pattern_match.group(1)
    dest_dir = "plugins/nuked"
    plugin = f"plugins/{input_str}.py"
    plugin_split = plugin.split("/")
    plugin_split.insert(1, dest_dir)
    plugin_split.remove(plugin_split[0])
    plugin_dest = "/".join(plugin_split)
    if os.path.exists(plugin_dest):
        if os.path.exists(plugin):
            os.remove(plugin)
        try:
            os.rename(plugin_dest, plugin)
            try:
                bot.remove_plugin(input_str)
            except:
                pass
            bot.load_plugin(input_str)
            await mone.edit(f"{input_str} has been recovered and loaded!")
        except Exception as e:
            await mone.edit(f"Unexpected error occured: {e}")
    else:
        await mone.edit("404: Module not found")


@bot.on(command(pattern="help ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    key = event.pattern_match.group(1)
    if not key:
        msg = "💫 The-TG-Bot v3.0 Modules:"
        title = ""
        for key, value in sorted(syntax.items()):
            new_title = f"\n\n{key[0].upper()}\n\n"
            if new_title == title:
                title = "\n"
            else:
                title = new_title
            msg += f"{title}-  {key}"
            title = new_title
        msg += f"\n\nNumber of modules: **{modcount}**\nSend .help <module_name> to get help regarding a module."
        await event.edit(msg)
    else:
        msg = ""
        msg += f"Available commands for **{key}** module:\n\n"
        msg += syntax[key]
        await event.edit(msg)


@bot.on(command(pattern="about ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    uname = platform.uname()
    botuser = await bot.get_me()
    botuser = f"\nUser: `@{botuser.username}\n"
    memory = psutil.virtual_memory()
    specs = f"`System: {uname.system}\nRelease: {uname.release}\nVersion: {uname.version}\nProcessor: {uname.processor}\nMemory [RAM]: {get_size(memory.total)}`"
    help_string = f"**The-TG-Bot v3.0 is running.**\n\n**General Info:**\n`Build Version: {build} {botuser}`Github Repository: `https://github.com/PriyamKalra/The-TG-Bot-3.0\n\n**System Specifications:**\n{specs}\n```Python: {sys.version}```\n```Telethon: {__version__}```\n\n**Developed By:** @A_FRICKING_GAMER"
    await event.edit(help_string + "\n\n")


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


syntax.update({
    "core": "\
```.load <as_a_reply_to_a_module_file>```\
\nUsage: Load a specified module.\
\n\n```.about```\
\nUsage: Returns userbot's system stats and some general information.\
\n\n```.reload <module_name>```\
\nUsage: Reload any module that was unloaded.\
\n\n```.unload <module_name>```\
\nUsage: Unload any loaded module.\
\n\n```.share <module_name>```\
\nUsage: Share any loaded module.\
\n\n```.nuke <module_name>```\
\nUsage: Nuke any module, loaded or unloaded.\
\n\n```.recovery <module_name>```\
\nUsage: Recover and load any nuked module.\
"
})
