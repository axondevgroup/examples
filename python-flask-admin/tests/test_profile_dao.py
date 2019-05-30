# Local application imports
import config
from app.data.dao import ProfileDao
from app.tests.ExtendedTestCase import (
    SANDBOX,
    ExtendedTestCase
)

def setUpModule():
    SANDBOX.start()


def tearDownModule():
    SANDBOX.stop()


class ProfileDaoTest(ExtendedTestCase):
    COLLECTION_NAME = 'profile'
    DAO = ProfileDao()
    EMAILS = ('57bc6f4cc9e77c0012893ff2', '57bff725c9e77c001289404c')


    def test_get_email(self):
        with self.context:
            emails = self.DAO.get_emails(self.EMAILS)
        self.assertEqual(emails['57bc6f4cc9e77c0012893ff2'], 'test1@gmail.com')

    def test_get_emails(self):
        with self.context:
            emails = self.DAO.get_emails(self.EMAILS)
        self.assertEqual(emails['57bff725c9e77c001289404c'], 'test2@gmail.com')
        self.assertEqual(len(emails), 2)
        self.assertIsInstance(emails, dict)

    def test_get_active_users(self):
        with self.context:
            active_users = self.DAO.get_active_users()
        self.assertEqual(active_users, 3)
