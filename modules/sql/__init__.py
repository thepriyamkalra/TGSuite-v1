import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

ENV = bool(os.environ.get("ENV", False))
if ENV:
    from env import ENV
else:
    from env import _ENV as ENV


def start() -> scoped_session:
    engine = create_engine(ENV.DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
