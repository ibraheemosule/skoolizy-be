import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture(autouse=True)
def set_testing_env(monkeypatch):
    monkeypatch.setenv("ENV", "testing")

def test_get_data(client, mocker):

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {
        "title": "testing",
        "event_time": "05:00:00",
        "event_start_date": "2020-05-23",
        "event_end_date": "2020-05-23",
        "type": "multi_event",
        "message": "here is anotherorking"
        }
    ]

    mocker.patch('app.mysql.connection.cursor', return_value=mock_cursor)

    response = client.get('/announcements')
    data = response.get_json()

    assert response.status_code == 200
    assert data == [
        {
        "title": "testing",
        "event_time": "05:00:00",
        "event_start_date": "2020-05-23",
        "event_end_date": "2020-05-23",
        "type": "multi_event",
        "message": "here is anotherorking"
        }
    ]

# def test_insert_data(client, mocker):
#     mock_cursor = MagicMock()
#     mocker.patch('app.mysql.connection.cursor', return_value=mock_cursor)

#     test_data = {
#         'title': 'Test Title',
#         'type': 'memo',
#         'message': 'Test Message',
#         'date': '2023-06-08',
#         'time': '12:00:00'
#     }

#     response = client.post('/announcements', json=test_data)
#     data = response.get_json()

#     assert response.status_code == 200
#     assert data['message'] == 'Data inserted successfully'

#     mock_cursor.execute.assert_called_once_with(
#         '''INSERT INTO announcements (title, type, message, date, time ) VALUES (%s, %s, %s, %s, %s)''', 
#         ('Test Title', 'memo', 'Test Message', '2023-06-08', '12:00:00')
#     )
#     mock_cursor.close.assert_called_once()

# def test_insert_data_fail(client, mocker):
#     mock_cursor = MagicMock()
#     mock_cursor.execute.side_effect = Exception("Database error")
#     mocker.patch('app.mysql.connection.cursor', return_value=mock_cursor)

#     test_data = {
#         'title': 'Test Title',
#         'type': 'memo',
#         'message': 'Test Message',
#         'date': '2023-06-08',
#         'time': '12:00:00'
#     }

#     response = client.post('/data', json=test_data)
#     data = response.get_json()

#     assert response.status_code == 500
#     assert 'error' in data
#     assert data['error'] == 'Database error'

#     mock_cursor.close.assert_called_once()
