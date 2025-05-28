from fastapi import APIRouter, Depends
from fias.app.routes import get_session
from sqlmodel import Session, select
from typing import List
from fias.app.db.model import (
        LevelType,
        HouseType,
        AddhouseType,
        AddressObjectType,
        ApartmentType,
        RoomType
)

router = APIRouter(prefix='/type', tags=['type'])


@router.get('/level', response_model=List[LevelType])
def get_leveltype(session: Session = Depends(get_session)):
    """
    Get list of levels with description
        levels 13 to 16 are deprecated
    """
    return session.exec(select(LevelType)).all()


@router.get('/house', response_model=List[HouseType])
def get_housetype(session: Session = Depends(get_session)):
    """
    Get list of house types.
    Used in house table
    """
    return session.exec(select(HouseType)).all()


@router.get('/addhouse', response_model=List[AddhouseType])
def get_addhousetype(session: Session = Depends(get_session)):
    """
    Get list of addhouse types.
    """
    return session.exec(select(AddhouseType)).all()


@router.get('/addressobject', response_model=List[AddressObjectType])
def get_addgressibjecttype(session: Session = Depends(get_session)):
    """
    Get list of address objects types.
    Level 1 to 8
    """
    return session.exec(select(AddressObjectType)).all()


@router.get('/apartment', response_model=List[ApartmentType])
def get_apartmenttype(session: Session = Depends(get_session)):
    """
    Get list of appartments types.
    """
    return session.exec(select(ApartmentType)).all()


@router.get('/room', response_model=List[RoomType])
def get_roomtype(session: Session = Depends(get_session)):
    """
    Get list of room types.
    """
    return session.exec(select(RoomType)).all()
