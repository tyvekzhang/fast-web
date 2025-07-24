from datetime import datetime


def get_current_time(fmt: str = "%Y-%m-%d %H:%M:%S"):
    now = datetime.utcnow()
    now_str = now.strftime(fmt)
    now_str = now_str.replace(" ", "_")
    return now_str


def get_date_time():
    tmp = get_current_time()
    current = tmp.replace("-", "").replace("_", "")
    return current
