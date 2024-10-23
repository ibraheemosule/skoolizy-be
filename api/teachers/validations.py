from datetime import datetime
from .data_types import TTeacherPayload
from utils.email_utils import is_email_valid
from utils.helpers import has_special_char, is_password_valid
from utils.error_handlers import CustomError


def teacher_validation(arg: TTeacherPayload, ignore_payloads=[]):
    errors = []

    try:
        keys = list(TTeacherPayload.__annotations__.keys())
        payload = arg.copy()
        password = payload.get('password')

        if password and not is_password_valid(password):
            errors.append(
                'Password must be a minimum of 8 characters long and must contain a capital letter, a small letter, a number and a symbol'
            )

        for p in ignore_payloads:
            if list(payload.keys()).count(p):
                del payload[p]

        for p in keys:
            if payload.get(p):
                del payload[p]
                continue
            p != 'middle_name' and errors.append(f'{p} is required')

        for err_payload in payload.keys():
            errors.append(f'{err_payload} is an invalid payload')

        if len(errors):
            raise CustomError(", ".join(errors), 403)

        payload = arg.copy()

        payload_with_max_len_50 = ('first_name', 'last_name', 'middle_name', 'country', 'state_of_origin', 'email')

        for p in payload_with_max_len_50:
            if p == 'email':
                not is_email_valid(payload[p]) and errors.append('Email is invalid')
                continue

            if p == 'middle_name' and not payload.get(p):
                continue
            if len(payload[p]) > 50:
                errors.append(f'{p} is too long')
            if len(payload[p]) < 3:
                errors.append(f'{p} is too short')
            if has_special_char(payload[p]):
                errors.append("{} has invalid special characters".format(p))

        if payload['gender'] not in ('male', 'female'):
            errors.append("gender should be male or female")

        if len(errors):
            raise CustomError(", ".join(errors), 403)

    except ValueError as e:
        raise CustomError(str(e), 403)
    except AttributeError as e:
        raise CustomError(str(e), 403)
