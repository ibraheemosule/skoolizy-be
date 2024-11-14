from sqlalchemy import (
    Enum,
    String,
    Time,
    Date,
    Integer,
    TIMESTAMP,
    func,
)
from configs.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError, fields, validate, validates_schema


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    recipient = db.Column(
        Enum("all", "parents", "teachers", "students", name="recipient_enum"),
        default="all",
    )
    date_created = db.Column(TIMESTAMP(timezone=True), default=func.current_timestamp())
    title = db.Column(String(100), nullable=False)
    announcement_type = db.Column(Enum("memo", "single_event", "multi_event", name="type_enum"), nullable=False)
    message = db.Column(String(1000), nullable=True)
    event_start_date = db.Column(Date, nullable=True)
    event_end_date = db.Column(Date, nullable=True)
    event_time = db.Column(Time, nullable=True)
    reminder = db.Column(Integer(), default=None)


class AnnouncementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Announcement
        load_instance = True

    recipient = fields.String(validate=validate.OneOf(['all', 'parents', 'teachers', 'students']), default='all')
    date_created = fields.DateTime()
    title = fields.String(validate=validate.Length(min=10, max=100), required=True)
    announcement_type = fields.String(validate=validate.OneOf(["memo", "single_event", "multi_event"]), required=True)
    message = fields.String(validate=validate.Length(min=20, max=1000))
    event_start_date = fields.DateTime()
    event_end_date = fields.DateTime()
    event_time = fields.Time()
    reminder = fields.Int(validate=validate.OneOf([1, 2, 3, 4, 5, 6, 7]))

    @validates_schema
    def validate(self, data, **kwargs):
        announcement_type = data.get('type')
        event_start_date = data.get('event_start_date')
        event_end_date = data.get('event_end_date')
        event_time = data.get('event_time')
        message = data.get('message')

        if announcement_type == 'multi_event':
            if event_start_date == None:
                raise ValidationError("Event start date is required for multi days event", 'event_start_date')

            if event_end_date == None:
                raise ValidationError("Event end date is required for multi days event", 'event_end_date')

        if announcement_type == 'single_event':
            if event_start_date == None:
                raise ValidationError("Event start date is required for a single event", 'event_start_date')

            if event_time == None:
                raise ValidationError("Event time is required for a single event", 'event_time')

            if event_end_date:
                raise ValidationError("Event end date should be omitted for a single event", 'event_end_date')

        if announcement_type == 'memo':
            if message == None:
                raise ValidationError("Message is required for a memo", 'message')

            if event_start_date:
                raise ValidationError("Event start date should be omitted for a memo", 'event_start_date')

            if event_end_date:
                raise ValidationError("Event end date should be omitted for a memo", 'event_end_date')
