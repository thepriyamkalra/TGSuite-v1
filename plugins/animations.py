from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import asyncio

from telethon.tl.types import ChannelParticipantsAdmins
from userbot import syntax

@bot.on(command("gmailhack ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    botuser = await bot.get_me()
    botuser = f"@{botuser.username}"
    animation_interval = 0.7
    animation_ttl = range(0, 20)      
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.from_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.from_id
        # Giving myself protection from getting hacked XD
        if idd == 1109396517:
            await reply_message.reply(f"`Wait a second, @TechyNewbie is My Boss!`\n**How dare you even think to hack my boss' google account stupid!**\n\n__Your account will be hacked in a few minutes! Pay 50$ to my Boss__ [Mp $inGH✪](https://t.me/TechyNewbie) __OR delete your telegram account to prevent the virus getting into your Gmail account __😏")
        else:
            animation_chars = [
        
            "`Connecting To Dark WEB Secret Server...`",
            "`Connection Successful!`",
            "`Targetting` [{}](tg://user?id={})'s `Google Account.`".format(firstname, idd),
            "`Attempting method I... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Method I FAILED!`",
            "`Attempting method II... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Method II Out Of Order!`",
            "`Attempting method III... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Disabling Account Security... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Getting Password... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Pulling Information... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Modifying Recovery Information... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Modifying Recovery Information... 69%\n█████████████████▒▒▒▒▒▒▒▒ `",
            "`Hacking... 74%\n███████████████████▒▒▒▒▒▒ `",
            "`Hacking.... 80%\n█████████████████████▒▒▒▒ `",
            "`Adding Modules... 86%\n██████████████████████▒▒▒ `",
            "`Adding Finishing Touches... 98%\n████████████████████████▒`",
            "`HACKED 100%\n█████████████████████████ `",
            f"{botuser} `Has Hacked` [{firstname}](tg://user?id={idd})'s `Google Account Successfully...`\n[{firstname}](tg://user?id={idd})'s __account is under Boss' control now__\n\n**Pay 50$ To** {botuser} **Or Get Ready To Lose all your YouTube Subscribers and See Your Mail Full Of Spams.**"
        ]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 20])


@bot.on(command("hack ?(.*)"))
async def func(var):
    if var.fwd_from:
        return
    botuser = await bot.get_me()
    botuser = f"@{botuser.username}"
    animation_interval = 0.7
    animation_ttl = range(0, 21)
    animation_chars = [
        "`Connecting To DarkWEB Secret Server...`",
        "`Connection Successful!`",
        "`Targetting your Telegram Account`",
        "`Target Selected.`",
        "`Attempting method 1... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Method 1 FAILED!`",
        "`Attempting method 2... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Removing Encryption... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Getting API ID and API Hash.. 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Getting API ID and API Hash... 17%\n████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Uploding Information... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking. 29%\n███████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking.. 35%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 43%\n███████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`modifying INFORMATION... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`MODIFYING information... 58%\n███████████████▒▒▒▒▒▒▒▒▒▒ `",
        "`modifying INFORMATION... 69%\n█████████████████▒▒▒▒▒▒▒▒ `",
        "`Adding Modules... 84%\n█████████████████████▒▒▒▒ `",
        "`Adding Finishing Touches... 98%\n████████████████████████▒`",
        "`HACKED... 100%\n█████████████████████████ `",
        f"`Your Telegram Account Hacked Successfully...`\n__Your userbot will now start spamming everywhere...__\n\n**Pay 25$ To** {botuser} **Or delete your account.**"
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await var.edit(animation_chars[i % 21])


@bot.on(command("police ?(.*)"))
async def func(fir):
    if fir.fwd_from:
        return
    botuser = await bot.get_me()
    botuser = f"@{botuser.first_name}"
    animation_interval = 1
    animation_ttl = range(0, 37)
    if fir.reply_to_msg_id:
        reply_message = await fir.get_reply_message()
        replied_user = await fir.client(GetFullUserRequest(reply_message.from_id))
        username = replied_user.user.username
        animation_chars = [
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",    
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
            "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
            "**Telegram Security Service is on its way here.**",
            "**Telegram Security Service is on its way here..**",
            "**Telegram Security Service is on its way here...**",
            "**Directly entering this Chat.**",
            "**Directly entering this Chat..**",
            "Via",
            "Server",
            "`2048`",
            "`2048.786`",
            "`2048.786.69`",
            "`2048.786.69.1`",
            "Passing through Narrow and Complicated Servers.",
            "Passing through Narrow and Complicated Servers..",
            f"**{botuser} Police is here**",
            f"**{botuser} Police is here!!**",
            "Looking for Guilty.",
            "Looking for Guilty..",
            "Looking for Guilty...",
            "Getting F.I.R..",
            "Getting F.I.R...",
            "**!!Guilty Arrested!!**",
            "**!! Guilty Arrested !!**",
            "__user BANNED from TELEGRAM__",
            "__USER banned FROM telegram__",
            "__user BANNED from TELEGRAM__",
            f"***JUSTICE***\n\nPolice has arrested {username} on the appeal of {botuser}!"
        ]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await fir.edit(animation_chars[i % 37])

                   
syntax.update({
    "animations": "\
**HACKING**\
\n• ```.hack``` (as a reply to message)\
\nUsage: __Hacks the Telegram account of the targeted user.__\
\n• ```.gmailhack``` (as a reply to message)\
\nUsage: __Hacks the Google account of the targeted user.__\
\n\n**POLICE**\
\n• `.police`\
\nUsage: __You need Police sometimes.__\
\n\n**SOLAR SYSTEM**\
\n• `.moon`\
\nUsage: __Moon animation__\
\n• `.earth`\
\nUsage: __Earth animation__\
\n• `.chandrayaan`\
\nUsage: __Based on Chandrayaan 2 by ISRO__\
\n• `.solarsystem`\
\nUsage: __kensar Solar System animation__\
\n\nMore Coming Soon...\
"
})
