
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError


def announcements_validation(payload: TAnnouncementPayload):
    keys = TAnnouncementPayload.__annotations__.keys()
    errors = []

    invalid_fields = {
        'memo': {'event_start_date', 'event_end_date', 'event_time'},
        'single_event': {'event_end_date'},
        'multi_event': {'event_time'}
    }

    for k in keys:
        if k in invalid_fields.get(payload['type'], {}):
            if k in payload:
                errors.append(f"{k} is an invalid payload")
        elif payload.get(k) is None:
            errors.append(f"{k} is empty")
    
    if len(errors):
        raise CustomError(', '.join(errors), 403)