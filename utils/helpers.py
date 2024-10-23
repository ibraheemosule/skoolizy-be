import re


def has_special_char(s):
    pattern = r"[<>\'\";`$!&|\\(){}[\]^~#@/]"

    if re.search(pattern, s):
        return True
    return False


def is_password_valid(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-])[A-Za-z\d!@#$%^&*()_+[\]{};:"|,.<>?/\\`~\-]{8,}$'
    return True if re.match(pattern, password) else False
