from fastapi import APIRouter, HTTPException, Depends, Request
from fias.app.db.db_parser import DBParser
from fias.app.routes import get_session
from sqlmodel import Session, select
from typing import List
from fias.app.db.model import (
    AddressObject, House, Carplace,
    Room, Apartment, Stead
)

router = APIRouter(prefix="/addresses", tags=["addresses"])


def get_db_cache(
        request: Request,
        hierarchy: str = 'mun'
        ) -> DBParser:
    return DBParser(
            h_type=hierarchy,
            reestr=request.app.state.reestr,
            apart_type=request.app.state.apart_type,
            room_type=request.app.state.room_type,
            house_type=request.app.state.house_type,
            addhouse_type=request.app.state.addhouse_type
            )


@router.get('/address_objects', response_model=List[AddressObject])
async def get_address_object(session: Session = Depends(get_session)):
    """
    Get json list of address_objects
        level 1 to 8
    """
    return session.exec(select(AddressObject)).all()


@router.get('/steads', response_model=List[Stead])
async def get_stead(session: Session = Depends(get_session)):
    """
    Get json list of steads
        level 9
    """
    return session.exec(select(Stead)).all()


@router.get('/houses', response_model=List[House])
async def get_house(session: Session = Depends(get_session)):
    """
    Get json list of houses
        level 10
    """
    return session.exec(select(House)).all()


@router.get('/rooms', response_model=List[Room])
async def get_room(session: Session = Depends(get_session)):
    """
    Get json list of rooms
        level 11
    """
    return session.exec(select(Room)).all()


@router.get('/apartments', response_model=List[Apartment])
async def get_apartment(session: Session = Depends(get_session)):
    """
    Get json list of rooms
        level 12
    """
    return session.exec(select(Stead)).all()


@router.get('/carplaces', response_model=List[Carplace])
async def get_carplace(session: Session = Depends(get_session)):
    """
    Get json list of carplaces
        level 17
    """
    return session.exec(select(Carplace)).all()


@router.get("/{objectid}/obj-address-string")
async def get_object_full_address(
            objectid: int,
            parser: DBParser = Depends(get_db_cache)
        ):
    """
    Get formatted address path for an object
    Parameters:
    - objectid: Address object ID from FIAS Reestr
    - hierarchy: 'mun' for municipal hierarchy (default),
                 'adm' for administrative
    """
    try:
        address_string = parser.collect_obj_full_path(objectid)
        if not address_string:
            raise HTTPException(status_code=404, detail="Address not found")
        return {"objectid": objectid, "address": address_string}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{objectid}/obj-address")
async def get_obj_address(
            objectid: int,
            parser: DBParser = Depends(get_db_cache)
        ):
    """
    Get single object by objectid. Level 1 to 8
    Parameters:
    - objectid: Address object ID from FIAS Reestr
    - hierarchy: 'mun' for municipal hierarchy (default),
                 'adm' for administrative
    """
    try:
        address_string = parser.collect_single_object(objectid)
        if not address_string:
            raise HTTPException(status_code=404, detail="Address not found")
        return {"objectid": objectid, "address": address_string}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{levelid}/level-strings")
async def get_level_strings(
        levelid: int,
        parser: DBParser = Depends(get_db_cache)
        ):
    """
    Get formatted path list of selected levelid
    Parameters:
    - levelid: Level ID from FIAS Reestr (1-12, 17)
    - hierarchy: 'mun' for municipal hierarchy (default),
                 'adm' for administrative
    Not advised to be used from level 6 to 17
    """
    try:
        level_list = parser.collect_path_strings_by_level(levelid)
        if not level_list:
            raise HTTPException(status_code=404, detail="Address not found")
        return {"levelid": levelid, "address list": level_list}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{levelid}/level-objects")
async def get_level_objects(
        levelid: int,
        parser: DBParser = Depends(get_db_cache)
        ):
    """
    Get formatted object list of selected levelid
    Parameters:
    - levelid: Level ID from FIAS Reestr (1-12, 17)
    - hierarchy: 'mun' for municipal hierarchy (default),
                 'adm' for administrative
    Not advised to be used from level 6 to 17
    """
    try:
        level_list = parser.collect_obj_by_level(levelid)
        if not level_list:
            raise HTTPException(status_code=404, detail="Address not found")
        return {"levelid": levelid, "address list": level_list}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
