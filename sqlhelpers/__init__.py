import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

ENV = bool(os.environ.get("ENV", False))
if ENV:
    from production import Config
else:
    if os.path.exists("config.py"):
        from development import Config


def start() -> scoped_session:
    engine = create_engine(Config.DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
