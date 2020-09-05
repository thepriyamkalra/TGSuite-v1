# For The-TG-Bot v3
# By Priyam Kalra
# Syntax (.say <text_to_print>)

import time



@client.on(events(pattern="say ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input = event.pattern_match.group(1)
    if not input:
        abe = await event.get_reply_message()
        input = abe.text
    strings = input.split()
    count = 0
    output = ""
    for _ in strings:
        output += f"{strings[count]}\n"
        count += 1
        await event.edit(output)
        time.sleep(0.25)

ENV.HELPER.update({
    "say": "\
```.say <text_to_print> (or as a reply to target message)```\
\nUsage: Says anything you want it to say.\
"
})
