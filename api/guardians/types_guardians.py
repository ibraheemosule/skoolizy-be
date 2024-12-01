from typing import TypedDict, Literal, Optional
from utils.constants import groups


class TGuardian(TypedDict):
    id: str
    tag: str
    created_at: str
    first_name: str
    middle_name: Optional[str]
    last_name: str
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    home_address: str
    phone_number: str
    email: str
    tier: Literal[1, 2, 3, 4, 5]
    group: Literal['guardians']
    verified: bool


class TGuardianPayload(TypedDict):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    email: str
    phone_number: str
    home_address: str
    group: Literal['guardians']
