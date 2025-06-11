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


class DBCollector:
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
        return session.exec(st).first()

    def _find_obj_path(self, session, objectid: int):
        st = select(
                self.hierarchy
                ).where(self.hierarchy.objectid == objectid)
        path = session.exec(st)
        if path:
            return path.first()

    def _get_obj(self, s, objectid: int):
        level = self.reestr.get(objectid)
        if level is None:
            return
        result = {}
        if 1 <= level <= 8:
            obj = self._load_by_objectid(s, objectid, AddressObject)
            result['typename'] = obj.typename
            result['name'] = obj.name
        elif level == 9:
            obj = self._load_by_objectid(s, objectid, Stead)
            result['number'] = obj.number
        elif level == 10:
            obj = self._load_by_objectid(s, objectid, House)
            result['house-type'] = self.house_type[obj.housetype]
            result['housenum'] = obj.housenum
            if obj.addtype1:
                result['addtype1'] = self.addhouse_type[obj.addtype1]
                result['addnum1'] = obj.addnum1
            if obj.addtype2:
                result['addtype2'] = self.addhouse_type[obj.addtype2]
                result['addnum2'] = obj.addnum2
        elif level == 11:
            obj = self._load_by_objectid(s, objectid, Apartment)
            result['apart-type'] = self.apart_type[obj.aparttype]
            result['number'] = obj.number
        elif level == 12:
            obj = self._load_by_objectid(s, objectid, Room)
            result['room-type'] = self.room_type[obj.roomtype]
            result['number'] = obj.number
        elif level == 17:
            obj = self._load_by_objectid(s, objectid, Carplace)
            result['number'] = obj.number

        return result


class DBParser(DBCollector):
    def __init__(
            self,
            reestr: dict,
            apart_type: dict,
            room_type: dict,
            house_type: dict,
            addhouse_type: dict,
            h_type: str = 'mun'
            ):
        super().__init__(
                reestr,
                apart_type,
                room_type,
                house_type,
                addhouse_type,
                h_type
                )

    def collect_single_object(self, objectid):
        with Session(engine) as s:
            return self._get_obj(s, objectid)

    def collect_obj_full_path(self, objectid: int):
        path_string = []
        with Session(engine) as s:
            path = self._find_obj_path(s, objectid)
            if path is None:
                raise ValueError(
                        f'No hierarchy path found for objectid: {objectid}'
                        )
            for item_id in path.path:
                obj_data = self._get_obj(s, item_id)
                part = ' '.join(filter(None, obj_data.values()))
                path_string.append(part)

            return ' '.join(filter(None, path_string))

    def collect_path_strings_by_level(self, levelid: int):
        res = []
        cache = {}
        with Session(engine) as s:
            # load all objectid from this level
            objects = s.exec(
                    select(Reestr.objectid).where(Reestr.levelid == levelid)
                ).all()

            # load all hierarchy paths
            path_list = s.exec(
                select(self.hierarchy.path).where(
                    self.hierarchy.objectid.in_(objects)
                    )
            ).all()
            for path in path_list:
                for item_id in path:
                    if cache.get(item_id) is None:
                        obj_data = self._get_obj(s, item_id)
                        cache[item_id] = ' '.join(
                                filter(None, obj_data.values())
                                )

                res.append({
                    'objectid': item_id,
                    'address': ' '.join([cache[id] for id in path])
                        }
                    )

            # find common prefix and diffrence
            return res

    def collect_obj_by_level(self, levelid: int):
        res = []
        with Session(engine) as s:
            # load all objectid from this level
            objects = s.exec(
                    select(Reestr.objectid).where(Reestr.levelid == levelid)
                ).all()
            for object_id in objects:
                current = {'objectid': object_id}
                current.update(self._get_obj(s, object_id))
                res.append(current)
        return res

    def reverse_find_path_string(self, string: int):
        pass
