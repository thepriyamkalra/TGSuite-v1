import requests
import random

themes = [
    "3024-night", "a11y-dark", "blackboard", "base16-dark", "base16-light",
    "cobalt", "dracula", "duotone-dark", "hopscotch", "lucario", "material",
    "monokai", "night-owl", "nord", "oceanic-next", "one-light", "one-dark",
    "panda-syntax", "paraiso-dark", "seti", "shades-of-purple", "solarized-dark",
    "solarized-light", "synthwave-84", "twilight", "verminal", "vscode",
    "yeti", "zenburn"
]


@client.on(events("carbon ?(.*)"))
async def carbonize(e):
    await e.edit("`Cooking a carbon..`")
    args = e.pattern_match.group(1)
    text = "%20".join(args.split()[:-1])
    theme = args.split()[-1]
    if theme not in themes:
        theme = "base16-dark"
        text = "%20".join(args.split())
    try:
        await client.send_file(
            e.chat_id,
            caption="@The_TG_Bot",
            file=requests.get(
                f"https://sjprojectsapi.herokuapp.com/carbon/?text={text}&theme={theme}&bg=black").json()['link'],
            force_document=False
        )
        await e.delete()
    except Exception:
        await e.edit("`API is down! Try again later.`")


ENV.HELPER.update({
    "carbon": f"\
```.carbon <input_text_here> (option: <theme_name>)```\
\nUsage: Make your code look nice.\
\nList of available themes:\
\n`{themes}`\
"
})
