from typing import List, Dict
from flask import Response, json, request, jsonify, Request
from .validations import announcements_validation
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError


class Announcements:
    def get(req: Request) -> Response:
        from app import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM announcements")
        data: List[Dict[str, int | str]] = cursor.fetchall()
        res = json.dumps(data, indent=1, sort_keys=True, default=str)
        return json.loads(res)
    

    def post(req: Request) -> Response:
        try:
            from app import mysql 
            data: TAnnouncementPayload = request.json
            announcements_validation(data)
            cursor = mysql.connection.cursor()
            cursor.execute(
                '''INSERT INTO announcements (title, type, message, event_start_date, event_end_date, event_time) VALUES (%s, %s, %s, %s, %s, %s)''', 
                (data.get('title'), data.get('type'), data.get('message'), data.get('event_start_date'), data.get('event_end_date'), data.get('event_time'))
            )
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Data inserted successfully'}), 200
        except  CustomError as e:
            return jsonify({'error': str(e)}), e.status_code