import re


def starts_with(prefix, string):
    return bool(re.match(prefix, string, re.I))

