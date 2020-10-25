from . import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText


class Filters(BASE):
    __tablename__ = "filter"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)
    content = Column(UnicodeText, nullable=False)
    file = Column(UnicodeText, nullable=True)

    def __init__(self, chat_id, trigger, content, file):
        self.chat_id = str(chat_id)
        self.trigger = trigger
        self.content = content
        self.file = file

Filters.__table__.create(checkfirst=True)


def get_filter(chat_id):
    try:
        return SESSION.query(Filters).filter(Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_filter(chat_id, trigger, content, file):
    existing = SESSION.query(Filters).get((str(chat_id), trigger))
    if existing:
        existing.content = content
        existing.file = file
    else:
        new = Filters(str(chat_id), trigger, content, file)
        SESSION.add(new)
    SESSION.commit()


def rm_filter(chat_id, trigger):
    exists = SESSION.query(Filters).filter(
        Filters.chat_id == str(chat_id), Filters.trigger == trigger)
    if exists:
        exists.delete()
        SESSION.commit()


def rmrf_filter(chat_id):
    filters = SESSION.query(Filters).filter(Filters.chat_id == str(chat_id))
    if filters:
        filters.delete()
        SESSION.commit()
