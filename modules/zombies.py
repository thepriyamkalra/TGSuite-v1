# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from asyncio import sleep
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)


# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================



@client.on(events(pattern="zombies ?(.*)"))
async def handler(event):
    """ For .zombies command, list all the ghost/deleted/zombie accounts in a chat. """

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No deleted accounts found, this group is clean asf.`"

    if con != "clean":
        await event.edit("`Searching for ghost/deleted/zombie accounts...`")
        async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"`Found` **{del_u}** `ghost/deleted/zombie account(s) in this group,\
            \nclean them by using .zombies clean`"
        await event.edit(del_status)
        return

    # Here laying the sanity check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.edit("`I am not an admin here!`")
        return

    await event.edit("`Cleaning up this mess..`")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await event.edit("`I don't have ban rights in this group!`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(
                EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
            
    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"
    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin account(s) could not be removed."
        
    await event.edit(del_status)
    await sleep(2)
    await event.delete()

ENV.HELPER.update({
    "zombies": "\
```.zombies```\
\nUsage: Search for deleted accounts in the current chat.\
\n\n```.zombies clean```\
\nUsage: Clean all zombie account from the current chat.\
"
})
