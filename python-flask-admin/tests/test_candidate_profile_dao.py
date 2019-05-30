# Local application imports
from app.data.dao import CandidateProfileDao
from app.tests.ExtendedTestCase import (
    ExtendedTestCase,
    SANDBOX
)

def setUpModule():
    SANDBOX.start()

def tearDownModule():
    SANDBOX.stop()


class CandidateProfileDaoTest(ExtendedTestCase):
    COLLECTION_NAME = 'candidate_profile'
    DAO = CandidateProfileDao()
    ORGANIZATION_ID = ('57c6e9fcc9e77c0012894079',)

    def setUp(self):
        with self.context:
            self.candidates = self.DAO.get_candidates_count(self.ORGANIZATION_ID)

    def test_get_candidates_count(self):
        self.assertEqual(self.candidates[self.ORGANIZATION_ID[0]]['CANDIDATE'], 2)

    def test_get_employees_count(self):
        self.assertEqual(self.candidates[self.ORGANIZATION_ID[0]]['EMPLOYEE'], 1)

    def test_get_candidates_return_type(self):
        self.assertIsInstance(self.candidates, dict)

    def test_get_candidates_statistic(self):
        with self.context:
            candidates = self.DAO.get_all_candidates_count()
        self.assertEqual(candidates['candidates_count'], 3)
        self.assertEqual(candidates['hired_candidates_count'], 1)



