# For The-TG-Bot v3
# Created By @loxxi
# Modified by @TechyNewbie (23/08/20)
# Modified by @justaprudev (28/08/20)

import requests


@client.on(events("lmgtfy ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    query = input_str.replace(" ", "+")
    url = f"https://lmgtfy.com/?q={query}&iie=1"
    try:
        webpage = requests.get(url).text
        if webpage:
            await event.edit(f"More info about \"[{input_str}]({url})\"")
    except:
        await event.edit("`Something went wrong! Please try again later.`")


ENV.HELPER.update({"lmgtfy": "\
`.lmgtfy <query>`\
\nUsage: A guide on how to search on google.\
"})
