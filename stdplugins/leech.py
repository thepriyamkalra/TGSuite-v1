import aria2p
from telethon import events
import asyncio
import os
from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("leech")

cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"
aria2_is_running = os.system(cmd)
aria2 = aria2p.API(aria2p.Client(
    host="http://localhost", port=6800, secret=""))


EDIT_SLEEP_TIME_OUT = 10


@borg.on(admin_cmd(pattern="leech ?(.*)"))
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.pattern_match.group(1)
    if var is None:
        var = await event.get_reply_message()
        var = str(var.text)
    if var is not None:
        var = str(var)
        if var.startswith("magnet:"):
            pass
        else:
            return await event.edit("Please provide a valid magnet link!")
    else:
        return await event.edit("Please provide a valid magnet link!")
    uris = [var]
    # Add URL Into Queue
    try:
        download = aria2.add_uris(uris, options=None, position=None)
    except:
        return
    gid = download.gid
    complete = None
    await progress_status(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid, event=event, previous=None)
    while complete != True:
        file = aria2.get_download(gid)
        complete = file.is_complete
        msg = f"Fetching [METADATA] for ```{file.name}```"
        await event.edit(msg)
        await asyncio.sleep(10)
    await event.edit("Fetched [METADATA], now ready to leech torrent..")


async def progress_status(gid, event, previous):
    ERROR = f"Failed to leech torrent!"
    try:
        file = aria2.get_download(gid)
        ERROR = f"Failed to leech ```{file.name}``!"
        if not file.is_complete:
            if not file.error_message:
                msg = f"Leeching ```{str(file.name)}```\nProgress info available in logger.."
                progress = f"```{file.name}``` leech info:\n\n**Speed:** {str(file.download_speed_string())}\n**Progress:** {str(file.progress_string())}\n**Total Size:** {str(file.total_length_string())}\n**ETA:** {str(file.eta_string())}\n\n"
                await log(progress)
                if previous != msg:
                    await event.edit(msg)
                    previous = msg
            else:
                await log(ERROR)
                return
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await progress_status(gid, event, previous)

        else:
            await event.edit(f"```{file.name}``` leeched successfully, starting upload..")
            return
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await log(ERROR)
            await event.edit(ERROR)
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit(ERROR)
            await log(ERROR)

        else:
            await event.edit(ERROR)
            await log(ERROR)
            return


async def log(text):
    LOGGER = Config.PRIVATE_GROUP_BOT_API_ID
    await borg.send_message(LOGGER, text)


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    return new_gid

SYNTAX.update({
    "leech": "\
**Requested Module --> leech**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.leech <magnet-link> (or as a reply to a magnet link)```\
\nUsage: Downloads the target torrent to temp download dirtory.\
\nTip: Use .upload <file-name> to upload it.\
"
})
