from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional


class ObjectLevelType(SQLModel, table=True):
    level: int = Field(primary_key=True)
    name: str


class HouseType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    shortname: str


class AddHouseType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    shortname: str


class AddressObjectType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    shortname: str
    level: int = Field(foreign_key='objectleveltype.level')


class ApartmentType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    shortname: str


class RoomType(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nubmer: int
    roomtype: str


class ObjectLevels(SQLModel, table=True):
    objectid: int = Field(primary_key=True)
    level: int = Field(foreign_key='objectleveltype.level')


class AdministrativeHierarchy(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path1: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path2: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path3: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path4: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path5: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path6: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path7: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path8: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )


class MunicipalHierarchy(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            primary_key=True
            )
    path1: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path2: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path3: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path4: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path5: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path6: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path7: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    path8: Optional[int] = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )


class AddressObject(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            primary_key=True
            )
    name: str
    typename: str
    level: int = Field(foreign_key='objectlevel.level')


class House(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    housenum: int
    housetype: int = Field(foreign_key='housetype.id')
    addnum1: int
    addtype1: int = Field(foreign_key='addhousetype.id')
    addnum2: int
    addtype2: int = Field(foreign_key='addhousetype.id')


class Carplace(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    number: int


class Room(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    number: int
    roomtype: int = Field(foreign_key='roomtype.id')


class Apartment(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    number: int
    aparttype: int = Field(foreign_key='apartmenttype.id')


class Stead(SQLModel, table=True):
    objectid: int = Field(
            default=None,
            foreign_key='objectlevels.objectid'
            )
    number: int
