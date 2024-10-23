from typing import TypedDict, Literal, Optional


class TTeacher(TypedDict):
    id: str
    date_created: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    email: str
    tier: Literal[1, 2, 3, 4, 5]
    role: Literal['staff']


class TTeacherPayload(TypedDict):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    email: str


class TConfirmSignup(TypedDict):
    email: str
    otp: str
