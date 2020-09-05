# For The-TG-Bot v3
# By Priyam Kalra
# Syntax .search <text>




@client.on(events(pattern="curtana ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_args = event.pattern_match.group(1)
    # Tweak input for lower chance of failure
    args = input_args.split()[0]
    args = f"#{args}"
    chat = "@curtanaupdates"
    async for message in client.iter_messages(chat):
        msg = message.text
        if msg is None:
            msg = ""
        if args.lower() in msg.lower():
            result = message
            break
        else:
            result = f"Nothing found for query:\n {input_args}"
    await event.delete()
    await client.send_message(
        event.chat_id,
        result,
        reply_to=reply,
        parse_mode="HTML",
        force_document=False,
        silent=True
    )

ENV.HELPER.update({"curtana": "\
```.curtana <rom_name>```\
\nUsage: Returns the latest build for a custom rom.\
\n```.curtana <kernel_name>```\
\nUsage: Returns the latest build for a custom kernel.\
\n```.curtana lrtwrp```\
\nUsage: Returns the latest lrtwrp build.\
\n\nUsing .curtana rom / .curtana kernel will return latest rom or kernel.\
"})
