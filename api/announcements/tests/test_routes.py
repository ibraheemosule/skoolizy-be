import pytest
from unittest.mock import MagicMock, patch
from app import app as flask_app
from . import mock_data as mk

def test_get_data(client):
    # Create a MagicMock for the cursor and set up its return value
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [mk.ANNOUNCEMENT_PAYLOAD]
    # Ensure that the application context is active
    with flask_app.app_context():
        # Patch the entire `app.mysql` module
        with patch('app.mysql', autospec=True) as mock_mysql:
            # Configure the mock to return the mock cursor
            mock_mysql.connection.cursor.return_value = mock_cursor
            # Make the request to the client
            response = client.get('/announcements')
            data = response.get_json()

            assert response.status_code == 200
            assert data == [mk.ANNOUNCEMENT_PAYLOAD]

@pytest.mark.parametrize("input_data, expected_status, expected_message", [
    mk.POST_NO_TYPE_IN_PAYLOAD_403,
    mk.POST_MULTI_EVENT_WITH_VALID_PAYLOAD_200,
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
def test_post_data(client, input_data, expected_status, expected_message):

    mock_cursor = MagicMock()
    mock_cursor.execute.return_value = None

    # Ensure that the application context is active
    with flask_app.app_context():
        with patch('app.mysql', autospec=True) as mock_mysql:
            mock_mysql.connection.cursor.return_value = mock_cursor

            response = client.post('/announcements', json=input_data)

            assert response.status_code == expected_status
            assert response.json == expected_message