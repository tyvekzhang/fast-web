from datetime import datetime, timezone


def get_current_time(fmt: str = "%Y-%m-%d %H:%M:%S"):
    now = datetime.now(timezone.utc)
    now_str = now.strftime(fmt)
    now_str = now_str.replace(" ", "_")
    return now_str


def get_date_time(fmt: str = "%Y%m%d_%H%M%S"):
    now = datetime.now(timezone.utc)
    return now.strftime(fmt)
