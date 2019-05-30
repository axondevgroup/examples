# Standard library imports
import unittest

# Third party import
from bson import json_util
from mongobox import MongoBox, utils

# Local application imports
import app
import config

DB_PORT = utils.get_free_port()
SANDBOX = MongoBox(port=DB_PORT)
DB = SANDBOX.client()[config.TestingConfig.DB_NAME]


class ExtendedTestCase(unittest.TestCase):
    DB = DB
    DB_PORT = DB_PORT

    @classmethod
    def setUpClass(cls):
        cls.collection = cls.DB[cls.COLLECTION_NAME]
        with open(f'./datasets/{cls.COLLECTION_NAME}.json') as file:
            data = json_util.loads(file.read())
            cls.collection.insert_many(data)
        cls.app = app.create_app((), testing=True)
        cls.app.config['DB_PORT'] = cls.DB_PORT
        cls.context = cls.app.app_context()

    @classmethod
    def tearDownClass(cls):
        cls.DB.drop_collection(cls.COLLECTION_NAME)