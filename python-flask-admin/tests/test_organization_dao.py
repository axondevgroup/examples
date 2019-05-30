# Local application imports
from app.data.dao import OrganizationDao
from app.data.models import (
    SearchOptions,
    OrganizationDetails,
    Organization
)
from app.tests.ExtendedTestCase import (
    SANDBOX,
    ExtendedTestCase
)

def setUpModule():
    SANDBOX.start()

def tearDownModule():
    SANDBOX.stop()


class OrganizationDaoTest(ExtendedTestCase):
    COLLECTION_NAME = 'organization'
    DAO = OrganizationDao()

    def setUp(self):
        self.search_options = SearchOptions()
        self.search_options.sort_order = 'DESC'
        self.search_options.sort_field = 'created_at'

    def test_count_filter_empty(self):
        self.search_options.filters={}
        with self.context:
            count = self.DAO.get_count(self.search_options)
        self.assertEqual(count, 4)

    def test_count_filter_include(self):
        self.search_options.filters={'name': 'App'}
        with self.context:
            count = self.DAO.get_count(self.search_options)
        self.assertEqual(count, 1)

    def test_get_organization(self):
        organization_name = 'Dmitry Inc'
        organization_id = str(self.collection.find({'name': organization_name}).next()['_id'])
        with self.context:
            organization = self.DAO.get_organization(organization_id)
        self.assertIsInstance(organization, OrganizationDetails, 'Unexpected return type')
        self.assertEqual(organization.name, organization_name, 'Unexpected organization name')
        self.assertEqual(organization.positions_count, 1, 'Unexpected positions count')
        self.assertIsNone(organization.inactivated_at, 'Unexpected ativation status')

    def test_get_organizations(self):
        self.search_options.sort_field = 'name'
        self.search_options.sort_order = 'DESC'
        with self.context:
            organizations = self.DAO.get_organizations(self.search_options)
            organization = organizations[0]
        self.assertIsInstance(organization, Organization, 'Unexpected instance type')
        self.assertIsInstance(organizations, tuple, 'Unexpected return type')
        self.assertEqual(len(organizations), 4, 'Unexpected organization list length')

    def test_get_orgnizations_limit(self):
        self.search_options.limit = 2
        with self.context:
            organizations = self.DAO.get_organizations(self.search_options)
        self.assertEqual(len(organizations), 2, 'Unexpected organization list length')

    def test_get_organizations_skip(self):
        self.search_options.skip = 2
        with self.context:
            organizations = self.DAO.get_organizations(self.search_options)
        self.assertEqual(organizations[0].name, 'Dmitry Inc')

    def test_get_organizations_sort(self):
        self.search_options.sort_field = 'name'
        self.search_options.sort_order = 'DESC'
        with self.context:
            organizations = self.DAO.get_organizations(self.search_options)
        self.assertEqual(organizations[0].name, 'Dmitry Inc')

    def test_get_organizations_filter_registered(self):
        self.search_options.filters = {'created_at': None}
        with self.context:
            organizations = self.DAO.get_organizations(self.search_options)
        self.assertEqual(len(organizations), 1)
        self.assertEqual(organizations[0].name, 'Another')

    def test_get_organizations_statistic(self):
        with self.context:
            statistic = self.DAO.get_organizations_statistic()
        self.assertEqual(statistic['ACTIVE'], 2)
        self.assertEqual(statistic['INACTIVE'], 1)
        self.assertEqual(statistic['NOT_REGISTERED'], 1)

    def tearDown(self):
        del self.search_options
