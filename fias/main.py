from fastapi import FastAPI
from fias.app.routes import types, hierarchy, addreses
from fias.app.db.db_parser import DBStarter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FIAS Address Service")


@app.on_event('startup')
def cache_data():
    loaded = DBStarter()
    app.state.reestr = loaded.reestr
    app.state.apart_type = loaded.apart_type
    app.state.room_type = loaded.room_type
    app.state.house_type = loaded.house_type
    app.state.addhouse_type = loaded.addhouse_type


routers = [
        types.router,
        hierarchy.router,
        addreses.router
        ]

for router in routers:
    app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
