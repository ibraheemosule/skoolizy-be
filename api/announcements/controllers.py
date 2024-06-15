from datetime import datetime, timedelta
from typing import List
from flask import Response, request, jsonify, Request
from sqlalchemy import func, text, Numeric
from .validations import announcements_validation
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError
from .models import Announcement

class Announcements:
    def get(req: Request) -> Response:     
        try:
            type = request.args.get('type')
            recipient = request.args.get('recipient')
            event_duration = int(request.args.get('event_days', 0))
            search = request.args.get('search')
            from_date =  request.args.get('from_date')

            query = Announcement.query
            
            if search: query = query.filter(Announcement.title.ilike(f'%{search}%'))

            if recipient: 
                 if recipient in ('all', 'parents', 'teachers', 'students'): query = query.filter(Announcement.recipient == recipient )
                 else: return jsonify({'error': "invalid recipient: expected (all, parents or students)"}), 400

            if type: 
                 if type in ('multi_event', 'single_event', 'memo'): query = query.filter(Announcement.type == type )
                 else: return jsonify({'error': "invalid type: expected ('multi_event', 'single_event', 'memo')"}), 400

            if type not in ('memo', 'single_event') and event_duration:
                query = query.filter(func.datediff(Announcement.event_end_date, Announcement.event_start_date) == event_duration)

            if from_date:
                try:
                    from_date =  datetime.strptime(from_date, '%Y-%m-%d')
                    to_date =  datetime.strptime(request.args.get('to_date', str(datetime.today().date())), '%Y-%m-%d')+ timedelta(days=1) - timedelta(seconds=1)

                    if from_date > to_date:
                        return jsonify({'error': "from_date should be an older than to_date"})
                    query = query.filter(Announcement.date_created.between(from_date, to_date))

                except ValueError as e:
                    return jsonify({'error': "Invalid date format: expected YYYY-MM-DD"}), 400

            announcements: List[Announcement] =  query.all()
            data = [announcement.to_dict() for announcement in announcements]

            return jsonify({'data': data}), 200
        
        except Exception as e:
             return jsonify({'error': str(e)}), 400

    def post(req: Request) -> Response:
        try:
            data: TAnnouncementPayload = request.json
            announcements_validation(data)

            from db import db
            from .models import Announcement
            db.session.add(Announcement(
            title=data.get('title'),
            type=data.get('type'),
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
    
    def get_one(req: Request, id: str) -> Response:
        try:
            announcement: Announcement =  Announcement.query.get(id)
            if announcement == None:
                raise CustomError(f'Announcement with id-{id} not found', 404)
            return jsonify({'data': announcement.to_dict()}), 200
        
        except CustomError as e:
            return jsonify({'error': str(e)}), e.status_code