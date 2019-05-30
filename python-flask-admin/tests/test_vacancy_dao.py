# Local application imports
import app
from app.data.dao import VacancyDao
from app.tests.ExtendedTestCase import (
    SANDBOX,
    ExtendedTestCase
)


def setUpModule():
    SANDBOX.start()

def tearDownModule():
    SANDBOX.stop()


class VacancyDaoTest(ExtendedTestCase):
    COLLECTION_NAME = 'vacancy'
    DAO = VacancyDao()
    ORGANIZATION_ID = '57c6e9fcc9e77c0012894079'

    def test_vacancies_count(self):
        with self.context:
            vacancies_count = self.DAO.get_vacancies_count((self.ORGANIZATION_ID,))
        self.assertIsInstance(vacancies_count, dict)
        self.assertEqual(vacancies_count[self.ORGANIZATION_ID]['OPEN'], 1)
        self.assertEqual(vacancies_count[self.ORGANIZATION_ID]['CLOSED'], 1)
        self.assertEqual(vacancies_count[self.ORGANIZATION_ID]['DRAFT'], 1)
        self.assertEqual(vacancies_count[self.ORGANIZATION_ID]['ARCHIVED'], 2)

    def test_vacancies_statistic(self):
        with self.context:
            vacancies = self.DAO.get_all_vacancies_count()
        self.assertEqual(vacancies, 4)
