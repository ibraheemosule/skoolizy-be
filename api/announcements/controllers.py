from datetime import datetime, timedelta
from flask import Response, request, jsonify
from sqlalchemy import func

from utils.email_utils import send_email
from utils.get_html import default_html
from utils.helpers import today_date
from utils.success_handlers import res, res_paginated
from .data_types import TAnnouncementPayload
from utils.error_handlers import CustomError
from .models import Announcement, AnnouncementSchema
from configs.db import db

schema = AnnouncementSchema()


class Announcements:
    def get(self) -> Response:
        req: TAnnouncementPayload = request.args.get

        announcement_type = req(
            "announcement_type",
        )
        recipient = req("recipient")
        event_days = int(req("event_days", 0))
        search = req("search")
        from_date = req("from_date")
        to_date = req('to_date')
        page = int(req('page', 1))
        per_page = int(req('per_page', 10))

        query = Announcement.query

        if search:
            query = query.filter(Announcement.title.ilike(f"%{search}%"))

        if recipient:
            if recipient in ("all", "parents", "teachers", "students"):
                query = query.filter(Announcement.recipient == recipient)
            else:
                raise CustomError("invalid recipient: expected (all, parents or students)", 400)

        if announcement_type:
            if announcement_type in ("multi_event", "single_event", "memo"):
                query = query.filter(Announcement.announcement_type == announcement_type)
            else:
                raise CustomError("invalid announcement_type: expected ('multi_event', 'single_event', 'memo')", 400)

        if announcement_type not in ("memo", "single_event") and event_days:
            query = query.filter(
                func.datediff(Announcement.event_end_date, Announcement.event_start_date) == event_days
            )

        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            to_date = to_date and datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

            if from_date > today_date():
                raise CustomError("From date should be an older than today's date")

            if to_date and from_date > to_date:
                raise CustomError("From date should be an older than To date")

            query = query.filter(Announcement.created_at.between(from_date, to_date or today_date()))

        return res_paginated(
            list_type="Announcement",
            schema=AnnouncementSchema(many=True),
            query=query.order_by(Announcement.created_at.desc()),
            per_page=per_page,
            page=page,
        )

    def post(self, user) -> Response:
        data: TAnnouncementPayload = request.get_json()

        data["created_by"] = user['tag']

        if 'tag' not in user or not user['tag']:
            raise CustomError("User identity trying to perform action is unknown", 401)

        announcement: Announcement = schema.load(data, session=Announcement)

        db.session.add(announcement)
        db.session.commit()

        send_email(
            subject="New Announcement From Skoolizy",
            recipients=["ibraheemsulay@gmail.com"],
            message=default_html(title=data["title"], message=f"<p>Hello,</p>{data['message']}"),
        )

        if data.get("reminder"):
            _id = schema.dump(Announcement.query.order_by(Announcement.id.desc()).first())['id']

            from utils.email_utils import schedule_email

            schedule_email(
                **{
                    "id": str(_id),
                    "subject": 'New Announcement From Skoolizy',
                    "message": default_html(title=data["title"], message=data["message"]),
                    "recipient": ["ibraheemsulay@gmail.com"],
                    "interval": data['reminder'],
                    "event_start_date": data["event_start_date"],
                }
            )

        return res(message="Announcement has been sent")

    def get_one(self, id: str) -> Response:
        announcement: Announcement = db.session.get(Announcement, id)

        if announcement == None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        return res(data=schema.dump(announcement), message="Announcement retrieved successfully")

    def update(self, id: str) -> Response:
        data = request.get_json()

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        validated_announcement = schema.load(data, partial=True, session=db.session)

        announcement: Announcement = db.session.get(Announcement, id)

        if announcement is None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        for v in data.keys():
            if v in ('announcement_type', "recipient", 'reminder'):
                raise CustomError(f"Cannot modify {v}", 403)

        for key, value in validated_announcement.items():
            if hasattr(announcement, key):
                setattr(announcement, key, value)

        db.session.commit()

        send_email(
            subject="(Updated) Announcement From Skoolizy",
            recipients=["ibraheemsulay@gmail.com"],
            message=default_html(title=data["title"], message=f"<p>Hello,</p>{data['message']}"),
        )

        return res(message=f"Announcement with id-{id} has been updated")

    def delete(self, id: str) -> Response:
        announcement: Announcement = db.session.get(Announcement, id)

        if announcement is None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        if announcement.announcement_type == 'memo':
            raise CustomError(f"Cannot delete announcement with id-{id} because it is a memo", 403)

        if announcement.event_start_date <= datetime.today().date():
            raise CustomError("Can't delete today's event or past event announcement", 403)

        db.session.delete(announcement)
        db.session.commit()

        return res(message=f"Announcement with id-{id} has been deleted", status_code=204)

    def stop_reminder(self, id: str):
        from utils import email_utils

        email_utils.stop_scheduled_email(id)

        announcement: Announcement = db.session.get(Announcement, id)
        announcementNaNpxinder = None

        db.session.commit()

        return res(message=f"Reminder email for announcement id-{id} has been stopped", status_code=202)
