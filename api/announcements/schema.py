from sqlalchemy import Enum, String, Time, Date, Integer, Text, TIMESTAMP, func, CheckConstraint
from db import db

class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    recipient = db.Column(Enum('all', 'parents', 'teachers', 'students', name='recipient_enum'), default='all')
    date_created = db.Column(TIMESTAMP, default=func.current_timestamp())
    title = db.Column(String(255), nullable=False)
    type = db.Column(Enum('memo', 'single_event', 'multi_event', name='type_enum'), nullable=False)
    message = db.Column(String(255), nullable=True)
    event_start_date = db.Column(Date, nullable=True)
    event_end_date = db.Column(Date, nullable=True)
    event_time = db.Column(Time, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(type != 'multi_event' OR (event_start_date IS NOT NULL AND event_end_date IS NOT NULL))",
            name='check_multi_event_type'
        ),
        CheckConstraint(
            "(type != 'single_event' OR (event_start_date IS NOT NULL AND event_end_date IS NULL AND event_time IS NOT NULL))",
            name='check_single_event_type'
        ),
        CheckConstraint(
            "(type != 'memo' OR (event_start_date IS NULL AND event_end_date IS NULL AND event_time IS NULL))",
            name='check_memo_type'
        ),
        CheckConstraint(
            "(type != 'memo' OR (message IS NOT NULL))",
            name='check_memo_has_message'
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "recipient": self.recipient,
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "title": self.title,
            "type": self.type,
            "message": self.message,
            "event_start_date": self.event_start_date.isoformat() if self.event_start_date else None,
            "event_end_date": self.event_end_date.isoformat() if self.event_end_date else None,
            "event_time": self.event_time.isoformat() if self.event_time else None
        }
