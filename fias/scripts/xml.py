import xml.etree.ElementTree as ET
import pandas as pd
import os


class XML:
    """
    path: str
        abspath to gar_xml/93/
    """

    def __init__(self, path: str):
        self._path = path

    def _parse_xml(self, filename) -> pd.DataFrame:
        """
        Make XML file into a pandas dataframe (df)
        filename (abspath): str
        """
        tree = ET.parse(filename)
        root = tree.getroot()
        df = [child.attrib for child in root]
        df = pd.DataFrame.from_dict(df)
        return df

    def _get_active(self, filename):
        """
        find active values
        """
        return self._parse_xml(filename).query('ISACTIVE == "1"')

    def _get_filename(self, start: str) -> str:
        """
        find filename in region direcotry
        """
        file_list = os.listdir(self._path)
        for file in file_list:
            if file.startswith(start):
                filename = os.path.join(self._path, file)
                break
        else:
            raise FileNotFoundError(
                    f'Looks like there is no {start} file in directory'
                    )
        return filename


class TypeAggregator(XML):
    def __init__(self, path):
        super().__init__(path)

    def _get_active(self, filename):
        """
        find active values
        """
        return self._parse_xml(filename).query('ISACTIVE == "true"')

    def aggregate_houses_types(self):
        file_path = self._get_filename('AS_HOUSE_TYPES')
        df = self._get_active(file_path)
        return df.set_index('ID')[['NAME', 'SHORTNAME']]

    def aggregate_addhouses_types(self):
        file_path = self._get_filename('AS_ADDHOUSE_TYPES')
        df = self._get_active(file_path)
        return df.set_index('ID')[['NAME', 'SHORTNAME']]

    def aggregate_addr_obj_types(self):
        file_path = self._get_filename('AS_ADDR_OBJ_TYPES')
        df = self._get_active(file_path)
        return df.set_index('ID')[['NAME', 'SHORTNAME', 'LEVEL']]

    def aggregate_apartment_types(self):
        file_path = self._get_filename('AS_APARTMENT_TYPES')
        df = self._get_active(file_path)
        return df.set_index('ID')[['NAME', 'SHORTNAME']]

    def aggregate_object_levels(self):
        """
        Aggregates object leves.
        Used for reference
        """
        file_path = self._get_filename('AS_OBJECT_LEVELS')
        df = self._get_active(file_path)
        return df.set_index('LEVEL')['NAME']


class HierarchyAggregator(XML):
    def __init__(self, path):
        super().__init__(path)

    def _aggregate_reestr_obj(self) -> dict:
        file_path = self._get_filename('AS_REESTR_OBJECTS')
        df = self._get_active(file_path)
        return df[['OBJECTID', 'LEVELID']]

    def aggregate_lvl_to_objid(self):
        """
        aggregates lvlid to objectid
           pd.Dataframe[lvlid, objectid: list[str]]
        """
        df = self._aggregate_reestr_obj()
        return df.groupby(
                'LEVELID'
                )['OBJECTID'].apply(list).to_frame()

    def aggregate_objid_to_lvl(self):
        """
        aggregates objectid to levelid
           pd.Dataframe[objectid, levelid]
        """
        df = self._aggregate_reestr_obj()
        return df.set_index('OBJECTID')['LEVELID'].to_frame()

    def aggregate_adm_hierarchy(self) -> dict:
        """
        aggregates administrative hierarchy
           pd.Dataframe[objectid, path: list[str]]
        """
        file_path = self._get_filename('AS_ADM_HIERARCHY')
        df = self._get_active(file_path)
        return df.set_index(
                'OBJECTID'
                )['PATH'].str.split('.').to_frame()

    def aggregate_mun_hierarchy(self) -> dict:
        """
        aggregates municipal hierarchy
           pd.Dataframe[objectid, path: list[str]]
        """
        file_path = self._get_filename('AS_MUN_HIERARCHY')
        df = self._get_active(file_path)
        return df.set_index(
                'OBJECTID'
                )['PATH'].str.split('.').to_frame()


class AddressAggregator(XML):
    def __init__(self, path):
        super().__init__(path)

    def aggregate_addr_obj(self):
        """
        Aggregates address objects (LEVEL 1-8)
        """
        file_path = self._get_filename('AS_ADDR_OBJ_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[[
                'NAME',
                'TYPENAME',
                'LEVEL'
                ]]

    def aggregate_houses(self):
        """
        Aggregates carplaces (LEVEL 10)
        """
        file_path = self._get_filename('AS_HOUSES_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[[
                'HOUSENUM',
                'HOUSETYPE',
                'ADDNUM1',
                'ADDTYPE1',
                'ADDNUM2',
                'ADDTYPE2'
                ]]

    def aggregate_carplaces(self):
        """
        Aggregates carplaces (LEVEL 17)
        """
        file_path = self._get_filename('AS_CARPLACES_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['NUMBER'].to_frame()

    def aggregate_rooms(self):
        """
        Aggregates rooms (LEVEL 12)
        """
        file_path = self._get_filename('AS_ROOMS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[['NUMBER', 'ROOMTYPE']]

    def aggregate_appartments(self):
        """
        Aggregates apartments (LEVEL 11)
        """
        file_path = self._get_filename('AS_APARTMENTS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[[
                'NUMBER',
                'APARTTYPE'
                ]]

    def aggregate_steads(self):
        """
        Aggregates carplaces (LEVEL 9)
        """
        file_path = self._get_filename('AS_STEADS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['NUMBER'].to_frame()
