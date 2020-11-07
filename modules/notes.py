# For The-TG-Bot v3
# By Priyam Kalra
# Based on the note module made by RaphielGang (https://da.gd/X4Mnf)
# Syntax (.save <notename>, .get <notename>, .clear <notename>, .clearall)

from modules.sql.notes_sql import get_notes, rm_note, add_note, rm_all_notes
import time


@client.on(events(pattern="notes ?(.*)"))
async def notes(event):
    if event.fwd_from:
        return
    notes = get_notes(event.chat_id)
    message = "**There are no saved notes in this chat.**"
    if notes:
        message = "**Notes saved in this chat:** \n\n"
        for note in notes:
            message += "**~** `" + note.keyword + "`\n"
    await event.edit(message)


@client.on(events(pattern="get ?(.*)"))
async def get(event):
    if event.fwd_from:
        return
    notename = (event.pattern_match.group(1)).lower()
    reply = await event.get_reply_message()
    notes = get_notes(event.chat_id)
    for note in notes:
        if notename == note.keyword:
            file = await client.get_messages(ENV.LOGGER_GROUP, ids=int(note.file)) if note.file else None
            await client.send_message(
                event.chat_id, 
                note.content, 
                file=file, 
                reply_to=reply, 
                silent=True
            )
            return await event.delete()
    await event.edit(f"**Note** `{notename}` **not found!**")


@client.on(events(pattern="save ?(.*)"))
async def save(event):
    if event.fwd_from:
        return
    notename = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if reply and notename:
        string = reply.text
        file = None
        if reply.media:
            media = await client.send_file(ENV.LOGGER_GROUP, reply.media, caption=f"note: {notename}")
            file = str(media.id)        
        add_note(event.chat_id, notename.lower(), string, file)
        message = f"**Note saved successfully.**\n**Use** `.get {notename}` **to get it.**"
    else:
        message = f"**Reply to something to save it!**"
    await event.edit(message)


@client.on(events(pattern="clear ?(.*)"))
async def clear(event):
    if event.fwd_from:
        return
    if event.text.split()[0][1:] != "clear":
        return
    notes = get_notes(event.chat_id)
    notename = (event.pattern_match.group(1)).lower()
    status = f"**Note {notename} not found.**"
    for note in notes:
        if notename == note.keyword:
            if note.file:
                file = await client.get_messages(ENV.LOGGER_GROUP, ids=int(note.file))
                await file.delete()
            rm_note(event.chat_id, notename)
            status = f"**Note** `{notename}` **cleared successfully**"
    await event.edit(status)


@client.on(events(pattern="clearall ?(.*)"))
async def clearall(event):
    if event.fwd_from:
        return
    await event.edit("**Purging all notes.**")
    for note in get_notes(event.chat_id):
        if note.file:
            file = await client.get_messages(ENV.LOGGER_GROUP, ids=int(note.file))
            await file.delete()
    rm_all_notes(str(event.chat_id))
    await event.edit("**All notes have been purged successfully.**")
    time.sleep(2)
    await event.delete()
    status = f"**Successfully purged all notes at** `{event.chat_id}`"
    await log(status)


async def log(text):
    LOGGER = ENV.LOGGER_GROUP
    await client.send_message(LOGGER, text)

ENV.HELPER.update({
    "notes": "\
`.notes`\
\nUsage: Prints the list of notes saved in the current chat.\
\n\n`.get <notename>`\
\nUsage: Gets the note with name <notename>\
\n\n`.save <notename>` (as a reply)\
\nUsage: Saves target message as a note with the name <notename>\
\n\n`.clear <notename>`\
\nUsage: Deletes the note with name <notename>.\
\n\n`.clearall`\
\nUsage: Deletes all the notes saved in the current chat.\
"
})
