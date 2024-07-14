import re


def has_special_char(s):
    pattern = r"[<>\'\";`$!&|\\(){}[\]^~#@/]"

    if re.search(pattern, s):
        return True
    return False
