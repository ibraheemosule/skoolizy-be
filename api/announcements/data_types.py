from typing import TypedDict, Literal, Optional


class TAnnouncement(TypedDict):
    id: int
    recipient: Literal["all", "parents", "teachers", "students"]
    date_created: str
    title: str
    type: Literal["memo", "single_event", "multi_event"]
    message: str
    event_start_date: Optional[str]
    event_end_date: Optional[str]
    event_time: Optional[str]


class TAnnouncementPayload(TypedDict):
    title: str
    type: Literal["memo", "single_event", "multi_event"]
    message: str
    event_start_date: Optional[str]
    event_end_date: Optional[str]
    event_time: Optional[str]
    reminder: Optional[Literal[1, 2, 3, 4, 5, 6, 7]]
