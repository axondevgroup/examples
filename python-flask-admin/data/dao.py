# Standard library imports
from typing import Dict, Tuple, List
from abc import ABC, abstractmethod

# Third party import
from bson.objectid import ObjectId
from pymongo.collection import Collection

# Local application imports
import app
from app.data.enums import SortOrder
from app.data.enums import (
    VacancyStatus,
    CandidateStatus,
    OrganizationActivationStatus
)
from app.data.models import (
    OrganizationDetails,
    Organization,
    SearchOptions
)

FILTERING_RULES = {
        'registration_filter': {'created_at': (lambda filter: {'$ne': None} if filter['registered'] else None)},
        'name_filter': {'name': (lambda filter: {'$regex': '%s' % filter['name'], '$options': 'i'})}
    }


class BaseDao(ABC):

    @property
    @abstractmethod
    def collection(self):
        raise NotImplementedError

    def get_collection(self) -> Collection:
        return app.mongo_db.get_db[self.collection]


class OrganizationDao(BaseDao):
    collection = 'organization'

    def get_count(self, search_options: SearchOptions) -> int:
        return self.get_collection().count_documents(filter=search_options.filters)

    def get_organizations(self, search_options: SearchOptions) -> Tuple[Organization]:
        sort = [(search_options.sort_field, SortOrder[search_options.sort_order].value)]
        organizations_cursor = self.get_collection().find(
            filter=search_options.filters,
            projection=Organization.__getattributes__(),
            sort=sort,
            limit=search_options.limit,
            skip=search_options.skip
        )
        return tuple(Organization(**organization) for organization in organizations_cursor)

    def get_organization(self, org_id: str) -> OrganizationDetails:
        match = {"$match": {'_id': ObjectId(org_id)}}

        project = {"$project": {'name': 1, 'created_at': 1, 'inactivated_at': 1,
                                'positions_count': {'$size': {"$ifNull": ["$positions", []]}},
                                'projects_count': {'$size': {"$ifNull": ["$projects", []]}}}}

        organization = self.get_collection().aggregate([match, project]).next()
        return OrganizationDetails(**organization)

    def get_organizations_statistic(self) -> Dict[str, int]:
        """Gets organizations statistics

           Makes query to MongoDB using facet: https://docs.mongodb.com/manual/reference/operator/aggregation/facet/

           Query Pipeline:
                {
                    NOT_REGISTERED: [
                        {"$match": {"created_at": null}},
                        {"$group": {'_id': null, NOT_REGISTERED: {"$sum": 1}}},
                        {"$project": {"_id": 0}}
                    ],
                    ACTIVE: [
                        {"$match": {"created_at": {"$ne": null}, "inactivated_at": null}},
                        {"$group": {'_id': null, ACTIVE: {"$sum": 1}}},
                        {"$project": {"_id": 0}}
                    ],
                    INACTIVE: [
                        {"$match": {"inactivated_at": {"$ne": null}, "created_at": {"$ne": null}}},
                        {"$group": {'_id': null, INACTIVE: {"$sum": 1}}},
                        {"$project": {"_id": 0}}
                    ],
                }

            Pipeline return:
                Document like -> {NOT_REGISTERED: [ {NOT_REGISTERED: <count: int>}, ],
                                  ACTIVE: [ {ACTIVE: <count: int>}, ],
                                  INACTIVE: [ {INACTIVE: <count: int>}, ]}

            :return: Dictionary  ->  {"ACTIVE": <count: int>, "INACTIVE": <count: int>, "NOT_REGISTERED": <count: int>}
        """
        facet = { "$facet": {
            OrganizationActivationStatus.NOT_REGISTERED.name: [
                       {"$match": {"created_at": None}},
                       {"$group": {'_id': None, OrganizationActivationStatus.NOT_REGISTERED.name: {"$sum": 1}}},
                       {"$project": {"_id": 0}}
            ],
            OrganizationActivationStatus.ACTIVE.name: [
                       {"$match": {"created_at": {"$ne": None}, "inactivated_at": None}},
                       {"$group": {'_id': None, OrganizationActivationStatus.ACTIVE.name: {"$sum": 1}}},
                       {"$project": {"_id": 0}}
            ],
            OrganizationActivationStatus.INACTIVE.name: [
                       {"$match": {"inactivated_at": {"$ne": None}, "created_at": {"$ne": None}}},
                       {"$group": {'_id': None, OrganizationActivationStatus.INACTIVE.name: {"$sum": 1}}},
                       {"$project": {"_id": 0}}
            ]
        }}

        organizations_count = self.get_collection().aggregate([facet]).next()
        active = organizations_count[OrganizationActivationStatus.ACTIVE.name].pop()
        inactive = organizations_count[OrganizationActivationStatus.INACTIVE.name].pop()
        not_registered = organizations_count[OrganizationActivationStatus.NOT_REGISTERED.name].pop()
        return dict(**active, **inactive, **not_registered)


