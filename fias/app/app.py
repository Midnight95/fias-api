from fias.app.db import engine, update_data, upload_data
from sqlmodel import SQLModel
import fias.app.model  # noqa


def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
