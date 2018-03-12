import re


def startsWith(prefix,string):
    return bool(re.match(prefix, string, re.I))
