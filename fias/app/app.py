from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from typing import List
from models import (  
    LevelType, HouseType, AddhouseType, AddressObjectType,
    ApartmentType, RoomType, Reestr, AdministrativeHierarchy,
    MunicipalHierarchy, AddressObject, House, Carplace,
    Room, Apartment, Stead
)

app = FastAPI()

# Database setup
from sqlmodel import create_engine
sqlite_url = "sqlite:///database.db"  # Update with your actual DB URL
engine = create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session

# LevelType Router
leveltype_router = APIRouter(prefix="/leveltypes", tags=["leveltypes"])

@leveltype_router.get("/", response_model=List[LevelType])
def get_leveltypes(session: Session = Depends(get_session)):
    return session.exec(select(LevelType)).all()

@leveltype_router.get("/{level}", response_model=LevelType)
def get_leveltype(level: int, session: Session = Depends(get_session)):
    if leveltype := session.get(LevelType, level):
        return leveltype
    raise HTTPException(404, "LevelType not found")

# Repeat similar structure for other models...


# HouseType Router
housetype_router = APIRouter(prefix="/housetypes", tags=["housetypes"])


@housetype_router.get("/", response_model=List[HouseType])
def get_housetypes(session: Session = Depends(get_session)):
    return session.exec(select(HouseType)).all()


@housetype_router.get("/{id}", response_model=HouseType)
def get_housetype(id: int, session: Session = Depends(get_session)):
    if housetype := session.get(HouseType, id):
        return housetype
    raise HTTPException(404, "HouseType not found")


# AddhouseType Router
addhousetype_router = APIRouter(prefix="/addhousetypes", tags=["addhousetypes"])


@addhousetype_router.get("/", response_model=List[AddhouseType])
def get_addhousetypes(session: Session = Depends(get_session)):
    return session.exec(select(AddhouseType)).all()


@addhousetype_router.get("/{id}", response_model=AddhouseType)
def get_addhousetype(id: int, session: Session = Depends(get_session)):
    if addhousetype := session.get(AddhouseType, id):
        return addhousetype
    raise HTTPException(404, "AddhouseType not found")

# Repeat this pattern for all other models...


# Finally, include all routers
routers = [
    leveltype_router,
    housetype_router,
    addhousetype_router,
    # Add all other routers here...
]

for router in routers:
    app.include_router(router)
