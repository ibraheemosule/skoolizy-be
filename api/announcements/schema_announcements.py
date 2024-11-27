from api.staffs.schema_staff import StaffSchema
from marshmallow import pre_load, validate, validates, validates_schema
from configs.db.base_schemas.base_schema import BaseSchema
from utils.error_handlers import CustomError
from utils.helpers import format_date_time, today_date
from utils.constants import groups
from .model_announcements import Announcement

from marshmallow import fields

# class Nested(fields.Nested):
#     """Nested field that inherits the session from its parent."""

#     def _deserialize(self, *args, **kwargs):
#         if hasattr(self.schema, "session"):
#             self.schema.session = db.session
#             self.schema.transient = self.root.transient
#         return super()._deserialize(*args, **kwargs)


class AnnouncementSchema(BaseSchema):
    class Meta:
        model = Announcement
        load_instance = True

    recipient = fields.String(validate=validate.OneOf(['all', *groups]), missing='all')
    created_at = fields.DateTime(dump_only=True)
    title = fields.String(validate=validate.Length(min=10, max=100), required=True)
    announcement_type = fields.String(validate=validate.OneOf(["memo", "single_event", "multi_event"]), required=True)
    message = fields.String(validate=validate.Length(min=20, max=1000), allow_none=True)
    event_start_date = fields.Date(allow_none=True)
    event_end_date = fields.Date(allow_none=True)
    event_time = fields.Time(allow_none=True)
    reminder = fields.Int(validate=validate.OneOf([1, 2, 3, 4, 5, 6, 7]), missing=None)
    creator = fields.Nested(
        StaffSchema, only=["tag", "email", "first_name"], dump_only=True, attribute="creator", data_key="created_by"
    )
    created_by = fields.String(
        required=True,
        load_only=True,
    )

    @pre_load
    def format_dates(self, data, **kwargs):
        try:
            if event_start_date := data.get('event_start_date'):
                data["event_start_date"] = format_date_time(event_start_date)["date_str"]

            if event_end_date := data.get('event_end_date'):
                data["event_end_date"] = format_date_time(event_end_date)["date_str"]

        except ValueError:
            raise CustomError("Invalid date format provided")

        return data

    @validates_schema
    def validate(self, data, **kwargs):
        announcement_type = data.get('announcement_type')
        event_start_date = data.get('event_start_date')
        event_end_date = data.get('event_end_date')

        if announcement_type == 'memo':
            if data.get('message') == None:
                raise CustomError("Message is required for a memo")

            if event_start_date:
                raise CustomError("Event start date should be omitted for a memo")

            if event_end_date:
                raise CustomError("Event end date should be omitted for a memo")

        if event_start_date == None:
            raise CustomError(
                f"Event start date is required for {announcement_type} event",
            )

        if event_start_date <= today_date().date():
            raise CustomError("event_start_date should be a future date")

        if announcement_type == 'multi_event':
            if event_end_date == None:
                raise CustomError("Event end date is required for multi days event")
            if event_start_date > event_end_date:
                raise CustomError("event_start_date should be an earlier date than event_end_date")

        if announcement_type == 'single_event':
            if data.get('event_time') == None:
                raise CustomError("Event time is required for a single event")

            if event_end_date:
                raise CustomError("Event end date should be omitted for a single event")

    @validates('message')
    def validate_message(self, message: str):
        if message and len(message.strip()) < 30 or len(message.strip()) > 5000:
            raise CustomError("Announcement message must be a minimum of 30 and maximum of 5000 characters", 403)

    @validates('title')
    def validate_message(self, title: str):
        if title and len(title.strip()) < 10 or len(title.strip()) > 50:
            raise CustomError("Announcement title must be a minimum of 10 and maximum of 50 characters", 403)
