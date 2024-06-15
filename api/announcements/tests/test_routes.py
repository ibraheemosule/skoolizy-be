import pytest
from db import db
from . import mock_data as mk
from api.announcements.models import Announcement


@pytest.mark.parametrize("url, data, expect", [
    mk.GET_ALL_RETURN_DATA,
    mk.GET_QUERY_BY_SEARCH_RETURN_DATA,
    mk.GET_QUERY_BY_SEARCH_RETURN_NO_DATA,
    mk.GET_QUERY_BY_RECIPIENT_RETURN_DATA,
    mk.GET_QUERY_BY_RECIPIENT_RETURN_NO_DATA,
    mk.GET_QUERY_BY_TYPE_RETURN_DATA,
    mk.GET_QUERY_BY_TYPE_RETURN_NO_DATA,
    mk.GET_QUERY_BY_START_DATE_RETURN_DATA
])
def test_get_data(client, url, data, expect):
    db.session.add(Announcement(**data))
    db.session.commit()

    response = client.get(url)
    res = response.json.get('data')

    if expect == 'no_data':
        assert res == [], 'invalid response received, expected []'
    else:
        assert len(res) == 1, "Invalid response expected"
        assert res[0].get('event_end_date') == str(mk.ANNOUNCEMENT_PAYLOAD['event_end_date']), 'announcement event_end_date mismatch' 
        assert res[0].get('event_start_date') == str(mk.ANNOUNCEMENT_PAYLOAD['event_start_date']), 'announcement event_start_date mismatch'
        assert res[0].get('event_time') == str(mk.ANNOUNCEMENT_PAYLOAD['event_time']), 'announcement event_time mismatch'
        assert res[0].get('title') == mk.ANNOUNCEMENT_PAYLOAD['title'], 'announcement title mismatch'
        assert res[0].get('message') == mk.ANNOUNCEMENT_PAYLOAD['message'], 'announcement message mismatch'
        assert res[0].get('type') == mk.ANNOUNCEMENT_PAYLOAD['type'], 'announcement type mismatch'


@pytest.mark.parametrize("data, expected_status, expected_message", [
    mk.POST_NO_TYPE_IN_PAYLOAD_403,
    mk.POST_INVALID_TYPE_IN_PAYLOAD_403,
    mk.POST_MULTI_EVENT_WITH_VALID_PAYLOAD_201,
    mk.POST_MULTI_EVENT_EVENT_TIME_IN_PAYLOAD_403,
    mk.POST_MULTI_EVENT_NO_MESSAGE_IN_PAYLOAD_201,
    mk.POST_MULTI_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403,
    mk.POST_MULTI_EVENT_NO_EVENT_END_DATE_IN_PAYLOAD_403,
    mk.POST_MULTI_EVENT_NO_TITLE_IN_PAYLOAD_403,
    mk.POST_SINGLE_EVENT_WITH_VALID_PAYLOAD_201,
    mk.POST_SINGLE_EVENT_EVENT_END_DATE_IN_PAYLOAD_403,
    mk.POST_SINGLE_EVENT_NO_MESSAGE_IN_PAYLOAD_201,
    mk.POST_SINGLE_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403,
    mk.POST_SINGLE_EVENT_NO_EVENT_TIME_IN_PAYLOAD_403,
    mk.POST_SINGLE_EVENT_NO_TITLE_IN_PAYLOAD_403,
    mk.POST_MEMO_WITH_VALID_PAYLOAD_201,
    mk.POST_MEMO_EVENT_END_DATE_IN_PAYLOAD_403,
    mk.POST_MEMO_EVENT_START_DATE_IN_PAYLOAD_403
])
def test_post_data(client, data, expected_status, expected_message):
    res = client.post('/announcements', json=data)
    assert res.status_code == expected_status
    assert res.json == expected_message