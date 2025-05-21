from sqlmodel import SQLModel, Field, ARRAY, Column, Integer, BigInteger
from typing import List


class LevelType(SQLModel, table=True):
    level: int = Field(primary_key=True, default=None)
    name: str


class HouseType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str | None


class AddhouseType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str | None


class AddressObjectType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str | None
    level: int = Field(foreign_key='leveltype.level')


class ApartmentType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str | None


class RoomType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str | None


class Reestr(SQLModel, table=True):
    objectid: int = Field(
            primary_key=True
            )
    levelid: int = Field(foreign_key='leveltype.level')


class AdministrativeHierarchy(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    path: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class MunicipalHierarchy(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    path: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class AddressObject(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    name: str
    typename: str
    level: int = Field(foreign_key='leveltype.level')


class House(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None, sa_type=BigInteger)
    objectid: int = Field(
            foreign_key='reestr.objectid',
            sa_type=BigInteger,
            )
    housenum: str | None = None
    housetype: int | None = Field(foreign_key='housetype.id', default=None)
    addnum1: str | None = None
    addtype1: int | None = Field(foreign_key='addhousetype.id', default=None)
    addnum2: str | None = None
    addtype2: int | None = Field(foreign_key='addhousetype.id', default=None)


class Carplace(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    number: str


class Room(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    number: str
    roomtype: int = Field(foreign_key='roomtype.id')


class Apartment(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    number: str
    aparttype: int | None = Field(foreign_key='apartmenttype.id', default=None)


class Stead(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            foreign_key='reestr.objectid'
            )
    number: str
