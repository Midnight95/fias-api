from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
