from datetime import datetime, timedelta


__success_response = {"message": "Data inserted successfully"}
__yesterday = str(datetime.today().date() + timedelta(days=-1))
__tomorrow = str(datetime.today().date() + timedelta(days=1))
__overmorrow = str(datetime.today().date() + timedelta(days=2))

ANNOUNCEMENT_PAYLOAD = {
    "title": "testing",
    "event_time": "05:00:00",
    "event_start_date": __tomorrow,
    "event_end_date": __overmorrow,
    "type": "multi_event",
    "message": "here is another working",
}
__MULTI_EVENT_PAYLOAD = {k: v for k, v in ANNOUNCEMENT_PAYLOAD.items() if k != "event_time"}
__SINGLE_EVENT_PAYLOAD = {
    k: v if v != "multi_event" else "single_event" for k, v in ANNOUNCEMENT_PAYLOAD.items() if k != "event_end_date"
}
__MEMO_PAYLOAD = {
    k: v if v != "multi_event" else "memo"
    for k, v in ANNOUNCEMENT_PAYLOAD.items()
    if k not in ["event_end_date", "event_time", "event_start_date"]
}


# GET REQUEST TESTS
GET_ALL_RETURN_DATA = ("/announcements", ANNOUNCEMENT_PAYLOAD, "data")
GET_QUERY_BY_SEARCH_RETURN_DATA = (
    "/announcements?search=testing",
    ANNOUNCEMENT_PAYLOAD,
    "data",
)
GET_QUERY_BY_SEARCH_RETURN_NO_DATA = (
    "/announcements?search=notvalid",
    ANNOUNCEMENT_PAYLOAD,
    "no_data",
)
GET_QUERY_BY_RECIPIENT_RETURN_DATA = (
    "/announcements?recipient=teachers",
    {**ANNOUNCEMENT_PAYLOAD, "recipient": "teachers"},
    "data",
)
GET_QUERY_BY_RECIPIENT_RETURN_NO_DATA = (
    "/announcements?recipient=teachers",
    ANNOUNCEMENT_PAYLOAD,
    "no_data",
)
GET_QUERY_BY_TYPE_RETURN_DATA = (
    "/announcements?type=multi_event",
    ANNOUNCEMENT_PAYLOAD,
    "data",
)
GET_QUERY_BY_TYPE_RETURN_NO_DATA = (
    "/announcements?type=multi_event",
    {**__SINGLE_EVENT_PAYLOAD},
    "no_data",
)
GET_QUERY_BY_START_DATE_RETURN_DATA = (
    f"/announcements?from_date={__yesterday}",
    ANNOUNCEMENT_PAYLOAD,
    "data",
)

# POST REQUEST TESTS
POST_NO_TYPE_IN_PAYLOAD_403 = (
    {k: v for k, v in __MULTI_EVENT_PAYLOAD.items() if k not in ["type"]},
    403,
    {"error": "type should be one of (all, parents, teachers, students)"},
)

POST_INVALID_TYPE_IN_PAYLOAD_403 = (
    {**__MULTI_EVENT_PAYLOAD, "type": "invalid_type"},
    403,
    {"error": "type should be one of (all, parents, teachers, students)"},
)

POST_MULTI_EVENT_WITH_VALID_PAYLOAD_201 = (
    __MULTI_EVENT_PAYLOAD,
    201,
    __success_response,
)

POST_MULTI_EVENT_EVENT_TIME_IN_PAYLOAD_403 = (
    ANNOUNCEMENT_PAYLOAD.copy(),
    403,
    {"error": "event_time is an invalid payload"},
)

POST_MULTI_EVENT_NO_MESSAGE_IN_PAYLOAD_201 = (
    {k: v for k, v in __MULTI_EVENT_PAYLOAD.items() if k not in ["message"]},
    201,
    __success_response,
)

POST_MULTI_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403 = (
    {k: v for k, v in __MULTI_EVENT_PAYLOAD.items() if k not in ["event_start_date"]},
    403,
    {"error": "event_start_date is required"},
)

POST_MULTI_EVENT_NO_EVENT_END_DATE_IN_PAYLOAD_403 = (
    {k: v for k, v in __MULTI_EVENT_PAYLOAD.items() if k not in ["event_end_date"]},
    403,
    {"error": "event_end_date is required, event_start_date should be an earlier date than event_end_date"},
)

POST_MULTI_EVENT_NO_TITLE_IN_PAYLOAD_403 = (
    {k: v for k, v in __MULTI_EVENT_PAYLOAD.items() if k not in ["title"]},
    403,
    {"error": "title is required"},
)


POST_SINGLE_EVENT_WITH_VALID_PAYLOAD_201 = (
    __SINGLE_EVENT_PAYLOAD,
    201,
    __success_response,
)

POST_SINGLE_EVENT_EVENT_END_DATE_IN_PAYLOAD_403 = (
    {**ANNOUNCEMENT_PAYLOAD, "type": "single_event"},
    403,
    {"error": "event_end_date is an invalid payload"},
)

POST_SINGLE_EVENT_NO_MESSAGE_IN_PAYLOAD_201 = (
    {k: v for k, v in __SINGLE_EVENT_PAYLOAD.items() if k not in ["message", "event_end_date"]},
    201,
    __success_response,
)

POST_SINGLE_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403 = (
    {k: v for k, v in __SINGLE_EVENT_PAYLOAD.items() if k not in ["event_start_date", "event_end_date"]},
    403,
    {"error": "event_start_date is required"},
)

POST_SINGLE_EVENT_NO_EVENT_TIME_IN_PAYLOAD_403 = (
    {k: v for k, v in __SINGLE_EVENT_PAYLOAD.items() if k not in ["event_end_date", "event_time"]},
    403,
    {"error": "event_time is required"},
)

POST_SINGLE_EVENT_NO_TITLE_IN_PAYLOAD_403 = (
    {k: v for k, v in __SINGLE_EVENT_PAYLOAD.items() if k not in ["event_end_date", "title"]},
    403,
    {"error": "title is required"},
)

POST_MEMO_WITH_VALID_PAYLOAD_201 = (__MEMO_PAYLOAD, 201, __success_response)

POST_MEMO_EVENT_END_DATE_IN_PAYLOAD_403 = (
    {**__MEMO_PAYLOAD, "event_end_date": "2020-05-23"},
    403,
    {"error": "event_end_date is an invalid payload"},
)

POST_MEMO_EVENT_START_DATE_IN_PAYLOAD_403 = (
    {**__MEMO_PAYLOAD, "event_start_date": "2020-05-23"},
    403,
    {"error": "event_start_date is an invalid payload"},
)

POST_MEMO_EVENT_TIME_IN_PAYLOAD_403 = (
    {**__MEMO_PAYLOAD, "event_time": "05:00:00"},
    403,
    {"error": "event_time is an invalid payload"},
)
