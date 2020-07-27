import re


def routing(condition, contents):
    if re.search(condition, contents):
        return [True, re.sub(condition, "", contents)]
    return []
