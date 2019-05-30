# Standard library imports
from typing import List
from collections import OrderedDict

# Local application imports
from app.data.enums import OrganizationActivationStatus
from app.data.dao import FILTERING_RULES
from app.data.models import (
    OrganizationResponse,
    OrganizationDetailsResponse,
    OrganizationsStatistic,
    Filters
)


def organization_serializer(organization: OrganizationResponse):
    serialized_object = {'_id': str(organization._id),
                         'name': organization.name,
                         'created_at': organization.created_at,
                         'email': organization.email,
                         'candidates_count': organization.candidates_count,
                         'employees_count': organization.employees_count,
                         'open_vacancies_count': organization.open_vacancies_count,
                         'inactive_vacancies_count': organization.inactive_vacancies_count}
    if organization.created_at is None:
        serialized_object['activation_status'] = OrganizationActivationStatus.NOT_REGISTERED.name
    elif organization.inactivated_at is None:
        serialized_object['activation_status'] = OrganizationActivationStatus.ACTIVE.name
    else:
        serialized_object['activation_status'] = OrganizationActivationStatus.INACTIVE.name

    return serialized_object


def organization_details_serializer(organization: OrganizationDetailsResponse):
    serialized_object = organization_serializer(organization)
    serialized_object['projects_count'] = organization.projects_count
    serialized_object['positions_count'] = organization.positions_count
    serialized_object['members_count'] = organization.members_count

    return serialized_object

def organization_statistic_serializer(statistic: OrganizationsStatistic):
    serialized_object = dict(
        active_organizations_count=statistic.active_organizations_count,
        inactive_organizations_count=statistic.inactive_organizations_count,
        not_registered_organizations_count=statistic.not_registered_organizations_count,
        active_users_count=statistic.active_users_count,
        vacancies_count=statistic.vacancies_count,
        candidates_count=statistic.candidates_count,
        hired_candidates_count=statistic.hired_candidates_count,
    )
    return serialized_object


def organizations_list_serializer(organizations: List[OrganizationResponse]):
    return list(map(organization_serializer, organizations))


def filters_serializer(filters: List[Filters]):
    serialized_filters = dict()
    for filter in filters:
        key = list(FILTERING_RULES[filter['filter_type']]).pop()
        value = list(FILTERING_RULES[filter['filter_type']].values()).pop()(filter)
        serialized_filters[key] = value
    return serialized_filters

