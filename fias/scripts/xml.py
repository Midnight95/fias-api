from abc import ABC
import xml.etree.ElementTree as ET
import pandas as pd
import os


class XML(ABC):
    """
    path: str
        abspath to gar_xml/93/
    """

    def __init__(self, path: str):
        self._path = path

    def _parse_xml(self, filename) -> pd.DataFrame:
        """
        Make XML file into a pandas dataframe (df)
        filename: str
        """
        tree = ET.parse(os.path.join(self._path, filename))
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
            raise f'Looks like there is no {start} file in directory'
        return filename


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
                )['OBJECTID'].apply(list).reset_index(name='OBJECTID_list')

    def aggregate_objid_to_lvl(self):
        """
        aggregates objectid to levelid
           pd.Dataframe[objectid, levelid]
        """
        df = self._aggregate_reestr_obj()
        return df.set_index('OBJECTID')['LEVELID'].to_frame().reset_index()

    def aggregate_adm_hierarchy(self) -> dict:
        """
        aggregates administrative hierarchy
           pd.Dataframe[objectid, path: list[str]]
        """
        file_path = self._get_filename('AS_ADM_HIERARCHY')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['PATH'].apply(
                        lambda x: x.split('.')
                        ).to_frame().reset_index()

    def aggregate_mun_hierarchy(self) -> dict:
        """
        aggregates municipal hierarchy
           pd.Dataframe[objectid, path: list[str]]
        """
        file_path = self._get_filename('AS_MUN_HIERARCHY')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['PATH'].apply(
                        lambda x: x.split('.')
                        ).to_frame().reset_index()


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
                ]].reset_index()

    def aggregate_houses(self):
        """
        Aggregates carplaces (LEVEL 10)
        """
        file_path = self._get_filename('AS_HOUSES_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[[
                'HOUSENUM',
                'HOUSETYPE'
                'ADDNUM1',
                'ADDTYPE1',
                'ADDNUM2',
                'ADDTYPE2'
                ]].to_frame().reset_index()

    def aggregate_carplaces(self):
        """
        Aggregates carplaces (LEVEL 17)
        """
        file_path = self._get_filename('AS_CARPLACES_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['NUMBER'].reset_index()

    def aggregate_appartments(self):
        """
        Aggregates apartments (LEVEL 11)
        """
        file_path = self._get_filename('AS_APARTMENTS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')[[
                'NUMBER',
                'APARTTYPE'
                ]].reset_index()

    def aggregate_rooms(self):
        """
        Aggregates rooms (LEVEL 12)
        """
        file_path = self._get_filename('AS_ROOMS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['NUMBER'].reset_index()

    def aggregate_steads(self):
        """
        Aggregates carplaces (LEVEL 9)
        """
        file_path = self._get_filename('AS_STEADS_20')
        df = self._get_active(file_path)
        return df.set_index('OBJECTID')['NUMBER'].reset_index()


class TypeAggregator(XML):
    def __init__(self, path):
        super().__init__(path)
