# The-TG-Bot Plugin for Torrent Search from torrent-paradise.ml
# Author: Nageen (https://github.com/archie9211) (@archie9211)
# Kanged by @InevitableThanos

import re
import requests


@client.on(events("torrent +(.*)"))
async def torr_search(message):
    await message.edit("`Sailing the Pirateship!`")
    input_ = message.pattern_match.group(1)
    max_limit = 10
    get_limit = re.compile(r"-l\d*[0-9]")
    query = re.sub(r"-\w*", "", input_).strip()
    r = requests.get("https://torrent-paradise.ml/api/search?q=" + query)
    if get_limit.search(input_) is not None:
        max_limit = int(get_limit.search(input_).group().strip("-l"))
    try:
        torrents = r.json()
        reply_ = ""
        torrents = sorted(torrents, key=lambda i: i["s"], reverse=True)
        for torrent in torrents[: min(max_limit, len(torrents))]:
            if len(reply_) < 4096 and torrent["s"] > 0:
                try:
                    reply_ = (
                        reply_ + f"\n\n<b>{torrent['text']}</b>\n"
                        f"<b>Size:</b> {humanbytes(torrent['len'])}\n"
                        f"<b>Seeders:</b> {torrent['s']}\n"
                        f"<b>Leechers:</b> {torrent['l']}\n"
                        f"<code>magnet:?xt=urn:btih:{torrent['id']}</code>"
                    )
                except Exception:
                    pass
        if reply_ == "":
            await message.edit(f"`Pirates were unsuccesful in finding {query}!`")
        else:
            await message.edit(text=reply_, parse_mode="html")
    except Exception:
        await message.edit("`Pirates are tired!\nAsk them later!`")
ENV.HELPER.update({
    "torrent": "\
```.torrent <query>```\
\nUsage: Searches the torrent sites for your query.\
"
})
