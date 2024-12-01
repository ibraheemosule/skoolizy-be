from datetime import datetime, timedelta
from flask import Response, request, jsonify
from sqlalchemy import func, or_

from api.staffs.model_staffs import Staff
from api.staffs.schema_staff import StaffSchema
from utils.email_utils import send_email
from utils.get_html import default_html
from utils.helpers import model_to_dict, today_date
from utils.success_handlers import res, res_paginated
from utils.constants import groups
from .types_announcements import TAnnouncementPayload
from utils.error_handlers import CustomError
from .model_announcements import Announcement
from .schema_announcements import AnnouncementSchema
from .constants_announcements import announcement_permission, get_recipients_email, immutable_announcement_fields
from configs.db import db

schema = AnnouncementSchema()
staff_schema = StaffSchema(many=True, session=db.session)


class Announcements:
    def get(self) -> Response:
        req: TAnnouncementPayload = request.args.get
        session_user = request.session_user

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
            permission = announcement_permission(session_user)

            if recipient not in (*groups, "general"):
                raise CustomError("invalid recipient: expected (general, guardians, staffs or students)", 400)

            if recipient not in permission:
                raise CustomError(f"You are not authorized to view {recipient}", 401)

            query = query.filter(Announcement.recipient == recipient)
        else:
            query = query.filter(
                or_(Announcement.recipient == session_user["group"], Announcement.recipient == 'general')
            )

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

    def post(self) -> Response:
        data: TAnnouncementPayload = request.get_json()
        session_user = request.session_user
        group = session_user.get('group')

        data["created_by"] = session_user['tag']

        if group != "staffs":
            raise CustomError("You are not allowed to create an announcement")

        announcement: Announcement = schema.load(data, session=db.session)

        if announcement.recipient not in ('general', *groups):
            raise CustomError(message="Can not create announcement to an unknown recipient group")

        recipients = get_recipients_email(announcement)

        if len(recipients) == 0:
            raise CustomError(
                message=f"Can not create announcement. No account associated with {announcement.recipient} group."
            )

        db.session.add(announcement)
        db.session.commit()

        send_email(
            subject="New Announcement From Skoolizy",
            recipients=recipients,
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
                    "recipient": recipients,
                    "interval": data['reminder'],
                    "event_start_date": announcement.event_start_date,
                }
            )

        return res(message="Announcement has been sent", status_code=201)

    def get_one(self, id: str) -> Response:
        announcement: Announcement = db.session.get(Announcement, id)

        if announcement == None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        return res(data=schema.dump(announcement), message="Announcement retrieved successfully")

    def update(self, id: str) -> Response:
        data = request.get_json()
        session_user = request.session_user

        if len(data.keys()) == 0:
            raise CustomError("No payload was sent")

        if session_user["group"] != 'staffs':
            raise CustomError(f"You are not authorized to perform this action", 401)

        announcement: Announcement = db.session.get(Announcement, id)

        if announcement is None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        announcement_dict = {**model_to_dict(announcement), **data}

        validated_announcement = schema.load(announcement_dict, session=db.session)

        for key, value in schema.dump(validated_announcement).items():
            if key in immutable_announcement_fields:
                continue
            setattr(announcement, key, value)

        db.session.commit()

        recipients = get_recipients_email(announcement)

        send_email(
            subject="(Updated) Announcement From Skoolizy",
            recipients=recipients,
            message=default_html(
                title=data.get("title", announcement.title),
                message=f"<p>Hello,</p>{data.get('message', announcement.message)}",
            ),
        )

        return res(message=f"Announcement with id-{id} has been updated")

    def delete(self, id: str) -> Response:
        session_user = request.session_user

        if session_user["group"] != 'staffs':
            raise CustomError(f"You are not authorized to perform this action", 401)

        announcement: Announcement = db.session.get(Announcement, id)

        if announcement is None:
            raise CustomError(f"Announcement with id-{id} not found", 404)

        if announcement.announcement_type == 'memo':
            raise CustomError(f"Cannot delete announcement with id-{id} because it is a memo", 403)

        if announcement.event_start_date <= datetime.today().date():
            raise CustomError("You can only delete future announcements", 403)

        db.session.delete(announcement)
        db.session.commit()

        recipients = get_recipients_email(announcement)

        send_email(
            subject="(Deleted) Announcement From Skoolizy",
            recipients=recipients,
            message=default_html(
                title=announcement.title,
                message=f"<p style='display: block;'>Hello,</p>{announcement.message}",
            ),
        )

        return res(message=f"Announcement with id-{id} has been deleted", status_code=204)

    def stop_reminder(self, id: str):
        from utils import email_utils

        announcement: Announcement = db.session.get(Announcement, id)

        if announcement == None:
            raise CustomError(message=f"Announcement with id-{id} not found", status_code=404)

        if announcement.reminder:
            email_utils.stop_scheduled_email(id)

            announcement.reminder = None
            db.session.commit()

            return res(message=f"Reminder email for announcement id-{id} has been stopped", status_code=202)

        return res(message=f"Announcement with id-{id} has no reminder")
