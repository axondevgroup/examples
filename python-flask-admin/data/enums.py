from enum import Enum, auto


class VacancyStatus(Enum):
    OPEN = auto()
    CLOSED = auto()
    ARCHIVED = auto()
    DRAFT = auto()


class OrganizationActivationStatus(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    NOT_REGISTERED = auto()


class CandidateStatus(Enum):
    CANDIDATE = 'CAN'
    EMPLOYEE = 'EMP'


class SortOrder(Enum):
    ASC = 1
    DESC = -1
