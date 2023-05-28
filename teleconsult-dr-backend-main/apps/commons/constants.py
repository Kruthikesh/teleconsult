from enum import Enum

from apps.commons.utils import BaseStatusClass


class UserTypes(Enum):
    DOCTOR = 'DOCTOR'
    PATIENT = 'PATIENT'


VALID_USER_TYPES = [
    UserTypes.DOCTOR.value,
    UserTypes.PATIENT.value
]


class Specialisations(BaseStatusClass):
    ORTHOPAEDIC = 'ORTHOPAEDIC'


class TCDState(BaseStatusClass):
    DOCTOR_SUGGESTION_SUBMITTED = 'DOCTOR_SUGGESTION_SUBMITTED'
    PATIENT_INPUT_SUBMITTED = 'PATIENT_INPUT_SUBMITTED'
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
