# For The-TG-Bot v3
# By Priyam Kalra
# Syntax (.bio <text_to_set_as_bio>)

import asyncio
import time
from telethon.errors import FloodWaitError
from telethon.tl import functions



DEL_TIME_OUT = 70
@client.on(events(pattern="bio ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1)
    await event.delete()
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio1 = f"{DMY} "
        bio2 = f"| "
        bio3 = f" | "
        bio4 = f"{HM}"
        bio5 = bio1 + bio2 + args + bio3 + bio4
        logger.info(bio5)
        try:
            await client(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio5
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await client.send_message(  # pylint:disable=E0602
            #     ENV.LOGGER_GROUP,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)


ENV.HELPER.update({
    "bio": "\
```.bio <text>```\
\nUsage: Updates the user's bio to <text> with the date and time of modification.\
"
})
