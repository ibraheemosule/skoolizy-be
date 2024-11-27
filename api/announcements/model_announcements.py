from sqlalchemy import Enum, String, Time, Date, Integer, TIMESTAMP, func, ForeignKey, orm
from configs.db import db
from utils.error_handlers import CustomError
from utils.constants import groups
from utils.helpers import field_update_fn
from .constants_announcements import immutable_announcement_fields, announcement_types


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(Integer(), primary_key=True, autoincrement=True)
    recipient = db.Column(Enum(*groups, "all"))
    created_at = db.Column(TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=None)
    title = db.Column(String(100), nullable=False)
    announcement_type = db.Column(
        Enum(*announcement_types, name="announcement_type_enum"), nullable=False, onupdate=None
    )
    message = db.Column(String(1000), nullable=True)
    event_start_date = db.Column(Date, nullable=True)
    event_end_date = db.Column(Date, nullable=True)
    event_time = db.Column(Time, nullable=True)
    reminder = db.Column(Integer(), default=None, nullable=True)
    created_by = db.Column(String(30), ForeignKey('staffs.tag'), nullable=False)

    creator = db.relationship("Staff")

    @orm.validates(*immutable_announcement_fields)
    def set_once(self, key, value):
        prev_value = getattr(self, key)

        if key == "reminder" and value in (prev_value, None):
            return value

        return field_update_fn(self, key, value)
