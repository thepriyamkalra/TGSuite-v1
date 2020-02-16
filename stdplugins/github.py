"""Get information about an user on GitHub
Syntax: .github USERNAME"""
from telethon import events
import requests
from userbot.utils import admin_cmd
from sql_helpers.global_variables_sql import SYNTAX, MODULE_LIST

MODULE_LIST.append("github")

@borg.on(admin_cmd("github (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await borg.send_file(
            event.chat_id,
            caption="""Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}""".format(name, html_url, gh_type, company, blog, location, bio, created_at),
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event
        )
        await event.delete()
    else:
        await event.edit("`{}`: {}".format(input_str, r.text))
SYNTAX.update({
    "github": "\
**Requested Module --> GITHUB**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.github <optional_choice>```\
\nUsage:Get information about an user on GitHub\
Syntax: .github USERNAME!\
"
})