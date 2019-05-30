# Standard library imports
from typing import Generator

# Local application imports
from app.data import dao
from app.data.models import (
    OrganizationResponse,
    OrganizationDetailsResponse,
    SearchOptions,
    OrganizationsStatistic
)
from app.data.enums import (
    VacancyStatus,
    CandidateStatus,
    OrganizationActivationStatus
)

profile_dao = dao.ProfileDao()
candidate_dao = dao.CandidateProfileDao()
vacancy_dao = dao.VacancyDao()
org_dao = dao.OrganizationDao()


def get_organizations(
        search_options: SearchOptions
    ) -> Generator[OrganizationResponse, None, None]:

    organizations = org_dao.get_organizations(search_options)
    organizations_dict = {organization._id: organization for organization in organizations}
    organizations_id_list = tuple(organizations_dict.keys())
    emails_dict = profile_dao.get_emails(organizations_id_list)
    candidates_count = candidate_dao.get_candidates_count(organizations_id_list)
    vacancies_count = vacancy_dao.get_vacancies_count(organizations_id_list)
    for id in organizations_dict:
        email = emails_dict.get(id, '')
        vacancies = vacancies_count.get(id)
        candidates = candidates_count.get(id)
        organization = OrganizationResponse(
            email=email,
            candidates_count=candidates[CandidateStatus.CANDIDATE.name],
            employees_count=candidates[CandidateStatus.EMPLOYEE.name],
            open_vacancies_count=vacancies[VacancyStatus.OPEN.name],
            inactive_vacancies_count=(vacancies[VacancyStatus.ARCHIVED.name]
                                      + vacancies[VacancyStatus.CLOSED.name]),
            **organizations_dict[id]
        )
        yield organization


def get_organizations_count(search_options: SearchOptions) -> int:
    return org_dao.get_count(search_options)


def get_organization(organization_id: str) -> OrganizationDetailsResponse:
    organization = org_dao.get_organization(organization_id)
    email = profile_dao.get_emails((organization._id,))
    vacancies_count = vacancy_dao.get_vacancies_count((organization._id,))
    candidates_count = candidate_dao.get_candidates_count((organization._id,))
    members = profile_dao.get_team_members(organization._id)
    organization_api_model = OrganizationDetailsResponse(
        email=email.get(organization._id, ''),
        candidates_count=candidates_count[organization._id][CandidateStatus.CANDIDATE.name],
        employees_count=candidates_count[organization._id][CandidateStatus.EMPLOYEE.name],
        open_vacancies_count=vacancies_count[organization._id][VacancyStatus.OPEN.name],
        inactive_vacancies_count=(vacancies_count[organization._id][VacancyStatus.ARCHIVED.name]
                                  + vacancies_count[organization._id][VacancyStatus.CLOSED.name]),
        members_count=members,
        **organization
    )
    return organization_api_model

def get_organizations_statistic():
    active_users_count = profile_dao.get_active_users()
    vacancies_count = vacancy_dao.get_all_vacancies_count()
    candidates_count = candidate_dao.get_all_candidates_count()
    organizations_count = org_dao.get_organizations_statistic()
    statistic = OrganizationsStatistic(
        active_organizations_count=organizations_count[OrganizationActivationStatus.ACTIVE.name],
        inactive_organizations_count=organizations_count[OrganizationActivationStatus.INACTIVE.name],
        not_registered_organizations_count=organizations_count[OrganizationActivationStatus.NOT_REGISTERED.name],
        active_users_count=active_users_count,
        vacancies_count=vacancies_count,
        **candidates_count
    )
    return statistic



