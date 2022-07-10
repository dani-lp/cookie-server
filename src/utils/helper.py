import re

under_pat = re.compile(r"_([a-z])")


def camelize(name: str):
    return under_pat.sub(lambda x: x.group(1).upper(), name)
