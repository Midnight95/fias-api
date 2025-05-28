from sqlmodel import Session
from fias.app.db.db import engine


def get_session():
    with Session(engine) as session:
        yield session
