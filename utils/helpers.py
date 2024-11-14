from datetime import datetime, timedelta
import re


def has_special_char(s):
    pattern = r"[<>\'\";`$!&|\\(){}[\]^~#@/]"

    if re.search(pattern, s):
        return True
    return False


def is_password_valid(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-])[A-Za-z\d!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-]{8,}$'
    return True if re.match(pattern, password) else False


def get_date_and_time(date: str):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").__str__().split(' ')


def get_date(date: str):
    return datetime.strftime(date, "%Y-%m-%d")


def get_time(time: str):
    return datetime.strftime(time, "%H:%M:%S")


def today_date():
    return (
        datetime.strptime(
            str(datetime.today().date()),
            "%Y-%m-%d",
        )
        + timedelta(days=1)
        - timedelta(seconds=1)
    )
