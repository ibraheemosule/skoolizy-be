from typing import TypedDict, Literal, Optional


class TTeacher(TypedDict):
    user_id: str
    date_created: str
    first_name: str
    last_name: str
    other_name: Optional[str]
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    email: str


class TTeacherPayload(TypedDict):
    first_name: str
    last_name: str
    other_name: Optional[str]
    gender: Literal['male', 'female']
    date_of_birth: str
    country: str
    state_of_origin: str
    email: str
