from datetime import datetime, timedelta
from typing import List
from flask import Response, request, jsonify, Request
from sqlalchemy import func
from .validations import announcements_validation
from .data_types import TAnnouncementPayload
from utils.error_handlers import CustomError
from .models import Announcement
from utils import get_html


class Announcements:
    def get(self) -> Response:
        try:
            type = request.args.get("type")
            recipient = request.args.get("recipient")
            event_days = int(request.args.get("event_days", 0))
            search = request.args.get("search")
            from_date = request.args.get("from_date")
            to_date = request.args.get('to_date')
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            query = Announcement.query

            if search:
                query = query.filter(Announcement.title.ilike(f"%{search}%"))

            if recipient:
                if recipient in ("all", "parents", "teachers", "students"):
                    query = query.filter(Announcement.recipient == recipient)
                else:
                    return (
                        jsonify({"error": "invalid recipient: expected (all, parents or students)"}),
                        400,
                    )

            if type:
                if type in ("multi_event", "single_event", "memo"):
                    query = query.filter(Announcement.type == type)
                else:
                    return (
                        jsonify({"error": "invalid type: expected ('multi_event', 'single_event', 'memo')"}),
                        400,
                    )

            if type not in ("memo", "single_event") and event_days:
                query = query.filter(
                    func.datediff(Announcement.event_end_date, Announcement.event_start_date) == event_days
                )

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
                    query = query.filter(Announcement.date_created.between(from_date, to_date or today_date))

                except ValueError as e:
                    return (
                        jsonify({"error": "Invalid date format: expected YYYY-MM-DD"}),
                        400,
                    )

            query = query.order_by(Announcement.date_created.desc())
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            announcements: List[Announcement] = pagination.items
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

    def post(self) -> Response:
        try:
            data: TAnnouncementPayload = request.json
            announcements_validation(data)

            from db import db
            from .models import Announcement

            db.session.add(
                Announcement(
                    title=data.get("title"),
                    type=data.get("type"),
                    message=data.get("message"),
                    recipient=data.get("recipient", "all"),
                    event_start_date=(data.get("event_start_date")),
                    event_end_date=(data.get("event_end_date")),
                    event_time=(data.get("event_time")),
                    reminder=data.get("reminder") and str(data.get("reminder")),
                )
            )

            db.session.commit()

            if data.get("reminder"):
                message = (
                    get_html.get_email('boilerplate.html')
                    .replace("{{message}}", data['message'])
                    .replace("{{title}}", data["title"])
                )
                _id = Announcement.query.order_by(Announcement.id.desc()).first().to_dict()['id']

                from utils.email_utils import schedule_email

                schedule_email(
                    **{
                        "id": str(_id),
                        "subject": 'New Announcement From Skoolizy',
                        "message": message,
                        "recipient": ["sulayibraheem@gmail.com"],
                        "interval": data['reminder'],
                        "event_start_date": data["event_start_date"],
                    }
                )

            return jsonify({"message": "Announcement has been sent"}), 201
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def get_one(self, id: str) -> Response:
        try:
            from db import db

            announcement: Announcement = db.session.get(Announcement, id)

            if announcement == None:
                raise CustomError(f"Announcement with id-{id} not found", 404)
            return jsonify({"data": announcement.to_dict()}), 200

        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def update(self, id: str) -> Response:
        try:
            data: TAnnouncementPayload = request.json

            from db import db

            announcement: Announcement = db.session.get(Announcement, id)

            if announcement is None:
                raise CustomError(f"Announcement with id-{id} not found", 404)

            keys = request.json.keys()
            for v in keys:
                if v in ('type', "recipient", 'reminder'):
                    raise CustomError(f"Cannot modify {v}", 403)

            data = {**announcement.to_dict(), **data}
            data.pop('date_created')
            data.pop('id')
            announcements_validation(data)

            announcement.title = data.get("title", announcement.title)
            announcement.message = data.get("message", announcement.message)
            announcement.event_start_date = data.get("event_start_date", announcement.event_start_date)
            announcement.event_end_date = data.get("event_end_date", announcement.event_end_date)
            announcement.event_time = data.get("event_time", announcement.event_time)

            db.session.commit()

            return jsonify({"message": f"Announcement with id-{id} has been updated"}), 200
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def delete(self, id: str) -> Response:
        try:
            from db import db

            announcement: Announcement = db.session.get(Announcement, id)
            if announcement is None:
                raise CustomError(f"Announcement with id-{id} not found", 404)
            if announcement.type == 'memo':
                raise CustomError(f"Cannot delete announcement with id-{id} because it is a memo", 403)

            if announcement.event_start_date <= datetime.today().date():
                raise CustomError("Can't delete today's event or past event announcement", 403)

            db.session.delete(announcement)
            db.session.commit()

            return jsonify({"message": f"Announcement with id-{id} has been deleted"}), 200
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def stop_reminder(self, id: str):
        from utils import email_utils

        email_utils.stop_scheduled_email(id)

        from db import db

        announcement: Announcement = db.session.get(Announcement, id)
        announcement.reminder = None

        db.session.commit()

        return jsonify({"message": f"Reminder email stopped for job id-{id}"}), 200
