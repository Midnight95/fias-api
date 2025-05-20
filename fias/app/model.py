from sqlmodel import SQLModel, Field, ARRAY, Column, Integer
from typing import List


class LevelType(SQLModel, table=True):
    level: int = Field(primary_key=True, default=None)
    name: str


class HouseType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str


class AddhouseType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str


class AddressObjectType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str
    level: int = Field(foreign_key='leveltype.level')


class ApartmentType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str
    shortname: str


class RoomType(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    nubmer: int
    roomtype: str


class Reestr(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            primary_key=True
            )
    level: int = Field(foreign_key='leveltype.level')


class AdministrativeHierarchy(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    path_list: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class MunicipalHierarchy(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    path_list: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class AddressObject(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    name: str
    typename: str
    level: int = Field(foreign_key='leveltype.level')


class House(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    housenum: int
    housetype: int = Field(foreign_key='housetype.id')
    addnum1: int
    addtype1: int = Field(foreign_key='addhousetype.id')
    addnum2: int
    addtype2: int = Field(foreign_key='addhousetype.id')


class Carplace(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    number: int


class Room(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    number: int
    roomtype: int = Field(foreign_key='roomtype.id')


class Apartment(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    number: int
    aparttype: int = Field(foreign_key='apartmenttype.id')


class Stead(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    objectid: int = Field(
            default=None,
            foreign_key='reestr.objectid'
            )
    number: int
