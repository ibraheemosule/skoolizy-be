
from .data_types import TAnnouncementPayload
from utils.custom_error import CustomError


def announcements_validation(payload: TAnnouncementPayload):
    keys = TAnnouncementPayload.__annotations__.keys()
    pass

    errors = []

    if payload['type'] == 'memo':
        for k in keys:
            if k in ['event_start_date', 'event_end_date', 'event_time']:
                errors.append(f"{k} is an invalid payload")
            elif payload.get(k) is None:
                errors.append(f"{k} is empty")
    
    if payload['type'] == 'single_event':
        for k in keys:
            if k == 'event_end_date':
                 errors.append(f"{k} is an invalid payload")
            elif payload.get(k) is None:
                errors.append(f"{k} is empty")
            
    if payload['type'] == 'multi_event':

        for k in keys:
            if k == 'event_time':
                  errors.append(f"{k} is an invalid payload")
            elif payload.get(k) is None:
                errors.append(f"{k} is empty")
    
    if len(errors):
        raise CustomError(', '.join(errors), 403)