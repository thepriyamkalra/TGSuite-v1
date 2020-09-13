from . import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func


class Filters(BASE):
    __tablename__ = "filter"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, trigger, reply):
        self.chat_id = str(chat_id)
        self.trigger = trigger
        self.reply = reply

Filters.__table__.create(checkfirst=True)


def get_filter(chat_id):
    try:
        return SESSION.query(Filters).filter(Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_filter(chat_id, trigger, reply):
    existing = SESSION.query(Filters).get((str(chat_id), trigger))
    if existing:
        existing.reply = reply
    else:
        new = Filters(str(chat_id), trigger, reply)
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
