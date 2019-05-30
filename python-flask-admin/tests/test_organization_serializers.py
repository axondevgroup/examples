# Standard library imports
import unittest

# Third party import
from bson import ObjectId
from datetime import datetime

# Local application imports
from app.data.models import OrganizationDetailsResponse
from app.data.serializers import organization_serializer


class OrganizationSerializerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.organization = OrganizationDetailsResponse(**{'name': 'test',
                                                          '_id': ObjectId(),
                                                          'created_at': datetime.now(),
                                                          'email': 'test@test.com',
                                                          'inactivated_at': None})
        cls.serialized = organization_serializer(cls.organization)

    def test_return_object(self):
        self.assertIsInstance(self.serialized, dict)

    def test_data_exist(self):
        self.assertIn('name', self.serialized)
        self.assertIn('_id', self.serialized)
        self.assertIn('email', self.serialized)
        self.assertIn('created_at', self.serialized)
        self.assertIn('activation_status', self.serialized)

    def test_data_objects(self):
        self.assertIsInstance(self.serialized['name'], str)
        self.assertIsInstance(self.serialized['_id'], str)
        self.assertIsInstance(self.serialized['email'], str)
        self.assertIsInstance(self.serialized['created_at'], datetime)
        self.assertIsInstance(self.serialized['activation_status'], str)

    def test_data_valid(self):
        self.assertEqual(self.serialized['activation_status'], 'ACTIVE')
