from datetime import datetime

import pytz
from django.utils import timezone


def convert_to_timezone(dt, target_timezone):
    """
    Convert a datetime object to a specific timezone.
    Assumes input datetime is in IST (Asia/Kolkata).
    """
    if dt.tzinfo is None:
        # If naive datetime, assume it's in IST
        ist = pytz.timezone("Asia/Kolkata")
        dt = ist.localize(dt)

    target_tz = pytz.timezone(target_timezone)
    return dt.astimezone(target_tz)


def convert_from_timezone(dt, source_timezone):
    """
    Convert a datetime from a specific timezone to IST.
    """
    if dt.tzinfo is None:
        # If naive datetime, assume it's in the source timezone
        source_tz = pytz.timezone(source_timezone)
        dt = source_tz.localize(dt)

    ist = pytz.timezone("Asia/Kolkata")
    return dt.astimezone(ist)


def get_current_ist_time():
    """
    Get current time in IST.
    """
    ist = pytz.timezone("Asia/Kolkata")
    return timezone.now().astimezone(ist)
