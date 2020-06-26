# For The-TG-Bot-3.0
# Modified by Priyam Kalra 6/21/2020
# Get information about an user on GitHub
# Syntax .github <username>

from userbot import syntax
import requests


@bot.on(command("github (.*)"))
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
        text = """
Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}
""".format(name, html_url, gh_type, company, blog, location, bio, created_at)
        await bot.send_file(
            event.chat_id,
            caption=text,
            file=avatar_url,
            force_document=False,
            allow_cache=False
        )
        await event.delete()
    else:
        await event.edit("`{}`: {}".format(input_str, r.text))


syntax.update({
    "github": "\
```.github <username>```\
\nUsage: Get information about any user on GitHub\
"})