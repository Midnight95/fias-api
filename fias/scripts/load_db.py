from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import pymongo
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
GAR_XML_DIR = os.getenv('GAR_XML_DIR')

clinet = pymongo.MongoClient(DATABASE_URL)
db = clinet['fias_db']


def walk_root(dir):
    for region in os.scandir(dir):
        if region.is_dir():

