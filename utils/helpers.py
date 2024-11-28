from datetime import date, datetime, time
import re
from typing import Dict, Optional, Union

from utils.error_handlers import CustomError


def has_special_char(s):
    pattern = r"[<>\'\";`$!&|\\(){}[\]^~#@/]"

    if isinstance(s, str) and re.search(pattern, s):
        return True
    return False


def is_password_valid(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-])[A-Za-z\d!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-]{8,}$'
    return True if re.match(pattern, password) else False


def format_date_time(
    date_str_or_obj: Union[str, datetime, date, time]
) -> Dict[str, Optional[Union[str, datetime, date, time]]]:
    if not date_str_or_obj:
        raise TypeError("Input must be a non-empty string, datetime, date, or time object")

    date_str, time_str, date_parse, time_parse, datetime_parse, datetime_str = None, None, None, None, None, None

    if isinstance(date_str_or_obj, str):
        formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str_or_obj, fmt)
                date_str = parsed.strftime("%Y-%m-%d")
                time_str = parsed.strftime("%H:%M:%S")
                date_parse = parsed.date()
                time_parse = parsed.time()
                datetime_parse = parsed
                datetime_str = parsed.isoformat()
                break
            except ValueError:
                continue
        if not date_str:
            raise ValueError("Invalid date string format")

    elif isinstance(date_str_or_obj, datetime):
        date_str = date_str_or_obj.strftime("%Y-%m-%d")
        time_str = date_str_or_obj.strftime("%H:%M:%S")
        date_parse = date_str_or_obj.date()
        time_parse = date_str_or_obj.time()
        datetime_parse = date_str_or_obj
        datetime_str = date_str_or_obj.isoformat()

    elif isinstance(date_str_or_obj, date):
        date_str = date_str_or_obj.strftime("%Y-%m-%d")
        date_parse = date_str_or_obj
        datetime_parse = datetime.combine(date_str_or_obj, time.min)
        datetime_str = datetime_parse.isoformat()

    elif isinstance(date_str_or_obj, time):
        time_str = date_str_or_obj.strftime("%H:%M:%S")
        time_parse = date_str_or_obj
        datetime_parse = datetime.combine(datetime.today(), date_str_or_obj)
        datetime_str = datetime_parse.isoformat()

    else:
        raise TypeError("Input must be a string, datetime, date, or time object")

    return {
        "date_str": date_str,
        "time_str": time_str,
        "date_parse": date_parse,
        "time_parse": time_parse,
        "datetime_parse": datetime_parse,
        "datetime_str": datetime_str,
    }


def parse_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d")


def get_time(time: str):
    return datetime.strftime(time, "%H:%M:%S")


def today_date() -> datetime:
    return datetime.combine(datetime.today().date(), datetime.max.time())


def days_diff(date: datetime) -> datetime:
    return (today_date() - date).days


def years_diff(date: datetime) -> datetime:
    return today_date().year - date.year


def model_to_dict(model_instance):
    """
    Converts a SQLAlchemy model instance to a dictionary.
    """
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}


def field_update_fn(self, key, value):
    prev_value = getattr(self, key)
    new_value = value

    if isinstance(prev_value, date):
        prev_value = prev_value.isoformat()

    if isinstance(new_value, date):
        new_value = new_value.isoformat()
    if prev_value is not None and prev_value != new_value:
        raise CustomError(f"{key} cannot be updated once set.")
    return value
