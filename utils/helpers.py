from datetime import datetime
import re
from typing import Dict


def has_special_char(s):
    pattern = r"[<>\'\";`$!&|\\(){}[\]^~#@/]"

    if isinstance(s, str) and re.search(pattern, s):
        return True
    return False


def is_password_valid(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-])[A-Za-z\d!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-]{8,}$'
    return True if re.match(pattern, password) else False


def get_date_and_time(date: str) -> Dict:
    date, time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").__str__().split(' ')
    return {"date": date, time: "time"}


def get_date(date: str):
    return datetime.strftime(date, "%Y-%m-%d")


def get_time(time: str):
    return datetime.strftime(time, "%H:%M:%S")


def today_date() -> datetime:
    return datetime.combine(datetime.today().date(), datetime.max.time())


def days_diff(date: datetime) -> datetime:
    return (today_date() - date).days


def years_diff(date: datetime) -> datetime:
    return today_date().year - date.year
