# For The-TG-Bot v3
# Syntax .tr <language_name>

import emoji
from googletrans import Translator


@client.on(events("tr ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    args = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        text = reply_message.message
        lang = args or "en"
    elif "|" in args:
        lang, text = args.split("|")
    else:
        await event.edit("`.tr language code` as reply to a message")
        return
    text = emoji.demojize(text.strip())
    lang = lang.strip()
    translator = Translator()
    try:
        try:
            translated = translator.translate(text, dest=lang)
        except ValueError:
            return await event.edit(f"`Language code {lang} is invalid.`")
        output_str = f"**Translated** from {translated.src} to {lang}:\n`{translated.text}`"
        await event.edit(output_str)
    except Exception as ex:
        await event.edit("`Looks like the google translator library is down, please try again later.`")
        logger.info(str(ex))


ENV.HELPER.update({
    "translate": "\
```.tr <language_code>``` (as a reply to target message)\
\nUsage: Translate target message to another language.\
\nClick [here](https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code) to see a detailed list of all language codes.\
"
})
