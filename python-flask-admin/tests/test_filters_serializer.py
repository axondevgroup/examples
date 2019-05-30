# Standard library imports
import unittest

# Local application imports
from app.data.serializers import filters_serializer


class OrganizationSerializerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registered = {'filter_type': 'registration_filter', 'registered': True}
        cls.unregistered = {'filter_type': 'registration_filter', 'registered': False}
        cls.name_filter = {'filter_type': 'name_filter', 'name': 'Echo'}

    def test_registration_filter_registered(self):
        serialized_registration_filter = filters_serializer((self.registered,))
        self.assertDictEqual({'created_at': {'$ne': None}}, serialized_registration_filter)

    def test_registration_filter_unregistered(self):
        serialized_registration_filter = filters_serializer((self.unregistered,))
        self.assertDictEqual({'created_at': None}, serialized_registration_filter)

    def test_name_filter(self):
        serialized_name_filter = filters_serializer((self.name_filter,))
        self.assertDictEqual({'name': {'$options': 'i', '$regex': 'Echo'}}, serialized_name_filter)

    def test_many_filters(self):
        serialized_filters = filters_serializer((self.name_filter, self.unregistered))
        self.assertDictEqual({'name': {'$options': 'i', '$regex': 'Echo'}, 'created_at': None}, serialized_filters)