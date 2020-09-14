from . import SESSION, BASE
from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func


class Blacklist(BASE):
    __tablename__ = "blacklists"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)
        self.trigger = trigger

Blacklist.__table__.create(checkfirst=True)


def get_bl(chat_id):
    try:
        return SESSION.query(Blacklist).filter(Blacklist.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_bl(chat_id, trigger):
    block = Blacklist(str(chat_id), trigger)
    SESSION.add(block)
    SESSION.commit()


def rm_bl(chat_id, trigger):
    blocked = SESSION.query(Blacklist).filter(
        Blacklist.chat_id == str(chat_id), Blacklist.trigger == trigger)
    if blocked:
        blocked.delete()
        SESSION.commit()


def rmrf_bl(chat_id):
    blacklist = SESSION.query(Blacklist).filter(Blacklist.chat_id == str(chat_id))
    if blacklist:
        blacklist.delete()
        SESSION.commit()
