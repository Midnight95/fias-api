from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os
import fias.app.model as model
from fias.scripts.xml import (
        TypeAggregator,
        HierarchyAggregator,
        AddressAggregator
        )


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
REGION_PATH = os.getenv('REGION_PATH')
TYPES_PATH = os.getenv('TYPES_PATH')
engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def upload_types():
    '''
    upload types to database
    must be executed first
    '''
    type_agg = TypeAggregator(TYPES_PATH)

    # process levels
    level_types = type_agg.aggregate_level_types().reset_index()
    level_types.columns = ['level', 'name']
    with Session(engine) as session:
        for _, row in level_types.iterrows():
            session.add(model.LevelType(**row.to_dict()))
        session.commit()

    # process houses
    house_types = type_agg.aggregate_houses_types().reset_index()
    house_types.columns = ['id', 'name', 'shortname']
    with Session(engine) as session:
        for _, row in house_types.iterrows():
            session.add(model.HouseType(**row.to_dict()))
        session.commit()

    # process addhouses
    addhouse_types = type_agg.aggregate_addhouses_types().reset_index()
    addhouse_types.columns = ['id', 'name', 'shortname']
    with Session(engine) as session:
        for _, row in addhouse_types.iterrows():
            session.add(model.AddhouseType(**row.to_dict()))
        session.commit()

    # process address object types
    address_obj_types = type_agg.aggregate_addr_obj_types().reset_index()
    address_obj_types.columns = ['id', 'name', 'shortname', 'level']
    with Session(engine) as session:
        for _, row in address_obj_types.iterrows():
            session.add(model.AddressObjectType(**row.to_dict()))
        session.commit()

    # process apartment types
    address_obj_types = type_agg.aggregate_apartment_types().reset_index()
    address_obj_types.columns = ['id', 'name', 'shortname']
    with Session(engine) as session:
        for _, row in address_obj_types.iterrows():
            session.add(model.ApartmentType(**row.to_dict()))
        session.commit()


def upload_hierarchy():
    '''
    upload hierarchy to database
    must be executed second
    '''
    hierarchy_agg = HierarchyAggregator(REGION_PATH)

    # process reestr
    reestr = hierarchy_agg.aggregate_reestr().reset_index()
    reestr.columns = ['objectid', 'levelid']
    with Session(engine) as session:
        for _, row in reestr.iterrows():
            session.add(model.Reestr(**row.to_dict()))
        session.commit()

    # process adm hierarchy
    adm_hierarchy = hierarchy_agg.aggregate_adm_hierarchy().reset_index()
    adm_hierarchy.columns = ['objectid', 'path']
    with Session(engine) as session:
        for _, row in adm_hierarchy.iterrows():
            session.add(model.AdministrativeHierarchy(**row.to_dict()))
        session.commit()

    # process mun hierarchy
    mun_hierarchy = hierarchy_agg.aggregate_mun_hierarchy().reset_index()
    mun_hierarchy.columns = ['objectid', 'path']
    with Session(engine) as session:
        for _, row in mun_hierarchy.iterrows():
            session.add(model.MunicipalHierarchy(**row.to_dict()))
        session.commit()


def upload_addresses():
    '''
    upload addresses to database
    must be executed last
    '''
    address_aggregator = AddressAggregator(REGION_PATH)
    # aggregate address object
    addr_obj = address_aggregator.aggregate_addr_obj().reset_index()
    addr_obj.columns = ['objectid', 'name', 'typename', 'level']
    with Session(engine) as session:
        for _, row in addr_obj.iterrows():
            session.add(model.AddressObject(**row.to_dict()))
        session.commit()

    # aggregate houses
    houses = address_aggregator.aggregate_houses().reset_index()
    houses.columns = [
            'objectid',
            'housenum',
            'housetype',
            'addnum1',
            'addtype1',
            'addnum2',
            'addtype2'
            ]
    with Session(engine) as session:
        for _, row in houses.iterrows():
            session.add(model.House(**row.to_dict()))
        session.commit()

    # aggregate carplaces
    carplaces = address_aggregator.aggregate_carplaces().reset_index()
    carplaces.columns = ['objectid', 'number']
    with Session(engine) as session:
        for _, row in carplaces.iterrows():
            session.add(model.Carplace(**row.to_dict()))
        session.commit()

    # aggregate rooms
    rooms = address_aggregator.aggregate_rooms().reset_index()
    rooms.columns = ['objectid', 'number', 'roomtype']
    with Session(engine) as session:
        for _, row in rooms.iterrows():
            session.add(model.Room(**row.to_dict()))
        session.commit()

    # aggregate apartments
    apartments = address_aggregator.aggregate_appartments().reset_index()
    apartments.columns = ['objectid', 'number', 'aparttype']
    with Session(engine) as session:
        for _, row in apartments.iterrows():
            session.add(model.Apartment(**row.to_dict()))
        session.commit()

    # aggregate steads
    steads = address_aggregator.aggregate_steads().reset_index()
    steads.columns = ['objectid', 'number']
    with Session(engine) as session:
        for _, row in steads.iterrows():
            session.add(model.Stead(**row.to_dict()))
        session.commit()


def update_data(*args, **kwargs):
    # updates current db using 'delta' file
    pass


if __name__ == '__main__':
    create_tables()
