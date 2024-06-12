from flask import json
from unittest.mock import MagicMock, patch
from app import app as flask_app
from db import db
from . import mock_data as mk
from api.announcements.models import Announcement

def test_get_data(client):
    db.session.add(Announcement(**mk.ANNOUNCEMENT_PAYLOAD))
    db.session.commit()

    response = client.get('/announcements')
    res = response.json
    assert len(res) == 1, "Invalid response expected"
    print(json.dumps(res[0], sort_keys=True,indent=4), '------------------')
    print(json.dumps(mk.ANNOUNCEMENT_PAYLOAD, sort_keys=True, indent=4))
    assert json.dumps(res[0], sort_keys=True) == json.dumps(mk.ANNOUNCEMENT_PAYLOAD, sort_keys=True), "Mismatch in payload"

# @pytest.mark.parametrize("input_data, expected_status, expected_message", [
#     mk.POST_NO_TYPE_IN_PAYLOAD_403,
#     mk.POST_INVALID_TYPE_IN_PAYLOAD_403,
#     mk.POST_MULTI_EVENT_WITH_VALID_PAYLOAD_200,
#     mk.POST_MULTI_EVENT_EVENT_TIME_IN_PAYLOAD_403,
#     mk.POST_MULTI_EVENT_NO_MESSAGE_IN_PAYLOAD_201,
#     mk.POST_MULTI_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403,
#     mk.POST_MULTI_EVENT_NO_EVENT_END_DATE_IN_PAYLOAD_403,
#     mk.POST_MULTI_EVENT_NO_TITLE_IN_PAYLOAD_403,
#     mk.POST_SINGLE_EVENT_WITH_VALID_PAYLOAD_201,
#     mk.POST_SINGLE_EVENT_EVENT_END_DATE_IN_PAYLOAD_403,
#     mk.POST_SINGLE_EVENT_NO_MESSAGE_IN_PAYLOAD_201,
#     mk.POST_SINGLE_EVENT_NO_EVENT_START_DATE_IN_PAYLOAD_403,
#     mk.POST_SINGLE_EVENT_NO_EVENT_TIME_IN_PAYLOAD_403,
#     mk.POST_SINGLE_EVENT_NO_TITLE_IN_PAYLOAD_403,
#     mk.POST_MEMO_WITH_VALID_PAYLOAD_201,
#     mk.POST_MEMO_EVENT_END_DATE_IN_PAYLOAD_403,
#     mk.POST_MEMO_EVENT_START_DATE_IN_PAYLOAD_403

#     ])
# def test_post_data(client, input_data, expected_status, expected_message):
#     response = client.post('/announcements', json=input_data)

#     assert response.status_code == expected_status
#     assert response.json == expected_message