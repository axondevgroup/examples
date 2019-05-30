# Standard libary imports
from typing import Dict, List
from dataclasses import dataclass


# Third party import
from datetime import datetime
from bson import objectid

# Local  application imports
from app.data.enums import SortOrder


@dataclass
class OrganizationResponse:
    _id: objectid
    email: str
    name: str = None
    created_at: datetime = None
    inactivated_at: datetime = None
    candidates_count: int = 0
    employees_count: int = 0
    open_vacancies_count: int = 0
    inactive_vacancies_count: int = 0


@dataclass
class OrganizationDetailsResponse(OrganizationResponse):
    members_count: List[Dict[str, int]] = None
    projects_count: int = 0
    positions_count: int = 0


@dataclass
class Organization:
    _id: objectid
    created_at: datetime = None
    name: str = None
    inactivated_at: datetime = None

    @staticmethod
    def __getattributes__():
        return ['_id', 'created_at', 'name', 'inactivated_at']

    def keys(self):
        return self.__getattributes__()

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass
class OrganizationDetails(Organization):
    projects_count: int = 0
    positions_count: int = 0

    @staticmethod
    def __getattributes__():
        return ['projects_count', 'positions_count'] + Organization.__getattributes__()


class Filters():
    registration_filter: Dict[str, bool] = {'registered': bool}
    name_filter: Dict[str, str] = {'name': str}


@dataclass
class SearchOptions():
    limit: int = 0
    skip: int = 0
    sort_field:  str = ''
    sort_order: SortOrder = SortOrder.ASC.value
    filters: Filters = None

@dataclass
class OrganizationsStatistic():
    active_organizations_count: int = 0
    inactive_organizations_count: int = 0
    not_registered_organizations_count: int = 0
    active_users_count: int = 0
    vacancies_count: int = 0
    candidates_count: int = 0
    hired_candidates_count: int = 0