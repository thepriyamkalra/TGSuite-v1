# For UniBorg
# By Priyam Kalra
# Based on the note module made by RaphielGang (https://da.gd/X4Mnf)
# Syntax (.save <notename>, .get <notename>, .clear <notename>, .clearall)

from sql_helpers.global_variables_sql import LOGGER, SYNTAX
from sql_helpers.notes_sql import get_notes, rm_note, add_note, rm_all_notes
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types


@borg.on(admin_cmd(pattern="saved ?(.*)"))
async def _(svd):
    if svd.fwd_from:
        return
    notes = get_notes(svd.chat_id)
    message = "**There are no saved notes in this chat.**"
    if notes:
        message = "**Notes saved in this chat:** \n\n"
        for note in notes:
            message = message + "**~** " + note.keyword + "\n"
        await svd.edit(message)


@borg.on(admin_cmd(pattern="clear ?(.*)"))
async def _(clr):
    if clr.fwd_from:
        return
    notename = clr.pattern_match.group(1)
    rm_note(clr.chat_id, notename)
    await clr.edit(f"**Note** ```{notename}``` **cleared successfully**")


@borg.on(admin_cmd(pattern="save ?(.*)"))
async def _(fltr):
    if fltr.fwd_from:
        return
    notename = fltr.pattern_match.group(1)
    string = fltr.text.partition(notename)[2]
    if fltr.reply_to_msg_id:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
        add_note(str(fltr.chat_id), notename, string)
        await fltr.edit(
            f"**Note saved successfully.**\n**Use** ```.get {notename}``` **to get it.**"
        )


@borg.on(admin_cmd(pattern="get ?(.*)"))
async def _(getnt):
    if getnt.fwd_from:
        return
    notename = getnt.pattern_match.group(1)
    notes = get_notes(getnt.chat_id)
    for note in notes:
        if notename == note.keyword:
            await getnt.reply(f"**Required Note:** ```{notename}```\n\n{note.reply}")
            return


@borg.on(admin_cmd(pattern="clearall ?(.*)"))
async def _(prg):
    if prg.fwd_from:
        return
    if not prg.text[0].isalpha():
        await prg.edit("**Purging all notes.**")
        rm_all_notes(str(prg.chat_id))
        if LOGGER:
            await borg.send_message(
                LOGGER, f"**Successfully cleaned all notes at** ```{prg.chat_id}```"
            )


# To be used in future project, syntax module to get help on any module

SYNTAX.update({
    "notes": "\
# <notename>\
\nUsage: Gets the note with name notename\
\n\n.save <notename> <notedata>\
\nUsage: Saves notedata as a note with the name notename\
\n\n.clear <notename>\
\nUsage: Deletes the note with name notename.\
"
})
