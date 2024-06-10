
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError


def announcements_validation(payload: TAnnouncementPayload):
    keys = TAnnouncementPayload.__annotations__.keys()
    errors = []

    invalid_fields = {
        'memo': {'invalid_payload': ('event_start_date', 'event_end_date', 'event_time'),'optional_payload': ()},
        'single_event': {'invalid_payload': ('event_end_date'), 'optional_payload': ('message')},
        'multi_event': {'invalid_payload': ('event_time'), 'optional_payload': ('message')}
    }

    type = invalid_fields.get(payload.get('type'))

    if type == None:
        raise CustomError('type is required', 403)
    
    for k in keys:
        if k in type.get('invalid_payload', {}):
            if k in payload:
                errors.append(f"{k} is an invalid payload")
        elif k not in type.get('optional_payload', {}) and payload.get(k) is None:
            errors.append(f"{k} is required")
    
    if len(errors):
        print(errors)
        raise CustomError(', '.join(errors), 403)