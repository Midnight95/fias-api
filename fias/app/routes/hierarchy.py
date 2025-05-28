from fastapi import Depends, APIRouter
from sqlmodel import Session, select
from typing import List
from fias.app.db.model import (
    Reestr, AdministrativeHierarchy,
    MunicipalHierarchy
)
from fias.app.routes import get_session


router = APIRouter(prefix='/hierarchy', tags=['hierarchy'])


@router.get('/reestr', response_model=List[Reestr])
async def get_reestr(session: Session = Depends(get_session)):
    return session.exec(select(Reestr)).all()


@router.get(
        '/adm_hierarchy',
        response_model=List[AdministrativeHierarchy]
        )
async def get_adm_hierarchy(session: Session = Depends(get_session)):
    return session.exec(select(AdministrativeHierarchy)).all()


@router.get(
        '/mun_hierarchy',
        response_model=List[MunicipalHierarchy]
        )
async def get_mun_hierarchy(session: Session = Depends(get_session)):
    return session.exec(select(MunicipalHierarchy)).all()
