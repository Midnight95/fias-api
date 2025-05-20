from sqlmodel import create_engine
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)


def upload_data(*args, **kwargs):
    # upload data from parsed xml
    pass


def update_data(*args, **kwargs):
    # updates current db using 'delta' file from fias
    pass
