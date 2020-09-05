# For The-TG-Bot v3
# By Priyam Kalra
# Based on the note module made by RaphielGang (https://da.gd/X4Mnf)
# Syntax (.save <notename>, .get <notename>, .clear <notename>, .clearall)

from modules.sql.notes_sql import get_notes, rm_note, add_note, rm_all_notes
import asyncio
import time


@client.on(events(pattern="notes ?(.*)"))
async def notes(svd):
    if svd.fwd_from:
        return
    notes = get_notes(svd.chat_id)
    message = "**There are no saved notes in this chat.**"
    if notes:
        message = "**Notes saved in this chat:** \n\n"
        for note in notes:
            message = message + "**~** `" + note.keyword + "`\n"
    await svd.edit(message)


@client.on(events(pattern="clear ?(.*)"))
async def clear(clr):
    if clr.fwd_from:
        return
    notes = get_notes(clr.chat_id)
    notelist = ""
    for note in notes:
        notelist = notelist + note.keyword
    notename = clr.pattern_match.group(1)
    status = f"**Note {notename} not found.**"
    if notename in notelist:
        rm_note(clr.chat_id, notename)
        status = f"**Note** ```{notename}``` **cleared successfully**"
    await clr.edit(status)


@client.on(events(pattern="save ?(.*)"))
async def save(fltr):
    if fltr.fwd_from:
        return
    notename = fltr.pattern_match.group(1)
    rep_msg = await fltr.get_reply_message()
    if rep_msg and notename:
        string = rep_msg.text
        add_note(str(fltr.chat_id), notename, string)
        message = f"**Note saved successfully.**\n**Use** ```.get {notename}``` **to get it.**"
    else:
        message = f"**Provide a valid note name!**"
    await fltr.edit(message)


@client.on(events(pattern="get ?(.*)"))
async def get(getnt):
    if getnt.fwd_from:
        return
    notename = getnt.pattern_match.group(1)
    notes = get_notes(getnt.chat_id)
    for note in notes:
        if notename == note.keyword:
            await getnt.reply(note.reply)
            await getnt.delete()
        else:
            await getnt.edit(f"**Note** ```{notename}``` **not found!**")


@client.on(events(pattern="clearall ?(.*)"))
async def clearall(prg):
    if prg.fwd_from:
        return
    if not prg.text[0].isalpha():
        await prg.edit("**Purging all notes.**")
        await prg.edit("**All notes have been purged successfully.**\n```This auto generated message will be deleted in a few seconds...```")
        rm_all_notes(str(prg.chat_id))
        time.sleep(5)
        await prg.delete()
        status = f"**Successfully purged all notes at** ```{prg.chat_id}```"
        await log(status)


async def log(text):
    LOGGER = ENV.LOGGER_GROUP
    await client.send_message(LOGGER, text)

ENV.HELPER.update({
    "notes": "\
```.get <notename>```\
\nUsage: Gets the note with name <notename>\
\n\n```.save <notename>``` (as a reply to message to save)\
\nUsage: Saves target message as a note with the name <notename>\
\n\n```.clear <notename>```\
\nUsage: Deletes the note with name <notename>.\
\n\n```.clearall <notename>```\
\nUsage: Deletes all the notes saved in the current chat.\
\n\n```.notes <notename>```\
\nUsage: Prints the list of notes saved in the current chat.\
"
})
