# For The-TG-Bot v3
# By Priyam Kalra

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto

if not hasattr(client.storage, "userObj"):
    client.storage.userObj = False


@client.on(events("clone ?(.*)"))
async def clone(event):
    if event.fwd_from:
        return
    inputArgs = event.pattern_match.group(1)
    if "-r" in inputArgs:
        await event.edit("`Reverting to my true identity..`")
        if not client.storage.userObj:
            return await event.edit("`You need to clone a profile before reverting!`")
        await updateProfile(client.storage.userObj, reset=True)
        await event.edit("`Feels good to be back.`")
        return
    elif "-d" in inputArgs:
        client.storage.userObj = False
        await event.edit("`The profile backup has been nuked.`")
        return
    if not client.storage.userObj:
        client.storage.userObj = await event.client(GetFullUserRequest(event.from_id))
    logger.info(client.storage.userObj)
    userObj = await getUserObj(event)
    await event.edit("`Stealing this random person's identity..`")
    await updateProfile(userObj)
    await event.edit("`I am you and you are me.`")


async def updateProfile(userObj, reset=False):
    firstName = "Deleted Account" if userObj.user.first_name is None else userObj.user.first_name
    lastName = "" if userObj.user.last_name is None else userObj.user.last_name
    userAbout = userObj.about if userObj.about is not None else ""
    userAbout = "" if len(userAbout) > 70 else userAbout
    if reset:
        userPfps = await client.get_profile_photos('me')
        userPfp = userPfps[0]
        await client(DeletePhotosRequest(
            id=[InputPhoto(
                id=userPfp.id,
                access_hash=userPfp.access_hash,
                file_reference=userPfp.file_reference
            )]))
    else:
        try:
            userPfp = userObj.profile_photo
            pfpImage = await client.download_media(userPfp)
            await client(UploadProfilePhotoRequest(await client.upload_file(pfpImage)))
        except:
            pass
    await client(UpdateProfileRequest(
        about=userAbout, first_name=firstName, last_name=lastName
    ))


async def getUserObj(event):
    if event.reply_to_msg_id:
        replyMessage = await event.get_reply_message()
        if replyMessage.forward:
            userObj = await event.client(
                GetFullUserRequest(replyMessage.forward.from_id or replyMessage.forward.channel_id
                                   )
            )
            return userObj
        else:
            userObj = await event.client(
                GetFullUserRequest(replyMessage.from_id)
            )
            return userObj


ENV.HELPER.update({"clone": "\
`.clone` (as a reply to a message of a user)\
\nUsage: Steals the user's identity.\
\n\n`.clone -r/-reset`\
\nUsage: Revert back to your true identity.\
\n\n`.clone -d/-del`\
\nUsage: Delete your profile's backup on your own risk.\
"})
