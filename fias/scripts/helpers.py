from fias.scripts.xml import XML
from random import randint
import os


class XMLHelper(XML):
    def __init__(self, path):
        super().__init__(path)

    def set_filename(self, filename):
        self._filename = filename
        self._abspath = self._get_filename(filename)
        self._df = self._parse_xml(self._abspath)

    def get_filename(self):
        return self._filename

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def show_xml_schema(self):
        return self._df.info()

    def show_random_object(self):
        return self._df.iloc[randint(0, self._df.shape[0])]

    def find_object_by_id(self):
        return self._df.query(f'OBJECTID == "{self._id}"')

    def find_level(self):
        filename = self._get_filename('AS_REESTR_OBJECTS')
        return self._parse_xml(self._get_filename(filename)).query(
                f'OBJECTID == "{self._id}"'
                )['LEVELID']

    def find_file(self):
        filenames = os.listdir(self._path)
        for file in filenames:
            df = self._parse_xml(self._get_filename(file))
            if df.get('OBJECTID') is None:
                continue
            obj = df.query(f'OBJECTID == "{self._id}"')
            if obj:
                return obj
