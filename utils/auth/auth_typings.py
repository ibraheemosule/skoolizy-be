from typing import TypedDict


class TConfirmSignup(TypedDict):
    tag: str
    code: str


class TUserAuth(TypedDict):
    tag: str


class TRefreshTokenAuth(TypedDict):
    REFRESH_TOKEN: str
