# For The-TG-Bot-3.0
# By Priyam Kalra for curtana
# Ported for realme 1 (cph1859)

from userbot import syntax


@bot.on(command(pattern="realme1 ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_args = event.pattern_match.group(1)
    # Tweak input for lower chance of failure
    args = input_args.split()[0]
    args = f"#{args}"
    chat = "@realme1updates"
    async for message in bot.iter_messages(chat):
        msg = message.text
        if msg is None:
            msg = ""
        if args.lower() in msg.lower():
            result = message
            break
        else:
            result = f"Nothing found for query:\n {input_args}"
    await event.delete()
    await bot.send_message(
        event.chat_id,
        result,
        reply_to=reply,
        parse_mode="HTML",
        force_document=False,
        silent=True
    )

syntax.update({"curtana": "\
```.realme1 <rom_name>```\
\nUsage: Returns the latest build for a custom rom.\
\n\nUsing .realme1 rom will return latest rom or kernel.\
"})
