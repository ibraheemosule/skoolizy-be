from datetime import datetime, timedelta


__success_response = {"message": "Announcement has been sent"}
__yesterday = str(datetime.today().date() + timedelta(days=-1))
__tomorrow = str(datetime.today().date() + timedelta(days=1))
__overmorrow = str(datetime.today().date() + timedelta(days=2))
__three_days_from_today = str(datetime.today().date() + timedelta(days=3))

__title = "testing to ensure this implementation works"
__message = "test message to ensure this implementation works fine as well"

ANNOUNCEMENT_PAYLOAD = {
    "title": __title,
    "event_time": "05:00:00",
    "event_start_date": __tomorrow,
    "event_end_date": __overmorrow,
    "type": "multi_event",
    "reminder": None,
    "message": __message,
}
__MULTI_EVENT_PAYLOAD = {k: v for k, v in ANNOUNCEMENT_PAYLOAD.items() if k != "event_time"}
__SINGLE_EVENT_PAYLOAD = {
    k: v if v != "multi_event" else "single_event" for k, v in ANNOUNCEMENT_PAYLOAD.items() if k != "event_end_date"
}
__MEMO_PAYLOAD = {
    k: v if v != "multi_event" else "memo"
    for k, v in ANNOUNCEMENT_PAYLOAD.items()
    if k not in ["event_end_date", "event_time", "event_start_date", "reminder"]
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
    {"error": "type should be one of (memo, single_event, multi_event)"},
)

POST_INVALID_TYPE_IN_PAYLOAD_403 = (
    {**__MULTI_EVENT_PAYLOAD, "type": "invalid_type"},
    403,
    {"error": "type should be one of (memo, single_event, multi_event)"},
)

POST_INVALID_RECIPIENT_IN_PAYLOAD_403 = (
    {**__MULTI_EVENT_PAYLOAD, "recipient": "invalid_type"},
    403,
    {'error': 'recipient should be one of (all, parents, teachers, students)'},
)

POST_MULTI_EVENT_WITH_VALID_PAYLOAD_201 = (
    __MULTI_EVENT_PAYLOAD,
    201,
    __success_response,
)

POST_MULTI_EVENT_EVENT_TIME_IN_PAYLOAD_403 = (
    ANNOUNCEMENT_PAYLOAD.copy(),
    403,
    {"error": "event_time is an invalid payload for multi_event announcement type"},
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
    {"error": "event_end_date is an invalid payload for single_event announcement type"},
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
    {"error": "event_end_date is an invalid payload for memo announcement type"},
)

POST_MEMO_EVENT_START_DATE_IN_PAYLOAD_403 = (
    {**__MEMO_PAYLOAD, "event_start_date": "2020-05-23"},
    403,
    {"error": "event_start_date is an invalid payload for memo announcement type"},
)

POST_MEMO_EVENT_TIME_IN_PAYLOAD_403 = (
    {**__MEMO_PAYLOAD, "event_time": "05:00:00"},
    403,
    {"error": "event_time is an invalid payload for memo announcement type"},
)

DELETE_SINGLE_EVENT_200 = (__SINGLE_EVENT_PAYLOAD, 200, {"message": "Announcement with id-1 has been deleted"})

DELETE_PAST_SINGLE_EVENT_403 = (
    {**__SINGLE_EVENT_PAYLOAD, 'event_start_date': str(datetime.today().date())},
    403,
    {'error': "Can't delete today's event or past event announcement"},
)

DELETE_MULTI_EVENT_200 = (__MULTI_EVENT_PAYLOAD, 200, {"message": "Announcement with id-1 has been deleted"})

DELETE_MEMO_403 = (__MEMO_PAYLOAD, 403, {"error": "Cannot delete announcement with id-1 because it is a memo"})


UPDATE_MULTI_EVENT_VALID_DATA_200 = (
    __MULTI_EVENT_PAYLOAD,
    {
        'message': 'update a new message here to test',
        'event_start_date': __overmorrow,
        'event_end_date': __three_days_from_today,
        'title': 'here is owkring',
    },
    200,
    {'message': 'Announcement with id-1 has been updated'},
)

UPDATE_MULTI_EVENT_END_DATE_EARLIER_THAN_EVENT_START_DATE_DATA_403 = (
    __MULTI_EVENT_PAYLOAD,
    {'event_start_date': __three_days_from_today},
    403,
    {'error': 'event_start_date should be an earlier date than event_end_date'},
)

UPDATE_SINGLE_EVENT_VALID_DATA_200 = (
    __SINGLE_EVENT_PAYLOAD,
    {
        'message': 'update thhis is the way you want to work here',
        'event_start_date': __three_days_from_today,
        'title': 'here is owkring',
    },
    200,
    {'message': 'Announcement with id-1 has been updated'},
)

UPDATE_SINGLE_EVENT_WITH_PAST_DATE_403 = (
    __MULTI_EVENT_PAYLOAD,
    {'event_start_date': __yesterday},
    403,
    {'error': 'event_start_date should be a future date'},
)
