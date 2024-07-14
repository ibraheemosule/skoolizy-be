from datetime import datetime
from .data_types import TTeacherPayload
from utils.custom_error import CustomError
from utils.email_utils import is_email_valid
from utils.helpers import has_special_char


def teacher_validation(arg: TTeacherPayload, ignore_payloads=[]):
    errors = []
    keys = list(TTeacherPayload.__annotations__.keys())
    payload = arg.copy()

    for p in ignore_payloads:
        if list(payload.keys()).count(p):
            del payload[p]

    for p in keys:
        if payload.get(p):
            del payload[p]
            continue
        p != 'other_name' and errors.append(f'{p} is required')

    for err_payload in payload.keys():
        errors.append(f'{err_payload} is an invalid payload')

    if len(errors):
        raise CustomError(", ".join(errors), 403)

    payload = arg.copy()

    payload_with_max_len_50 = ('first_name', 'last_name', 'other_name', 'country', 'state_of_origin', 'email')

    for p in payload_with_max_len_50:
        if p == 'email':
            not is_email_valid(payload[p]) and errors.append('Email is invalid')
            continue

        if p == 'other_name' and not payload.get(p):
            continue
        if len(payload[p]) > 50:
            errors.append(f'{p} is too long')
        if len(payload[p]) < 3:
            errors.append(f'{p} is too short')
        if has_special_char(payload[p]):
            errors.append(f'{p} has invalid special characters')

    if payload['gender'] not in ('male', 'female'):
        errors.append(f'gender should be male or female')

    if len(errors):
        raise CustomError(", ".join(errors), 403)

    # invalid_fields = {
    #     "memo": {
    #         "invalid_payload": ("event_start_date", "event_end_date", "event_time", "reminder"),
    #         "optional_payload": ("recipient"),
    #     },
    #     "single_event": {
    #         "invalid_payload": ("event_end_date"),
    #         "optional_payload": ("message", "recipient", "reminder"),
    #     },
    #     "multi_event": {
    #         "invalid_payload": ("event_time"),
    #         "optional_payload": ("message", "recipient", "reminder"),
    #     },
    # }

    # type = invalid_fields.get(payload.get("type"))

    # if invalid_fields.get(payload.get("type")) is None:
    #     raise CustomError("type should be one of (memo, single_event, multi_event)", 403)

    # if payload.get('recipient', 'all') not in ('all', 'teachers', 'students', 'parents'):
    #     raise CustomError("recipient should be one of (all, parents, teachers, students)", 403)

    # title = payload.get('title', '').strip()

    # if title and len(title) < 10 or len(title) > 50:
    #     raise CustomError("Announcement title must be a minimum of 10 and maximum of 50 characters", 403)

    # message = payload.get('message', '').strip()
    # if message and len(message) < 30 or len(message) > 5000:
    #     raise CustomError("Announcement message must be a minimum of 30 and maximum of 5000 characters", 403)

    # if reminder := payload.get("reminder"):
    #     if int(reminder) not in range(1, 8):
    #         raise CustomError("Reminder must be between (1, 2, 3, 4, 5, 6, 7) days", 403)

    # for k in keys:
    #     if k in type.get("invalid_payload", {}):
    #         if k in payload and payload[k] != None:
    #             event_type = payload.get("type")
    #             errors.append(f"{k} is an invalid payload for {event_type} announcement type")
    #     elif k not in type.get("optional_payload", {}) and not (payload.get(k)):
    #         errors.append(f"{k} is required")

    # if payload.get("type") != "memo" and (start_date := payload.get("event_start_date")):
    #     start_date = datetime.strptime(payload.get("event_start_date"), "%Y-%m-%d").date()
    #     end_date = (
    #         datetime.strptime(payload.get("event_end_date"), "%Y-%m-%d").date()
    #         if payload.get("event_end_date")
    #         else datetime.today().date()
    #     )

    #     if payload.get("type") == "multi_event" and start_date > end_date:
    #         errors.append("event_start_date should be an earlier date than event_end_date")

    #     if start_date <= datetime.today().date():
    #         errors.append("event_start_date should be a future date")

    if len(errors):
        raise CustomError(", ".join(errors), 403)
