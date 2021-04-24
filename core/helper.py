from datetime import datetime

def str_to_date(date: str, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.strptime(date, format)


def date_to_str(date: datetime, format="%Y-%m-%dT%H:%M:%S"):
    return date.strftime(format)