class ProfileDao(BaseDao):
    collection = 'profile'
    projections = {"email": 1, "organization_id": 1}

    def get_emails(self, organizations_id: Tuple[ObjectId]) -> Dict[ObjectId, str]:
        filter = {"organization_id": {"$in": organizations_id},
                  "role": "COMPANY_ADMIN"}
        emails = self.get_collection().find(filter=filter,
                                            projection=self.projections)
        emails_dict = {email['organization_id']: email['email'] for email in emails}

        return emails_dict

    def get_team_members(self, org_id: str) -> List[Dict[str, int]]:
        match = {"$match": {"organization_id": ObjectId(org_id), "inactivated_at": None}}
        project = {"$project": {"role": 1}}
        group = {"$group": {"_id": "$role", "count": {"$sum": 1}}}

        team_members = list()
        for member in self.get_collection().aggregate([match, project, group]):
            team_members.append({member['_id']: member['count']})
        return team_members

    def get_active_users(self) -> int:
        filter = {'inactivated_at': None, 'removed_at': None}
        return self.get_collection().count_documents(filter=filter)


class CandidateProfileDao(BaseDao):
    collection = 'candidate_profile'

    def get_candidates_count(self, organizations_id: Tuple[ObjectId]) -> Dict[ObjectId, Dict[str, int]]:
        """Gets organizations candidates count

            Query Pipeline:
                [{$match: {
                    "organization_id": {"$in": [<organizations_id>]},
                    "draft_steps": null,
                    "removed_at": null}},
                 {$project: {"organization_id": 1,
                             "EMP": {"$cond": [ { $eq: [ "$status_code", "EMP" ] }, 1, 0 ]},
                             "CAN": {"$cond": [ { $eq: [ "$status_code", "CAN" ] }, 1, 0 ]},}},
                 {$group: {_id: "$organization_id", EMP: {"$sum": "$EMP"}, CAN: {"$sum": "$CAN"}}}]

            Pipeline return:
                Documents like -> {"_id": <organization_id>, "EMP": <count>, "CAN": <count>}

            :param organizations_id: List of organizations ID
            :return: Dictionary  ->  {<organization_oid>: {EMPLOYEE: <count>,
                                                           CANDIDATE: <count>}}
        """
        match = {"$match": {"organization_id": {"$in": organizations_id},
                            "draft_steps": None,
                            "removed_at": None}}

        project = {"$project": {"organization_id": 1,
                   CandidateStatus.CANDIDATE.name: {"$cond": [{
                       '$eq': ['$status_code', CandidateStatus.CANDIDATE.value]}, 1, 0]},
                   CandidateStatus.EMPLOYEE.name: {"$cond": [{
                       '$eq': ['$status_code', CandidateStatus.EMPLOYEE.value]}, 1, 0]}}}

        group = {"$group": {'_id': '$organization_id',
                            CandidateStatus.EMPLOYEE.name: {
                                '$sum': f'${CandidateStatus.EMPLOYEE.name}'},
                            CandidateStatus.CANDIDATE.name: {
                                '$sum': f'${CandidateStatus.CANDIDATE.name}'}}}

        candidates_count_dict = {id: {status.name: 0 for status in CandidateStatus} for id in organizations_id}
        for candidate in self.get_collection().aggregate([match, project, group]):
            candidates_count_dict[candidate['_id']] = candidate
        return candidates_count_dict

    def get_all_candidates_count(self) -> Dict[str, int]:
        match = {"$match": {'draft_steps': None}}

        project_before = {"$project": {CandidateStatus.EMPLOYEE.name: {'$cond': [{ '$and':
                                    [{'$eq': ['$status_code', 'EMP']},
                                    {'$ne': ['$removed_at', None]}]}, 1, 0 ]}}}

        group = {"$group": {'_id': None,
                            'hired_candidates_count': {'$sum': f'${CandidateStatus.EMPLOYEE.name}'},
                            "candidates_count": {'$sum': 1}}}
        project_after = {"$project": {"_id": 0}}

        candidates_count = self.get_collection().aggregate([match, project_before, group, project_after]).next()
        return candidates_count


