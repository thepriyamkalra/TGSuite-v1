# By RaphielGang (https://da.gd/HlfJ)

from . import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText


class Notes(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    content = Column(UnicodeText, nullable=False)
    file = Column(UnicodeText, nullable=True)

    def __init__(self, chat_id, keyword, content, file):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.content = content
        self.file = file

Notes.__table__.create(checkfirst=True)


def get_notes(chat_id):
    try:
        return SESSION.query(Notes).filter(Notes.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_note(chat_id, keyword, content, file):
    adder = SESSION.query(Notes).get((str(chat_id), keyword))
    if adder:
        adder.content = content
        adder.file = file
    else:
        adder = Notes(str(chat_id), keyword, content, file)
        SESSION.add(adder)
    SESSION.commit()


def rm_note(chat_id, keyword):
    note = SESSION.query(Notes).filter(
        Notes.chat_id == str(chat_id), Notes.keyword == keyword)
    if note:
        note.delete()
        SESSION.commit()


def rm_all_notes(chat_id):
    notes = SESSION.query(Notes).filter(Notes.chat_id == str(chat_id))
    if notes:
        notes.delete()
        SESSION.commit()
