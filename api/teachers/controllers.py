from datetime import datetime, timedelta
from typing import List
from flask import Response, request, jsonify, Request
from sqlalchemy import func
from .validations import teacher_validation
from .data_types import TTeacherPayload
from utils.custom_error import CustomError
from .models import Teacher
import os
from cognito import cognito_client


class Teachers:
    def get(req: Request) -> Response:
        try:
            type = request.args.get("type")
            recipient = request.args.get("recipient")
            event_days = int(request.args.get("event_days", 0))
            search = request.args.get("search")
            from_date = request.args.get("from_date")
            to_date = request.args.get('to_date')
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            query = Teacher.query

            if search:
                query = query.filter(Teacher.title.ilike(f"%{search}%"))

            if recipient:
                if recipient in ("all", "parents", "teachers", "students"):
                    query = query.filter(Teacher.recipient == recipient)
                else:
                    return (
                        jsonify({"error": "invalid recipient: expected (all, parents or students)"}),
                        400,
                    )

            if type:
                if type in ("multi_event", "single_event", "memo"):
                    query = query.filter(Teacher.type == type)
                else:
                    return (
                        jsonify({"error": "invalid type: expected ('multi_event', 'single_event', 'memo')"}),
                        400,
                    )

            if type not in ("memo", "single_event") and event_days:
                query = query.filter(func.datediff(Teacher.event_end_date, Teacher.event_start_date) == event_days)

            if from_date:
                try:
                    from_date = datetime.strptime(from_date, "%Y-%m-%d")
                    to_date = to_date and datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(
                        seconds=1
                    )

                    today_date = (
                        datetime.strptime(
                            str(datetime.today().date()),
                            "%Y-%m-%d",
                        )
                        + timedelta(days=1)
                        - timedelta(seconds=1)
                    )

                    if from_date > today_date:
                        return (
                            jsonify({"error": f"From date should be an older than today's date"}),
                            403,
                        )

                    if to_date and from_date > to_date:
                        return (
                            jsonify({"error": f"From date should be an older than To date"}),
                            403,
                        )
                    query = query.filter(Teacher.date_created.between(from_date, to_date or today_date))

                except ValueError as e:
                    return (
                        jsonify({"error": "Invalid date format: expected YYYY-MM-DD"}),
                        400,
                    )

            query = query.order_by(Teacher.date_created.desc())
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            announcements: List[Teacher] = pagination.items
            total_items = pagination.total
            total_pages = pagination.pages

            data = [announcement.to_dict() for announcement in announcements]
            return (
                jsonify(
                    {
                        "data": data,
                        'per_page': per_page,
                        'total_items': total_items,
                        'page': page,
                        'total_pages': total_pages,
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def post(req: Request) -> Response:
        try:
            data: TTeacherPayload = request.json
            teacher_validation(data, ['password'])

            email = data.get('email')
            password = data.get('password')

            from db import db
            from .models import Teacher

            last_id = getattr(Teacher.query.order_by(Teacher.id.desc()).first(), 'get_id', lambda: None)() or 0
            tag = f'sf-{last_id + 1}'

            cognito = cognito_client()
            cognito.admin_create_user(
                UserPoolId=os.getenv('FLASK_COGNITO_USER_POOL_ID'),
                Username=tag,
                TemporaryPassword=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'username', 'Value': tag}
                    # {'Name': 'email_verified', 'Value': 'true'}
                ],
            )

            cognito.admin_add_user_to_group(
                UserPoolId=os.getenv('FLASK_COGNITO_USER_POOL_ID'),
                Username=tag,
                # Email=email,
                GroupName='staff',
            )

            db.session.add(
                Teacher(
                    first_name=data.get("first_name"),
                    last_name=data.get("last_name"),
                    other_name=data.get("other_name"),
                    gender=data.get("gender"),
                    date_of_birth=(data.get("date_of_birth")),
                    country=(data.get("country")),
                    state_of_origin=(data.get("state_of_origin")),
                    email=(data.get("email")),
                    tier=str(3),
                    tag=tag,
                )
            )

            db.session.commit()

            return jsonify({"message": "Your account has been created"}), 201
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def get_one(req: Request, id: str) -> Response:
        try:
            from db import db

            announcement: Teacher = db.session.get(Teacher, id)

            if announcement == None:
                raise CustomError(f"Teacher with id-{id} not found", 404)
            return jsonify({"data": announcement.to_dict()}), 200

        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def update(req: Request, id: str) -> Response:
        try:
            data: TTeacherPayload = request.json
            from db import db

            announcement: Teacher = db.session.get(Teacher, id)

            if announcement is None:
                raise CustomError(f"Announcement with id-{id} not found", 404)

            keys = request.json.keys()
            for v in keys:
                if v in ('type', "recipient", 'reminder'):
                    raise CustomError(f"Cannot modify {v}", 403)

            data = {**announcement.to_dict(), **data}
            data.pop('date_created')
            data.pop('id')
            teacher_validation(data)

            announcement.title = data.get("title", announcement.title)
            announcement.message = data.get("message", announcement.message)
            announcement.event_start_date = data.get("event_start_date", announcement.event_start_date)
            announcement.event_end_date = data.get("event_end_date", announcement.event_end_date)
            announcement.event_time = data.get("event_time", announcement.event_time)

            from db import db

            db.session.commit()

            return jsonify({"message": f"Announcement with id-{id} has been updated"}), 200
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def delete(req: Request, id: str) -> Response:
        try:
            from db import db

            announcement: Teacher = db.session.get(Teacher, id)

            if announcement is None:
                raise CustomError(f"Announcement with id-{id} not found", 404)
            if announcement.type == 'memo':
                raise CustomError(f"Cannot delete announcement with id-{id} because it is a memo", 403)

            if announcement.event_start_date <= datetime.today().date():
                raise CustomError(f"Can't delete today's event or past event announcement", 403)

            db.session.delete(announcement)
            db.session.commit()

            return jsonify({"message": f"Announcement with id-{id} has been deleted"}), 200
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code
