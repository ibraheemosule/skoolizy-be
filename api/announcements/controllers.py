from typing import List
from flask import Response, request, jsonify, Request
from .validations import announcements_validation
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError
from .models import Announcement

class Announcements:
    def get(req: Request) -> Response:
        announcements: List[Announcement] =  Announcement.query.all()
        data = [announcement.to_dict() for announcement in announcements]
        return jsonify(data), 200

    def post(req: Request) -> Response:
        try:
            data: TAnnouncementPayload = request.json
            announcements_validation(data)

            from db import db
            from .models import Announcement
            db.session.add(Announcement(
            title=data['title'],
            type=data['type'],
            message=data.get('message'),
            recipient=data.get('recipient', 'all'),
            event_start_date=(data.get('event_start_date')),
            event_end_date=(data.get('event_end_date')),
            event_time=(data.get('event_time'))
            ))

            db.session.commit()
            return jsonify({'message': 'Data inserted successfully'}), 201
        except  CustomError as e:
            return jsonify({'error': str(e)}), e.status_code