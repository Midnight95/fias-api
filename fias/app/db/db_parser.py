from fias.app.db.model import (
    LevelType, HouseType, AddhouseType, AddressObjectType,
    ApartmentType, RoomType, Reestr, AdministrativeHierarchy,
    MunicipalHierarchy, AddressObject, House, Carplace,
    Room, Apartment, Stead
)
from sqlmodel import Session, select
from fias.app.db.db import engine


class DBStarter:
    def __init__(self):
        with Session(engine) as session:
            # load all objectid from this level
            reestr = session.exec(select(Reestr)).all()
            self.reestr = {
                obj.objectid: obj.levelid
                for obj in reestr
            }
            # load all types (drasticly reduces SQL queries)
            apart_type = session.exec(select(ApartmentType)).all()
            self.apart_type = {
                obj.id: obj.shortname
                for obj in apart_type
            }
            room_type = session.exec(select(RoomType)).all()
            self.room_type = {
                obj.id: obj.shortname
                for obj in room_type
            }
            house_type = session.exec(select(HouseType)).all()
            self.house_type = {
                obj.id: obj.shortname
                for obj in house_type
            }
            addhouse_type = session.exec(select(AddhouseType)).all()
            self.addhouse_type = {
                obj.id: obj.shortname
                for obj in addhouse_type
            }


class DBParser:
    def __init__(
            self,
            reestr: dict,
            apart_type: dict,
            room_type: dict,
            house_type: dict,
            addhouse_type: dict,
            h_type: str = 'mun'
            ):
        '''
        Finds object path.
            objectid: int
            h_type: str = 'mun' or 'adm'
            default is 'mun'
        '''
        if h_type == 'mun':
            self.hierarchy = MunicipalHierarchy
        elif h_type == 'adm':
            self.hierarchy = AdministrativeHierarchy
        else:
            raise ValueError('Looks like you chose wrong hierarchy')

        self.reestr: dict = reestr
        self.apart_type: dict = apart_type
        self.room_type: dict = room_type
        self.house_type: dict = house_type
        self.addhouse_type: dict = addhouse_type

    def _load_by_objectid(self, session,  objectid: int, model):
        st = select(model).where(model.objectid == objectid)
        obj = session.exec(st)
        return obj.first()

    def find_obj_path(self, session, objectid: int):
        st = select(
                self.hierarchy
                ).where(self.hierarchy.objectid == objectid)
        path = session.exec(st)
        if path:
            return path.first()

    def collect_current_path(self, session, objectid: int) -> str:
        path_string = []
        item_level = self.reestr[objectid]
        if item_level in range(1, 9):
            obj = self._load_by_objectid(session, objectid, AddressObject)
            path_string.append(obj.typename)
            path_string.append(obj.name)
        elif item_level == 9:
            obj = self._load_by_objectid(session, objectid, Stead)
            path_string.append(obj.number)
        elif item_level == 10:
            obj = self._load_by_objectid(session, objectid, House)
            path_string.append(self.house_type[obj.housetype])
            path_string.append(obj.housenum)
            if obj.addtype1:
                add_type = self.addhouse_type[obj.addtype1]
                path_string.append(add_type)
                path_string.append(obj.addnum1)
            if obj.addtype2:
                add_type = self.addhouse_type[obj.addtype2]
                path_string.append(add_type)
                path_string.append(obj.addnum2)
        elif item_level == 11:
            obj = self._load_by_objectid(session, objectid, Apartment)
            apart_type = self.apart_type[obj.aparttype]
            path_string.append(apart_type)
            path_string.append(obj.number)
        elif item_level == 12:
            obj = self._load_by_objectid(session, objectid, Room)
            room_type = self.room_type[obj.roomtype]
            path_string.append(room_type)
            path_string.append(obj.number)
        return ' '.join(filter(None, path_string))

    def collect_obj_full_path(self, objectid: int):
        path_string = []
        with Session(engine) as s:
            path = self.find_obj_path(s, objectid)
            if path is None:
                raise ValueError(
                        f'No hierarchy path found for objectid: {objectid}'
                        )
            for item_id in path.path:
                item_level = self.reestr[item_id]
                if item_level in range(1, 9):
                    obj = self._load_by_objectid(s, item_id, AddressObject)
                    path_string.append(obj.typename)
                    path_string.append(obj.name)
                elif item_level == 9:
                    obj = self._load_by_objectid(s, item_id, Stead)
                    path_string.append(obj.number)
                elif item_level == 10:
                    obj = self._load_by_objectid(s, item_id, House)
                    path_string.append(self.house_type[obj.housetype])
                    path_string.append(obj.housenum)
                    if obj.addtype1:
                        add_type = self.addhouse_type[obj.addtype1]
                        path_string.append(add_type)
                        path_string.append(obj.addnum1)
                    if obj.addtype2:
                        add_type = self.addhouse_type[obj.addtype2]
                        path_string.append(add_type)
                        path_string.append(obj.addnum2)
                elif item_level == 11:
                    obj = self._load_by_objectid(s, item_id, Apartment)
                    apart_type = self.apart_type[obj.aparttype]
                    path_string.append(apart_type)
                    path_string.append(obj.number)
                elif item_level == 12:
                    obj = self._load_by_objectid(s, item_id, Room)
                    room_type = self.room_type[obj.roomtype]
                    path_string.append(room_type)
                    path_string.append(obj.number)
            return ' '.join(filter(None, path_string))

    def cache_entries(self, entry: list[int], cache: dict) -> None:
        """
        Creates or updates path cache IN PLACE
        """
        if cache in None:
            cache = {}
        elif entry in cache.keys():
            return

    def collect_path_strings_by_level(self, levelid: int):
        with Session(engine) as session:
            # load all objectid from this level
            objectids = session.exec(
                    select(Reestr.objectid).where(Reestr.levelid == levelid)
                ).all()

            # load all hierarchy paths
            path_list = session.exec(
                select(self.hierarchy.path).where(
                    self.hierarchy.objectid.in_(objectids)
                    )
            ).all()

            # find common prefix and diffrence
            prefix, difference = self._find_common_prefix_numpy(path_list)
            prefix_path = []
            for pfx in prefix_path:
                prefix_path.append(self.collect_path_string(pfx))
            res = []
            for diff in difference:
                res.append(' '.join(
                   [prefix_path, self.collect_path_string(diff)])
                          )
            return res

    def reverse_find_path_string(self, string: int):
        pass
