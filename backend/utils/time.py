from time import time
from datetime import datetime, timezone

def get_now_unix():
    return int(time())

def unix_to_date_string(unix: int, format: str, tz: timezone = timezone.utc):
    utc_datetime = datetime.fromtimestamp(unix, tz=tz)
    return utc_datetime.strftime(format)