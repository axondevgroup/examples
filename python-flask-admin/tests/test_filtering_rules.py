# Standard library imports
import unittest

# Local application imports
from app.data.dao import FILTERING_RULES


class FilteringRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registered = True
        cls.name = 'App'

    def test_registration_rule(self):
        registration_filter = FILTERING_RULES['registration_filter']['created_at']({'registered': False})
        self.assertIsNone(registration_filter)

    def test_registration_rule_unregistered(self):
        registration_filter = FILTERING_RULES['registration_filter']['created_at']({'registered': True})
        self.assertDictEqual(registration_filter, {'$ne': None})

    def test_name_filter(self):
        name_filter = FILTERING_RULES['name_filter']['name']({'name': 'Dima'})
        self.assertDictEqual(name_filter, {'$regex': 'Dima', '$options': 'i'})

