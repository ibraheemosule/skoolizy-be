from datetime import datetime, timedelta
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError


def announcements_validation(payload: TAnnouncementPayload):
    keys = TAnnouncementPayload.__annotations__.keys()
    errors = []

    invalid_fields = {
        "memo": {
            "invalid_payload": ("event_start_date", "event_end_date", "event_time"),
            "optional_payload": ("recipient"),
        },
        "single_event": {
            "invalid_payload": ("event_end_date"),
            "optional_payload": ("message", "recipient"),
        },
        "multi_event": {
            "invalid_payload": ("event_time"),
            "optional_payload": ("message", "recipient"),
        },
    }

    type = invalid_fields.get(payload.get("type"))

    if invalid_fields.get(payload.get("type")) is None:
        raise CustomError("type should be one of (all, parents, teachers, students)", 403)

    for k in keys:
        if k in type.get("invalid_payload", {}):
            if k in payload and payload[k] != None:
                event_type = payload.get("type")
                errors.append(f"{k} is an invalid payload for {event_type} announcement type")
        elif k not in type.get("optional_payload", {}) and payload.get(k) is None:
            errors.append(f"{k} is required")

    if payload.get("type") != "memo" and (start_date := payload.get("event_start_date")):
        start_date = datetime.strptime(payload.get("event_start_date"), "%Y-%m-%d").date()
        end_date = (
            datetime.strptime(payload.get("event_end_date"), "%Y-%m-%d").date()
            if payload.get("event_end_date")
            else datetime.today().date()
        )

        if payload.get("type") == "multi_event" and start_date > end_date:
            errors.append("event_start_date should be an earlier date than event_end_date")

        if start_date <= datetime.today().date():
            errors.append("event_start_date should be a future day")

    if len(errors):
        raise CustomError(", ".join(errors), 403)
