# Standard library imports
import unittest

# Local application imports
from app.data.models import OrganizationsStatistic
from app.data.serializers import organization_statistic_serializer


class StatisticSerializerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.statistic = OrganizationsStatistic(
            active_organizations_count=10,
            inactive_organizations_count=20,
            not_registered_organizations_count=30,
            active_users_count=40,
            vacancies_count=50,
            candidates_count=60,
            hired_candidates_count=70)
        cls.serialized = organization_statistic_serializer(cls.statistic)

    def test_return_object(self):
        self.assertIsInstance(self.serialized, dict)

    def test_value_valid(self):
        self.assertEqual(self.serialized['active_organizations_count'], 10)
        self.assertEqual(self.serialized['active_users_count'], 40)
        self.assertEqual(self.serialized['candidates_count'], 60)
        self.assertEqual(self.serialized['inactive_organizations_count'], 20)
        self.assertEqual(self.serialized['vacancies_count'], 50)
        self.assertEqual(self.serialized['hired_candidates_count'], 70)
        self.assertEqual(self.serialized['not_registered_organizations_count'], 30)