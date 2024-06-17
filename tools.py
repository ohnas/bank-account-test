from datetime import datetime, timedelta
import pytz


def get_yesterday():
    kst = pytz.timezone("Asia/Seoul")
    now = datetime.now(pytz.utc).astimezone(kst)
    yesterday = now - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    return yesterday_str


def format_converter(date_string):
    if len(date_string) == 8:
        date_object = datetime.strptime(date_string, "%Y%m%d")
        formatted_date_string = date_object.strftime("%Y-%m-%d")

        return formatted_date_string

    elif len(date_string) == 14:
        date_object = datetime.strptime(date_string, "%Y%m%d%H%M%S")
        formatted_date_string = date_object.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_date_string
