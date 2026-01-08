def is_missing_fields(location):
    return not location.get("city") or not location.get("country")
