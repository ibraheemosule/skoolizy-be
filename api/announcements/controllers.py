from datetime import datetime, timedelta
from typing import List
from flask import Response, request, jsonify, Request
from sqlalchemy import func
from .validations import announcements_validation
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError
from .models import Announcement


class Announcements:
    def get(req: Request) -> Response:
        try:
            type = request.args.get("type")
            recipient = request.args.get("recipient")
            event_days = int(request.args.get("event_days", 0))
            search = request.args.get("search")
            from_date = request.args.get("from_date")
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
                    to_date = (
                        datetime.strptime(
                            request.args.get("to_date", str(datetime.today().date())),
                            "%Y-%m-%d",
                        )
                        + timedelta(days=1)
                        - timedelta(seconds=1)
                    )

                    if from_date > to_date:
                        return jsonify({"error": "from_date should be an older than to_date"})
                    query = query.filter(Announcement.date_created.between(from_date, to_date))

                except ValueError as e:
                    return (
                        jsonify({"error": "Invalid date format: expected YYYY-MM-DD"}),
                        400,
                    )

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

    def post(req: Request) -> Response:
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
                )
            )

            db.session.commit()
            return jsonify({"message": "Data inserted successfully"}), 201
        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code

    def get_one(req: Request, id: str) -> Response:
        try:
            announcement: Announcement = Announcement.query.get(id)
            if announcement == None:
                raise CustomError(f"Announcement with id-{id} not found", 404)
            return jsonify({"data": announcement.to_dict()}), 200

        except CustomError as e:
            return jsonify({"error": str(e)}), e.status_code
