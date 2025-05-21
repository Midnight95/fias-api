import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from typing import List
from fias.app.model import (
    LevelType, HouseType, AddhouseType, AddressObjectType,
    ApartmentType, RoomType, Reestr, AdministrativeHierarchy,
    MunicipalHierarchy, AddressObject, House, Carplace,
    Room, Apartment, Stead
)
from sqlmodel import create_engine

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = FastAPI()

# Database setup
engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


# type router
type_router = APIRouter(prefix='/type', tags=['type'])


@type_router.get('/level', response_model=List[LevelType])
def get_leveltype(session: Session = Depends(get_session)):
    return session.exec(select(LevelType)).all()


@type_router.get('/house', response_model=List[HouseType])
def get_housetype(session: Session = Depends(get_session)):
    return session.exec(select(HouseType)).all()


@type_router.get('/addhouse', response_model=List[AddhouseType])
def get_addhousetype(session: Session = Depends(get_session)):
    return session.exec(select(AddhouseType)).all()


@type_router.get('/addressobject', response_model=List[AddressObjectType])
def get_addgressibjecttype(session: Session = Depends(get_session)):
    return session.exec(select(AddressObjectType)).all()


@type_router.get('/apartment', response_model=List[ApartmentType])
def get_apartmenttype(session: Session = Depends(get_session)):
    return session.exec(select(ApartmentType)).all()


@type_router.get('/room', response_model=List[RoomType])
def get_roomtype(session: Session = Depends(get_session)):
    return session.exec(select(RoomType)).all()


# hierarchy router
hierarchy_router = APIRouter(prefix='/hierarchy', tags=['hierarchy'])


@hierarchy_router.get('/reestr', response_model=List[Reestr])
def get_reestr(session: Session = Depends(get_session)):
    return session.exec(select(Reestr)).all()


@hierarchy_router.get(
        '/adm_hierarchy',
        response_model=List[AdministrativeHierarchy]
        )
def get_adm_hierarchy(session: Session = Depends(get_session)):
    return session.exec(select(AdministrativeHierarchy)).all()


@hierarchy_router.get(
        '/mun_hierarchy',
        response_model=List[MunicipalHierarchy]
        )
def get_mun_hierarchy(session: Session = Depends(get_session)):
    return session.exec(select(MunicipalHierarchy)).all()


# address router
address_router = APIRouter(prefix='/address', tags=['address'])


@address_router.get('/address_object', response_model=List[AddressObject])
def get_address_object(session: Session = Depends(get_session)):
    return session.exec(select(AddressObject)).all()


@address_router.get('/house', response_model=List[House])
def get_house(session: Session = Depends(get_session)):
    return session.exec(select(House)).all()


@address_router.get('/carplace', response_model=List[Carplace])
def get_carplace(session: Session = Depends(get_session)):
    return session.exec(select(Carplace)).all()


@address_router.get('/room', response_model=List[Room])
def get_room(session: Session = Depends(get_session)):
    return session.exec(select(Room)).all()


@address_router.get('/apartment', response_model=List[Apartment])
def get_apartment(session: Session = Depends(get_session)):
    return session.exec(select(Stead)).all()


@address_router.get('/stead', response_model=List[Stead])
def get_stead(session: Session = Depends(get_session)):
    return session.exec(select(Stead)).all()


routers = [
    type_router,
    hierarchy_router,
    address_router
]

for router in routers:
    app.include_router(router)