class VacancyDao(BaseDao):
    collection = 'vacancy'

    def get_vacancies_count(self, organizations_id: Tuple[ObjectId]) -> Dict[ObjectId, Dict[str, int]]:
        """Gets organizations vacancies count

            Query Pipeline:
                [{$match: {"organization_id": {"$in": [<organizations_id>]},
                           "removed_at": null}},
                 {$project: {"organization_id": 1,
                            "OPEN": {"$cond": [ { $eq: [ "$status_code", "OPEN" ] }, 1, 0 ]},
                            "CLOSED": {"$cond": [ { $eq: [ "$status_code", "CLOSED" ] }, 1, 0 ]},}},
                            "ARCHIVED": {"$cond": [ { $eq: [ "$status_code", "ARCHIVED" ] }, 1, 0 ]},}},
                            "DRAFT": {"$cond": [ { $eq: [ "$status_code", "DRAFT" ] }, 1, 0 ]},}},
                 {$group: {_id: "$organization_id",
                           OPEN: {"$sum": "OPEN"},
                           CLOSED: {"$sum": "CLOSED"},
                           ARCHIVED: {"$sum": "ARCHIVED"},
                           DRAFT: {"$sum": "DRAFT"}}}]

            Pipeline return:
                Documents like -> {"_id": <organization_id>,
                                   "OPEN": <count>,
                                   "CLOSED": <count>,
                                   "ARCHIVED": <count>,
                                   "DRAFT": <count>}

            :param organizations_id: List of organizations ID
            :return: Dictionary  ->  {<organization_oid>: {OPEN: <count>,
                                                           CLOSED: <count>,
                                                           ARCHIVED: <count>,
                                                           DRAFT: <count>}}
                """
        match = {"$match": {"organization_id": {"$in": organizations_id}, "removed_at": None}}

        project = {"$project": {"organization_id": 1,
                   VacancyStatus.OPEN.name: {"$cond": [{
                       '$eq': ['$status_code', VacancyStatus.OPEN.name]}, 1, 0]},
                   VacancyStatus.CLOSED.name: {"$cond": [{
                       '$eq': ['$status_code', VacancyStatus.CLOSED.name]}, 1, 0]},
                   VacancyStatus.ARCHIVED.name: {"$cond": [{
                       '$eq': ['$status_code', VacancyStatus.ARCHIVED.name]}, 1, 0]},
                   VacancyStatus.DRAFT.name: {"$cond": [{
                       '$eq': ['$status_code', VacancyStatus.DRAFT.name]}, 1, 0]}}}

        group = {"$group": {'_id': '$organization_id',
                            VacancyStatus.OPEN.name: {
                                '$sum': f'${VacancyStatus.OPEN.name}'},
                            VacancyStatus.CLOSED.name: {
                                '$sum': f'${VacancyStatus.CLOSED.name}'},
                            VacancyStatus.ARCHIVED.name: {
                                '$sum': f'${VacancyStatus.ARCHIVED.name}'},
                            VacancyStatus.DRAFT.name: {
                                '$sum': f'${VacancyStatus.DRAFT.name}'}}}

        vacancies_count_dict = {id: {status.name: 0 for status in VacancyStatus} for id in organizations_id}
        for vacancy in self.get_collection().aggregate([match, project, group]):
            vacancies_count_dict[vacancy['_id']] = vacancy
        return vacancies_count_dict

    def get_all_vacancies_count(self):
        filter={'status_code': {'$ne': 'DRAFT'}}
        return self.get_collection().count_documents(filter=filter)

