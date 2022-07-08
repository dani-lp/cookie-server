from uuid import UUID
    
def is_valid_uuid(value, version=4):
    try:
        uuid = UUID(str(value), version=version)
    except ValueError:
        return False
    return str(uuid) == str(value)

def not_none(s, d):
    if s is None:
        return d
    return s